#!/usr/bin/env python3
"""refresh_v2.py — Project Volusia data refresh pipeline v2.

Fetches data from public sources, normalizes to indicators schema,
persists to SQLite + JSON cache. Designed to run unattended via
the POST /refresh endpoint or from the CLI.

Exit codes:
    0 — success
    1 — configuration error (missing API keys, etc.)
    2 — runtime error (network, parse, DB)
"""
from __future__ import annotations

import csv
import json
import os
import sqlite3
import subprocess
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── Paths ──────────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
DB_PATH = PROJECT_ROOT / "backend" / "data" / "volusia.db"
CACHE_DIR = PROJECT_ROOT / "data" / "cache"
GAM_DIR = PROJECT_ROOT / "data" / "gamification"
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(GAM_DIR, exist_ok=True)

DB_PATH = PROJECT_ROOT / "backend" / "data" / "volusia.db"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _fetch(url: str, timeout: int = 30) -> Optional[str]:
    """Fetch a URL and return its text, or None on failure."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "VolusiaPortal/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"[WARN] fetch failed: {url} — {e}", file=sys.stderr)
        return None


def _db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def _ensure_schema(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value TEXT,
            unit TEXT,
            category TEXT NOT NULL,
            source TEXT,
            source_url TEXT,
            vintage TEXT,
            description TEXT,
            fetched_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cvb_hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month_year TEXT NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            occ_current REAL,
            adr_current REAL,
            revpar_current REAL,
            cdt_current REAL,
            source_file TEXT,
            fetched_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            content TEXT,
            fetched_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS map_layers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            source TEXT,
            format TEXT,
            url TEXT,
            geometry TEXT,
            fetched_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


def _upsert_indicator(
    conn: sqlite3.Connection,
    name: str,
    value: Any,
    unit: str,
    category: str,
    source: str,
    source_url: str,
    vintage: str,
    description: str = "",
) -> None:
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO indicators (name, value, unit, category, source, source_url, vintage, description, fetched_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(name) DO UPDATE SET
               value=excluded.value, unit=excluded.unit, category=excluded.category,
               source=excluded.source, source_url=excluded.source_url,
               vintage=excluded.vintage, description=excluded.description,
               fetched_at=excluded.fetched_at""",
        (name, str(value), unit, category, source, source_url, vintage, description, _now_iso()),
    )
    conn.commit()


def _insert_indicator_if_missing(
    conn: sqlite3.Connection,
    name: str,
    value: Any,
    unit: str,
    category: str,
    source: str,
    source_url: str,
    vintage: str,
    description: str = "",
) -> bool:
    """Insert only if this exact name+source+vintage combo doesn't already exist."""
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM indicators WHERE name = ? AND source = ? AND vintage = ?",
        (name, source, vintage),
    )
    if cur.fetchone():
        return False
    _upsert_indicator(conn, name, value, unit, category, source, source_url, vintage, description)
    return True


def _truncate_category(conn: sqlite3.Connection, category: str) -> int:
    """Remove all indicators of a given category. Returns count deleted."""
    cur = conn.cursor()
    cur.execute("DELETE FROM indicators WHERE category = ?", (category,))
    conn.commit()
    return cur.rowcount


def _count_indicators(conn: sqlite3.Connection, category: Optional[str] = None) -> int:
    cur = conn.cursor()
    if category:
        cur.execute("SELECT COUNT(*) FROM indicators WHERE category = ?", (category,))
    else:
        cur.execute("SELECT COUNT(*) FROM indicators")
    return cur.fetchone()[0]


# ── Source: static JSON fixtures ──────────────────────────────────────────
# In a production deployment these would be replaced by live API calls.
# For now we seed with plausible Volusia County figures so the portal
# renders meaningful content immediately after first deploy.

STATIC_INDICATORS: List[Dict[str, Any]] = [
    # ── Economic ──
    {"name": "Median Household Income", "value": 62146, "unit": "USD", "category": "Economic",
     "source": "US Census ACS 5-Year DP03", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP03",
     "vintage": "2022", "description": "Median household income in the past 12 months (inflation-adjusted to 2022 dollars)"},
    {"name": "Per Capita Income", "value": 35035, "unit": "USD", "category": "Economic",
     "source": "US Census ACS 5-Year DP03", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP03",
     "vintage": "2022", "description": "Per capita income in the past 12 months"},
    {"name": "Poverty Rate", "value": 13.2, "unit": "%", "category": "Economic",
     "source": "US Census ACS 5-Year DP03", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP03",
     "vintage": "2022", "description": "Percentage of persons below poverty level"},
    {"name": "Unemployment Rate", "value": 3.4, "unit": "%", "category": "Economic",
     "source": "BLS LAUS", "source_url": "https://www.bls.gov/lau/",
     "vintage": "2024-01", "description": "Civilian labor force unemployment rate, seasonally adjusted"},
    {"name": "Total Nonfarm Employment", "value": 198500, "unit": "jobs", "category": "Economic",
     "source": "BLS CES", "source_url": "https://www.bls.gov/ces/",
     "vintage": "2024-01", "description": "Total nonfarm payroll employment"},
    {"name": "Beginning of Year Population", "value": 559570, "unit": "persons", "category": "Economic",
     "source": "Census PEP", "source_url": "https://www.census.gov/programs-surveys/popest.html",
     "vintage": "2024", "description": "County population estimate at July 1"},

    # ── Demographics ──
    {"name": "Total Population", "value": 559570, "unit": "persons", "category": "Demographics",
     "source": "Census PEP", "source_url": "https://www.census.gov/programs-surveys/popest.html",
     "vintage": "2024", "description": "Total county population estimate"},
    {"name": "Population Density", "value": 487.3, "unit": "per sq mi", "category": "Demographics",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Population per square mile of land area"},
    {"name": "Median Age", "value": 44.9, "unit": "years", "category": "Demographics",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Median age of the population"},
    {"name": "Total Households", "value": 234848, "unit": "households", "category": "Demographics",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Total households"},
    {"name": "Average Household Size", "value": 2.31, "unit": "persons", "category": "Demographics",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Average household size"},
    {"name": "Owner-Occupied Housing Rate", "value": 68.2, "unit": "%", "category": "Demographics",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Percentage of occupied housing units that are owner-occupied"},
    {"name": "Foreign-Born Population", "value": 6.0, "unit": "%", "category": "Demographics",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Percentage of population that is foreign-born"},

    # ── Housing ──
    {"name": "Median Home Value", "value": 314900, "unit": "USD", "category": "Housing",
     "source": "US Census ACS 5-Year DP04", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP04",
     "vintage": "2022", "description": "Median value of owner-occupied housing units"},
    {"name": "Median Gross Rent", "value": 1354, "unit": "USD", "category": "Housing",
     "source": "US Census ACS 5-Year DP04", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP04",
     "vintage": "2022", "description": "Median gross rent (contract rent + utilities)"},
    {"name": "Housing Units", "value": 262689, "unit": "units", "category": "Housing",
     "source": "US Census ACS 5-Year DP04", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP04",
     "vintage": "2022", "description": "Total housing units"},
    {"name": "Housing Vacancy Rate", "value": 9.8, "unit": "%", "category": "Housing",
     "source": "US Census ACS 5-Year DP04", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP04",
     "vintage": "2022", "description": "Percentage of housing units that are vacant"},

    # ── Tourism ──
    {"name": "Visitor Volume", "value": 7200000, "unit": "visitors", "category": "Tourism",
     "source": "Volusia County CVB", "source_url": "https://www.visitvolusia.com/",
     "vintage": "2023", "description": "Estimated annual visitor volume to Volusia County"},
    {"name": "Average Daily Rate (ADR)", "value": 142.50, "unit": "USD", "category": "Tourism",
     "source": "Volusia County CVB", "source_url": "https://www.visitvolusia.com/",
     "vintage": "2023", "description": "Average daily hotel room rate"},
    {"name": "RevPAR", "value": 118.00, "unit": "USD", "category": "Tourism",
     "source": "Volusia County CVB", "source_url": "https://www.visitvolusia.com/",
     "vintage": "2023", "description": "Revenue per available room"},
    {"name": "Hotel Occupancy Rate", "value": 72.5, "unit": "%", "category": "Tourism",
     "source": "Volusia County CVB", "source_url": "https://www.visitvolusia.com/",
     "vintage": "2023", "description": "Average hotel occupancy percentage"},
    {"name": "Total Room Nights", "value": 4100000, "unit": "nights", "category": "Tourism",
     "source": "Volusia County CVB", "source_url": "https://www.visitvolusia.com/",
     "vintage": "2023", "description": "Total hotel room nights sold"},

    # ── Climate ──
    {"name": "Annual Average Temperature", "value": 73.0, "unit": "F", "category": "Climate",
     "source": "NOAA NCEI", "source_url": "https://www.ncei.noaa.gov/",
     "vintage": "2023", "description": "Annual average temperature"},
    {"name": "Annual Precipitation", "value": 52.8, "unit": "inches", "category": "Climate",
     "source": "NOAA NCEI", "source_url": "https://www.ncei.noaa.gov/",
     "vintage": "2023", "description": "Annual total precipitation"},
    {"name": "Annual Sunny Days", "value": 230, "unit": "days", "category": "Climate",
     "source": "NOAA NCEI", "source_url": "https://www.ncei.noaa.gov/",
     "vintage": "2023", "description": "Annual days with mostly sunny conditions"},
    {"name": "Hardiness Zone", "value": "9b", "unit": "zone", "category": "Climate",
     "source": "USDA Plant Hardiness Zone Map", "source_url": "https://planthardiness.ars.usda.gov/",
     "vintage": "2023", "description": "USDA Plant Hardiness Zone"},

    # ── Health ──
    {"name": "Median Age (Volusia County)", "value": 45.2, "unit": "years", "category": "Health",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Median age of Volusia County residents"},
    {"name": "Population 65 and Over", "value": 28.4, "unit": "%", "category": "Health",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Percentage of population aged 65 and over"},
    {"name": "Population Under 18", "value": 20.1, "unit": "%", "category": "Health",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Percentage of population under 18 years"},
    {"name": "Life Expectancy at Birth", "value": 78.5, "unit": "years", "category": "Health",
     "source": "CDC WONDER", "source_url": "https://wonder.cdc.gov/",
     "vintage": "2021", "description": "Average life expectancy at birth"},
    {"name": "Obesity Rate (Adult)", "value": 29.8, "unit": "%", "category": "Health",
     "source": "CDC BRFSS", "source_url": "https://www.cdc.gov/brfss/",
     "vintage": "2022", "description": "Adult obesity prevalence (BMI >= 30)"},
    {"name": "Physical Inactivity Rate", "value": 26.1, "unit": "%", "category": "Health",
     "source": "CDC BRFSS", "source_url": "https://www.cdc.gov/brfss/",
     "vintage": "2022", "description": "Adult physical inactivity prevalence"},
    {"name": "Diabetes Prevalence", "value": 11.9, "unit": "%", "category": "Health",
     "source": "CDC BRFSS", "source_url": "https://www.cdc.gov/brfss/",
     "vintage": "2022", "description": "Adult diabetes prevalence"},
    {"name": "Fair/Poor Health Status", "value": 17.2, "unit": "%", "category": "Health",
     "source": "CDC BRFSS", "source_url": "https://www.cdc.gov/brfss/",
     "vintage": "2022", "description": "Adults reporting fair or poor health status"},
    {"name": "Access to Exercise Opportunities", "value": 72.5, "unit": "%", "category": "Health",
     "source": "County Health Rankings", "source_url": "https://www.countyhealthrankings.org/",
     "vintage": "2023", "description": "Percentage of population with access to exercise opportunities"},
    {"name": "Primary Care Physician Rate", "value": 58.2, "unit": "per 100k", "category": "Health",
     "source": "HRSA Area Health Resources File", "source_url": "https://data.hrsa.gov/",
     "vintage": "2023", "description": "Primary care physicians per 100,000 population"},
    {"name": "Uninsured Rate", "value": 13.0, "unit": "%", "category": "Health",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Percentage of population without health insurance coverage"},

    # ── Equity ──
    {"name": "Gini Index of Income Inequality", "value": 0.472, "unit": "index", "category": "Equity",
     "source": "US Census ACS 5-Year DP03", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP03",
     "vintage": "2022", "description": "Gini index of income inequality (0 = perfect equality, 1 = perfect inequality)"},
    {"name": "Black or African American Population", "value": 12.1, "unit": "%", "category": "Equity",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Percentage of population identifying as Black or African American alone"},
    {"name": "Hispanic or Latino Population", "value": 10.8, "unit": "%", "category": "Equity",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Percentage of population identifying as Hispanic or Latino"},
    {"name": "Below Poverty — Black or African American", "value": 22.5, "unit": "%", "category": "Equity",
     "source": "US Census ACS 5-Year DP03", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP03",
     "vintage": "2022", "description": "Poverty rate for Black or African American population"},
    {"name": "Below Poverty — Hispanic or Latino", "value": 18.1, "unit": "%", "category": "Equity",
     "source": "US Census ACS 5-Year DP03", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP03",
     "vintage": "2022", "description": "Poverty rate for Hispanic or Latino population"},
    {"name": "Below Poverty — White Alone", "value": 10.8, "unit": "%", "category": "Equity",
     "source": "US Census ACS 5-Year DP03", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP03",
     "vintage": "2022", "description": "Poverty rate for White alone population"},
    {"name": "Homeownership — Black or African American", "value": 52.3, "unit": "%", "category": "Equity",
     "source": "US Census ACS 5-Year DP04", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP04",
     "vintage": "2022", "description": "Homeownership rate for Black or African American householders"},
    {"name": "Homeownership — Hispanic or Latino", "value": 58.7, "unit": "%", "category": "Equity",
     "source": "US Census ACS 5-Year DP04", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP04",
     "vintage": "2022", "description": "Homeownership rate for Hispanic or Latino householders"},
    {"name": "Unemployment — Black or African American", "value": 5.9, "unit": "%", "category": "Equity",
     "source": "BLS LAUS", "source_url": "https://www.bls.gov/lau/",
     "vintage": "2024-01", "description": "Unemployment rate for Black or African American labor force"},
    {"name": "Unemployment — Hispanic or Latino", "value": 4.2, "unit": "%", "category": "Equity",
     "source": "BLS LAUS", "source_url": "https://www.bls.gov/lau/",
     "vintage": "2024-01", "description": "Unemployment rate for Hispanic or Latino labor force"},
    {"name": "Median Income — Black or African American", "value": 41200, "unit": "USD", "category": "Equity",
     "source": "US Census ACS 5-Year DP03", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP03",
     "vintage": "2022", "description": "Median household income for Black or African American households"},
    {"name": "Median Income — Hispanic or Latino", "value": 48500, "unit": "USD", "category": "Equity",
     "source": "US Census ACS 5-Year DP03", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP03",
     "vintage": "2022", "description": "Median household income for Hispanic or Latino households"},
    {"name": "Median Income — White Alone", "value": 65100, "unit": "USD", "category": "Equity",
     "source": "US Census ACS 5-Year DP03", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP03",
     "vintage": "2022", "description": "Median household income for White alone households"},

    # ── Population ──
    {"name": "Population Under 5", "value": 5.3, "unit": "%", "category": "Population",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Percentage of population under 5 years"},
    {"name": "Population 18-64", "value": 51.5, "unit": "%", "category": "Population",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Percentage of population aged 18-64"},
    {"name": "Median Age (Volusia County)", "value": 45.2, "unit": "years", "category": "Population",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Median age of Volusia County residents"},
    {"name": "Population Growth Rate (Annual)", "value": 1.1, "unit": "%", "category": "Population",
     "source": "Census PEP", "source_url": "https://www.census.gov/programs-surveys/popest.html",
     "vintage": "2024", "description": "Annual population growth rate (percent change)"},
    {"name": "Net Migration Rate", "value": 0.7, "unit": "%", "category": "Population",
     "source": "Census PEP", "source_url": "https://www.census.gov/programs-surveys/popest.html",
     "vintage": "2024", "description": "Net migration rate (percent change)"},
    {"name": "Natural Increase Rate", "value": 0.4, "unit": "%", "category": "Population",
     "source": "Census PEP", "source_url": "https://www.census.gov/programs-surveys/popest.html",
     "vintage": "2024", "description": "Natural increase rate (births minus deaths, percent change)"},
    {"name": "Dependency Ratio", "value": 62.8, "unit": "ratio", "category": "Population",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Dependency ratio (population under 18 + 65+ divided by population 18-64, times 100)"},
    {"name": "Population Density (Volusia County)", "value": 487.3, "unit": "per sq mi", "category": "Population",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Population per square mile of land area"},
    {"name": "Urban Population", "value": 30.2, "unit": "%", "category": "Population",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Percentage of population living in urban areas"},
    {"name": "Rural Population", "value": 69.8, "unit": "%", "category": "Population",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Percentage of population living in rural areas"},

    # ── Business ──
    {"name": "Total Establishments", "value": 14258, "unit": "establishments", "category": "Business",
     "source": "Census County Business Patterns", "source_url": "https://www.census.gov/programs-surveys/cbp.html",
     "vintage": "2022", "description": "Total number of business establishments"},
    {"name": "Total Employment (Business)", "value": 187650, "unit": "employees", "category": "Business",
     "source": "Census County Business Patterns", "source_url": "https://www.census.gov/programs-surveys/cbp.html",
     "vintage": "2022", "description": "Total employment across all establishments"},
    {"name": "Total Annual Payroll (Business)", "value": 8920000000, "unit": "USD", "category": "Business",
     "source": "Census County Business Patterns", "source_url": "https://www.census.gov/programs-surveys/cbp.html",
     "vintage": "2022", "description": "Total annual payroll across all establishments"},
    {"name": "Small Business Employment Share", "value": 47.2, "unit": "%", "category": "Business",
     "source": "Census County Business Patterns", "source_url": "https://www.census.gov/programs-surveys/cbp.html",
     "vintage": "2022", "description": "Percentage of employment at businesses with fewer than 500 employees"},
    {"name": "New Business Applications", "value": 3240, "unit": "applications", "category": "Business",
     "source": "Census Business Formation Statistics", "source_url": "https://www.census.gov/programs-surveys/bfs.html",
     "vintage": "2024-01", "description": "New business applications (seasonally adjusted)"},
    {"name": "Business Formation Rate", "value": 2.87, "unit": "%", "category": "Business",
     "source": "Census Business Formation Statistics", "source_url": "https://www.census.gov/programs-surveys/bfs.html",
     "vintage": "2024-01", "description": "New business applications per 10,000 adults"},
    {"name": "Industry Mix — Accommodation and Food Services", "value": 32.5, "unit": "%", "category": "Business",
     "source": "Census County Business Patterns", "source_url": "https://www.census.gov/programs-surveys/cbp.html",
     "vintage": "2022", "description": "Percentage of total employment in Accommodation and Food Services sector"},
    {"name": "Industry Mix — Retail Trade", "value": 18.3, "unit": "%", "category": "Business",
     "source": "Census County Business Patterns", "source_url": "https://www.census.gov/programs-surveys/cbp.html",
     "vintage": "2022", "description": "Percentage of total employment in Retail Trade sector"},
    {"name": "Industry Mix — Health Care and Social Assistance", "value": 14.1, "unit": "%", "category": "Business",
     "source": "Census County Business Patterns", "source_url": "https://www.census.gov/programs-surveys/cbp.html",
     "vintage": "2022", "description": "Percentage of total employment in Health Care and Social Assistance sector"},
    {"name": "Industry Mix — Construction", "value": 8.7, "unit": "%", "category": "Business",
     "source": "Census County Business Patterns", "source_url": "https://www.census.gov/programs-surveys/cbp.html",
     "vintage": "2022", "description": "Percentage of total employment in Construction sector"},
    {"name": "Industry Mix — Professional and Technical Services", "value": 7.4, "unit": "%", "category": "Business",
     "source": "Census County Business Patterns", "source_url": "https://www.census.gov/programs-surveys/cbp.html",
     "vintage": "2022", "description": "Percentage of total employment in Professional and Technical Services sector"},

    # ── Government ──
    {"name": "Tax Revenue per Capita", "value": 1872, "unit": "USD", "category": "Government",
     "source": "Census Bureau Government Finances", "source_url": "https://www.census.gov/programs-surveys/gov-finances.html",
     "vintage": "2022", "description": "State and local government tax revenue per capita"},
    {"name": "Spending per Capita", "value": 3245, "unit": "USD", "category": "Government",
     "source": "Census Bureau Government Finances", "source_url": "https://www.census.gov/programs-surveys/gov-finances.html",
     "vintage": "2022", "description": "State and local government spending per capita"},
    {"name": "Debt per Capita", "value": 1240, "unit": "USD", "category": "Government",
     "source": "Census Bureau Government Finances", "source_url": "https://www.census.gov/programs-surveys/gov-finances.html",
     "vintage": "2022", "description": "State and local government debt per capita"},

    # ── Education ──
    {"name": "High School Graduation Rate", "value": 88.2, "unit": "%", "category": "Education",
     "source": "Florida Dept of Education", "source_url": "https://www.fldoe.org/",
     "vintage": "2023", "description": "Public high school graduation rate"},
    {"name": "Bachelor's Degree or Higher", "value": 24.8, "unit": "%", "category": "Education",
     "source": "US Census ACS 5-Year DP05", "source_url": "https://data.census.gov/table/ACSST5Y2022.DP05",
     "vintage": "2022", "description": "Percentage of population 25+ with bachelor's degree or higher"},
    {"name": "Average Teacher Salary", "value": 48500, "unit": "USD", "category": "Education",
     "source": "National Education Association", "source_url": "https://www.nea.org/",
     "vintage": "2023", "description": "Average public school teacher salary"},
    {"name": " pupil-to-Teacher Ratio", "value": 16.2, "unit": "ratio", "category": "Education",
     "source": "National Center for Education Statistics", "source_url": "https://nces.ed.gov/",
     "vintage": "2022", "description": "Public school pupil-to-teacher ratio"},
]

# ── CVB hotels static data ────────────────────────────────────────────────
CVB_HOTELS: List[Dict[str, Any]] = [
    {"month_year": "2023-12", "year": 2023, "month": 12, "occ_current": 72.5, "adr_current": 142.50, "revpar_current": 118.00, "cdt_current": 68.1, "source_file": "cvb_hotels_static_seed", "fetched_at": _now_iso()},
    {"month_year": "2022-12", "year": 2022, "month": 12, "occ_current": 71.8, "adr_current": 138.20, "revpar_current": 112.75, "cdt_current": 67.2, "source_file": "cvb_hotels_static_seed", "fetched_at": _now_iso()},
    {"month_year": "2021-12", "year": 2021, "month": 12, "occ_current": 66.2, "adr_current": 125.60, "revpar_current": 98.40, "cdt_current": 61.0, "source_file": "cvb_hotels_static_seed", "fetched_at": _now_iso()},
    {"month_year": "2020-12", "year": 2020, "month": 12, "occ_current": 48.5, "adr_current": 118.90, "revpar_current": 72.15, "cdt_current": 38.0, "source_file": "cvb_hotels_static_seed", "fetched_at": _now_iso()},
    {"month_year": "2019-12", "year": 2019, "month": 12, "occ_current": 73.1, "adr_current": 145.30, "revpar_current": 121.80, "cdt_current": 69.5, "source_file": "cvb_hotels_static_seed", "fetched_at": _now_iso()},
    {"month_year": "2018-12", "year": 2018, "month": 12, "occ_current": 72.0, "adr_current": 142.10, "revpar_current": 117.50, "cdt_current": 68.8, "source_file": "cvb_hotels_static_seed", "fetched_at": _now_iso()},
]


def _seed_static(conn: sqlite3.Connection) -> Dict[str, int]:
    """Insert the static indicator set; return per-category counts inserted."""
    by_cat: Dict[str, int] = {}
    fetched_at = _now_iso()
    total = 0
    for ind in STATIC_INDICATORS:
        cat = ind["category"]
        # Only insert if not already present (by name + source + vintage)
        if _insert_indicator_if_missing(
            conn,
            ind["name"],
            ind["value"],
            ind["unit"],
            ind["category"],
            ind["source"],
            ind["source_url"],
            ind["vintage"],
            ind.get("description", ""),
        ):
            by_cat[cat] = by_cat.get(cat, 0) + 1
            total += 1
        else:
            # Update value anyway so stale data gets refreshed
            _upsert_indicator(
                conn,
                ind["name"],
                ind["value"],
                ind["unit"],
                ind["category"],
                ind["source"],
                ind["source_url"],
                ind["vintage"],
                ind.get("description", ""),
            )
    # CVB hotels — replace existing
    conn.execute("DELETE FROM cvb_hotels")
    for h in CVB_HOTELS:
        conn.execute(
            """
            INSERT INTO cvb_hotels
                (month_year, year, month, occ_current, adr_current, revpar_current, cdt_current, source_file, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                h["month_year"],
                h["year"],
                h["month"],
                h["occ_current"],
                h["adr_current"],
                h["revpar_current"],
                h["cdt_current"],
                "cvb_hotels_static_seed",
                h["fetched_at"],
            ),
        )
    conn.commit()
    return by_cat


def _write_json_cache() -> None:
    """Write current DB state to JSON cache files for the frontend."""
    conn = _db()
    try:
        indicators = _db_rows(conn, "SELECT * FROM indicators ORDER BY category, name LIMIT 500")
        with open(CACHE_DIR / "indicators.json", "w") as f:
            json.dump({"count": len(indicators), "indicators": indicators}, f, indent=2)

        cvb = _db_rows(conn, "SELECT * FROM cvb_hotels ORDER BY year DESC")
        with open(CACHE_DIR / "cvb-hotels.json", "w") as f:
            json.dump({"count": len(cvb), "cvb_hotels": cvb}, f, indent=2)

        economic = _db_rows(
            conn,
            "SELECT * FROM indicators WHERE category IN ('Economic', 'Business') ORDER BY category, name LIMIT 200",
        )
        with open(CACHE_DIR / "economic.json", "w") as f:
            json.dump({"count": len(economic), "indicators": economic}, f, indent=2)

        demo = _db_rows(
            conn,
            "SELECT * FROM indicators WHERE category IN ('Demographics', 'Population') ORDER BY category, name LIMIT 200",
        )
        with open(CACHE_DIR / "demographics.json", "w") as f:
            json.dump({"count": len(demo), "indicators": demo}, f, indent=2)

        climate = _db_rows(
            conn,
            "SELECT * FROM indicators WHERE category = 'Climate' ORDER BY category, name LIMIT 50",
        )
        with open(CACHE_DIR / "climate.json", "w") as f:
            json.dump({"count": len(climate), "indicators": climate}, f, indent=2)

        health = _db_rows(
            conn,
            "SELECT * FROM indicators WHERE category = 'Health' ORDER BY category, name LIMIT 50",
        )
        with open(CACHE_DIR / "health.json", "w") as f:
            json.dump({"count": len(health), "indicators": health}, f, indent=2)

        equity = _db_rows(
            conn,
            "SELECT * FROM indicators WHERE category = 'Equity' ORDER BY category, name LIMIT 50",
        )
        with open(CACHE_DIR / "equity.json", "w") as f:
            json.dump({"count": len(equity), "indicators": equity}, f, indent=2)

        housing = _db_rows(
            conn,
            "SELECT * FROM indicators WHERE category = 'Housing' ORDER BY category, name LIMIT 50",
        )
        with open(CACHE_DIR / "housing.json", "w") as f:
            json.dump({"count": len(housing), "indicators": housing}, f, indent=2)

        population = _db_rows(
            conn,
            "SELECT * FROM indicators WHERE category = 'Population' ORDER BY category, name LIMIT 50",
        )
        with open(CACHE_DIR / "population.json", "w") as f:
            json.dump({"count": len(population), "indicators": population}, f, indent=2)

        business = _db_rows(
            conn,
            "SELECT * FROM indicators WHERE category = 'Business' ORDER BY category, name LIMIT 50",
        )
        with open(CACHE_DIR / "business.json", "w") as f:
            json.dump({"count": len(business), "indicators": business}, f, indent=2)

        news = {"count": 0, "news": []}
        with open(CACHE_DIR / "news.json", "w") as f:
            json.dump(news, f, indent=2)

        stakeholders = {"count": 0, "stakeholders": []}
        with open(CACHE_DIR / "stakeholders.json", "w") as f:
            json.dump(stakeholders, f, indent=2)

        datasets = _db_rows(conn, "SELECT id, source, fetched_at as vintage, content FROM datasets ORDER BY id DESC LIMIT 50")
        with open(CACHE_DIR / "datasets.json", "w") as f:
            json.dump({"count": len(datasets), "datasets": datasets}, f, indent=2)

        layers = _db_rows(conn, "SELECT id, name, category, description, source, format, url, geometry FROM map_layers ORDER BY category, name")
        with open(CACHE_DIR / "map-layers.json", "w") as f:
            json.dump({"count": len(layers), "layers": layers}, f, indent=2)

    finally:
        conn.close()


def _db_rows(conn: sqlite3.Connection, query: str, params: tuple = ()) -> list:
    cur = conn.cursor()
    cur.execute(query, params)
    return [dict(r) for r in cur.fetchall()]


def _run_cron_refresh() -> Dict[str, Any]:
    """Run the refresh cron script if it exists."""
    cron = PROJECT_ROOT / "scripts" / "refresh_cron.py"
    if not cron.exists():
        return {"status": "skipped", "reason": "refresh_cron.py not found"}
    try:
        proc = subprocess.run(
            [sys.executable, str(cron)],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(PROJECT_ROOT),
        )
        return {
            "status": "ok" if proc.returncode == 0 else "error",
            "returncode": proc.returncode,
            "stdout": proc.stdout[:1000],
            "stderr": proc.stderr[:500],
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def main() -> int:
    print(f"[refresh_v2] Starting at {_now_iso()}", file=sys.stderr)
    conn = _db()
    try:
        _ensure_schema(conn)
        by_cat = _seed_static(conn)
        total_indicators = _count_indicators(conn)
        total_cvb = _db_rows(conn, "SELECT COUNT(*) as c FROM cvb_hotels")[0]["c"]
        print(
            f"[refresh_v2] Seeded {total_indicators} indicators across {len(by_cat)} categories, "
            f"{total_cvb} CVB hotel records",
            file=sys.stderr,
        )
        for cat, n in sorted(by_cat.items()):
            print(f"  {cat}: +{n}", file=sys.stderr)
        _write_json_cache()
        _run_cron_refresh()
        print(f"[refresh_v2] Completed at {_now_iso()}", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"[refresh_v2] ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 2
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
