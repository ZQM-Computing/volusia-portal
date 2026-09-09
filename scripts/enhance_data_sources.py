"""Project Volusia — Data Source Enhancement v1

Adds new Florida-specific data sources, data freshness monitoring,
and source diversity tracking.

New sources added:
  - FRED API (direct JSON API, replaces fragile HTML scraping)
  - Florida DEO Labor Market Statistics
  - FDLE Uniform Crime Report (Volusia County)
  - Florida CHARTS (Community Health Assessment Resource Tool)
  - Volusia County Property Appraiser (parcel counts)
"""

import os
import re
import io
import csv
import json
import sqlite3
import requests
from pathlib import Path
from datetime import datetime, date, timedelta

# --- Paths ---
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CACHE_DIR = DATA_DIR / "cache"
DB_PATH = DATA_DIR / "volusia.db"
PUBLIC_DIR = DB_PATH.parent  # public snapshots land in data/

CACHE_DIR.mkdir(parents=True, exist_ok=True)

TODAY = date.today()
NOW = datetime.now()

# --- API Keys (optional — graceful fallback) ---
FRED_API_KEY = os.environ.get("FRED_API_KEY", "")


def fetch_url(url: str, timeout: int = 30) -> str | None:
    """Fetch URL content with standard headers."""
    try:
        resp = requests.get(url, timeout=timeout, headers={
            "User-Agent": "Project-Volusia/1.0 (Data Research)",
            "Accept": "application/json"
        })
        resp.raise_for_status()
        return resp.text
    except Exception:
        return None


# ---------------------------------------------------------------------------
# NEW SOURCE 1: FRED Direct API
# Replaces fragile HTML scraping of fred.stlouisfed.org
# ---------------------------------------------------------------------------
def fetch_fred_api(series_ids: list[str]) -> dict:
    """Fetch economic time series from FRED's JSON API.
    
    FRED provides a free JSON API that's far more reliable than scraping
    the HTML pages. Requires an API key (free registration).
    
    Falls back to curated values if API key is missing.
    """
    if not FRED_API_KEY:
        # Fallback: curated FRED values (last verified)
        curated = {
            "FLVOLU7POP": {"value": 553284.0, "date": "2024-01-01", "title": "Volusia County Population"},
            "FLVOLU7URN": {"value": 3.5, "date": "2025-06-01", "title": "Volusia County Unemployment Rate"},
            "FLVOLU7PCPI": {"value": 48712.0, "date": "2023-01-01", "title": "Per Capita Personal Income"},
            "FLVOLU7NRMN": {"value": 11.2, "date": "2025-06-01", "title": "Nonfarm Payroll Employment (thousands)"},
        }
        return {"source": "FRED (curated fallback)", "series": curated, "note": "FRED_API_KEY not set — using curated values"}
    
    results = {}
    for sid in series_ids:
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={sid}&api_key={FRED_API_KEY}&file_type=json&sort_order=desc&limit=1"
        content = fetch_url(url)
        if not content:
            continue
        try:
            data = json.loads(content)
            obs = data.get("observations", [{}])[0]
            results[sid] = {
                "value": float(obs.get("value", 0)),
                "date": obs.get("date", ""),
                "title": sid
            }
        except (json.JSONDecodeError, ValueError):
            continue
    
    return {"source": "FRED API", "series": results, "fetchedAt": NOW.isoformat()}


# ---------------------------------------------------------------------------
# NEW SOURCE 2: Florida DEO Labor Market Statistics
# ---------------------------------------------------------------------------
def fetch_florida_deo() -> dict | None:
    """Fetch Florida Dept of Economic Opportunity labor market data for Volusia County.
    
    FL DEO provides labor market stats via their public reports.
    We extract key figures from the HTML.
    """
    content = fetch_url("https://floridajobs.org/workforce-statistics/publications-and-reports/labor-market-statistics")
    if not content:
        return None
    
    result = {
        "source": "Florida DEO Labor Market Statistics",
        "sourceUrl": "https://floridajobs.org/workforce-statistics",
        "fetchedAt": NOW.isoformat()
    }
    
    # Extract unemployment rate mentions
    m = re.search(r'Volusia[^<]*?(\d+\.\d+)%\s*(?:unemployment|jobless)', content, re.IGNORECASE)
    if m:
        result["unemploymentRate"] = float(m.group(1))
    
    # Extract labor force
    m = re.search(r'Volusia[^<]*?(\d{1,3}(?:,\d{3})+)\s*(?:labor force|employed)', content, re.IGNORECASE)
    if m:
        result["laborForce"] = int(m.group(1).replace(",", ""))
    
    return result


# ---------------------------------------------------------------------------
# NEW SOURCE 3: FDLE Uniform Crime Report
# ---------------------------------------------------------------------------
def fetch_fdle_crime() -> dict | None:
    """Fetch Florida Department of Law Enforcement crime data for Volusia County.
    
    FDLE publishes crime statistics per county. We scrape the summary page.
    """
    content = fetch_url("https://www.fdle.state.fl.us/FSAC/UCR/Reports/County-Crime-Stats")
    if not content:
        return None
    
    result = {
        "source": "FDLE Uniform Crime Report",
        "sourceUrl": "https://www.fdle.state.fl.us/FSAC/UCR/Reports/County-Crime-Stats",
        "fetchedAt": NOW.isoformat()
    }
    
    # Try to find Volusia County data
    patterns = [
        r'Volusia.*?(\d+\.\d+)\s*per\s*100,000',
        r'Volusia.*?crime rate.*?(\d+\.\d+)',
        r'Volusia.*?(\d+)\s*index crimes',
    ]
    for pat in patterns:
        m = re.search(pat, content, re.IGNORECASE | re.DOTALL)
        if m:
            result["crimeRatePer100k"] = float(m.group(1))
            break
    
    return result


# ---------------------------------------------------------------------------
# NEW SOURCE 4: Florida CHARTS (Community Health Assessment)
# ---------------------------------------------------------------------------
def fetch_florida_charts() -> dict | None:
    """Fetch Florida Department of Health CHARTS data for Volusia County.
    
    CHARTS provides community health indicators (birth rates, death rates,
    uninsured rate, etc.) for Florida counties.
    """
    content = fetch_url("https://www.flhealthcharts.gov/ChartsReports/rdPage.aspx?rdReport=ChartsProfiles.CountyProfile")
    if not content:
        return None
    
    result = {
        "source": "Florida CHARTS (FL Dept of Health)",
        "sourceUrl": "https://www.flhealthcharts.gov/",
        "fetchedAt": NOW.isoformat()
    }
    
    # Extract key health indicators
    health_patterns = {
        "uninsuredRate": r'uninsured.*?(\d+\.\d+)%',
        "uninsuredRateAdult": r'adult uninsured.*?(\d+\.\d+)%',
        "physiciansPer100k": r'physicians.*?per.*?100,000.*?(\d+\.?\d*)',
        "preventableHospitalizations": r'preventable hospitalizations.*?(\d+\.?\d*)',
        "lifeExpectancy": r'life expectancy.*?(\d+\.?\d*)',
    }
    
    for key, pat in health_patterns.items():
        m = re.search(pat, content, re.IGNORECASE)
        if m:
            result[key] = float(m.group(1))
    
    return result


# ---------------------------------------------------------------------------
# NEW SOURCE 5: Volusia County Property Appraiser
# ---------------------------------------------------------------------------
def fetch_property_appraiser() -> dict | None:
    """Fetch Volusia County parcel counts from the Property Appraiser's office.
    
    This gives us the total number of taxable parcels — a proxy for
    development density and tax base.
    """
    content = fetch_url("https://www.volusia.org/services/property-appraiser/")
    if not content:
        return None
    
    result = {
        "source": "Volusia County Property Appraiser",
        "sourceUrl": "https://www.volusia.org/services/property-appraiser/",
        "fetchedAt": NOW.isoformat()
    }
    
    m = re.search(r'(\d{1,3}(?:,\d{3})+)\s*parcels', content, re.IGNORECASE)
    if m:
        result["totalParcels"] = int(m.group(1).replace(",", ""))
    
    m = re.search(r'total.*?assessed.*?value.*?\$([\d,.]+)\s*(billion|million|trillion)', content, re.IGNORECASE)
    if m:
        val = float(m.group(1).replace(",", ""))
        mult = {"million": 1e6, "billion": 1e9, "trillion": 1e12}
        result["assessedValue"] = val * mult.get(m.group(2).lower(), 1)
    
    return result


# ---------------------------------------------------------------------------
# DATA QUALITY & FRESHNESS MONITORING
# ---------------------------------------------------------------------------
def get_data_freshness(db_path: Path) -> dict:
    """Analyze data freshness across all indicators.
    
    Returns:
        dict with:
        - total_indicators: count
        - stale_indicators: list older than 365 days
        - fresh_indicators: list updated within 90 days
        - by_category: breakdown per category
    """
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            "SELECT name, value, unit, category, source, source_url, vintage, description, "
            "CASE WHEN fetched_at IS NOT NULL THEN fetched_at ELSE '' END as fa "
            "FROM indicators ORDER BY category, name"
        ).fetchall()
    finally:
        conn.close()
    
    stale = []
    fresh = []
    by_cat = {}
    all_indicators = []
    
    for r in rows:
        indicator = dict(r)
        all_indicators.append(indicator)
        cat = indicator.get("category", "Unknown")
        by_cat.setdefault(cat, []).append(indicator)
        
        # Check vintage freshness
        vintage = indicator.get("vintage", "")
        is_stale = False
        
        if vintage:
            # Try to parse year from vintage
            year_match = re.search(r'(20\d{2})', vintage)
            if year_match:
                year = int(year_match.group(1))
                if year < TODAY.year - 1:
                    is_stale = True
        
        if is_stale:
            stale.append(indicator)
        else:
            fresh.append(indicator)
    
    return {
        "total_indicators": len(all_indicators),
        "stale_count": len(stale),
        "fresh_count": len(fresh),
        "stale_indicators": stale,
        "fresh_indicators": fresh,
        "by_category": {cat: len(items) for cat, items in by_cat.items()},
        "assessed_at": NOW.isoformat()
    }


def check_source_diversity(db_path: Path) -> dict:
    """Check how many distinct data sources are feeding the system."""
    conn = sqlite3.connect(str(db_path))
    try:
        rows = conn.execute("SELECT DISTINCT source FROM indicators").fetchall()
    finally:
        conn.close()
    
    sources = [r[0] for r in rows if r[0]]
    return {
        "source_count": len(sources),
        "sources": sources,
        "recommendation": "Consider adding more sources" if len(sources) < 10 else "Good diversity"
    }


# ---------------------------------------------------------------------------
# ENHANCED REFRESH — Integrates new sources with existing DB
# ---------------------------------------------------------------------------
def ensure_db_schema(db_path: Path):
    """Ensure the indicators and datasets tables exist."""
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            value TEXT,
            unit TEXT,
            category TEXT,
            source TEXT,
            source_url TEXT,
            vintage TEXT,
            description TEXT,
            fetched_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            content TEXT,
            fetched_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.commit()
    conn.close()


def upsert_indicator(name: str, value: str, unit: str, category: str,
                     source: str, source_url: str = "", vintage: str = "",
                     description: str = ""):
    """Insert or update an indicator row."""
    conn = sqlite3.connect(str(DB_PATH))
    try:
        conn.execute("""
            INSERT INTO indicators (name, value, unit, category, source, source_url, vintage, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                value=excluded.value, unit=excluded.unit, category=excluded.category,
                source=excluded.source, source_url=excluded.source_url,
                vintage=excluded.vintage, description=excluded.description,
                fetched_at=datetime('now','localtime')
        """, (name, value, unit, category, source, source_url, vintage, description))
        conn.commit()
    finally:
        conn.close()


def enhance_all():
    """Run all enhancements: new sources + quality monitoring."""
    ensure_db_schema(DB_PATH)
    
    print("=" * 60)
    print("PROJECT VOLUSIA — DATA SOURCE ENHANCEMENT v1")
    print("=" * 60)
    print()
    
    # --- 1. FRED API (replaces fragile HTML scraping) ---
    print("[1] FRED API Integration...")
    fred_data = fetch_fred_api(["FLVOLU7POP", "FLVOLU7URN", "FLVOLU7PCPI", "FLVOLU7NRMN"])
    if "series" in fred_data:
        series = fred_data["series"]
        if "FLVOLU7POP" in series:
            upsert_indicator("fred_population_api", str(series["FLVOLU7POP"]["value"]),
                           "persons", "Economic", fred_data["source"],
                           "https://fred.stlouisfed.org/series/FLVOLU7POP",
                           series["FLVOLU7POP"]["date"], "Volusia County population (FRED API)")
            print(f"    Population: {series['FLVOLU7POP']['value']:,.0f} ({series['FLVOLU7POP']['date']})")
        if "FLVOLU7URN" in series:
            upsert_indicator("fred_unemployment_api", str(series["FLVOLU7URN"]["value"]),
                           "percent", "Economic", fred_data["source"],
                           "https://fred.stlouisfed.org/series/FLVOLU7URN",
                           series["FLVOLU7URN"]["date"], "Volusia County unemployment rate (FRED API)")
            print(f"    Unemployment: {series['FLVOLU7URN']['value']}% ({series['FLVOLU7URN']['date']})")
        if "FLVOLU7PCPI" in series:
            upsert_indicator("fred_per_capita_income_api", str(series["FLVOLU7PCPI"]["value"]),
                           "USD", "Economic", fred_data["source"],
                           "https://fred.stlouisfed.org/series/FLVOLU7PCPI",
                           series["FLVOLU7PCPI"]["date"], "Per capita personal income (FRED API)")
            print(f"    Per capita income: ${series['FLVOLU7PCPI']['value']:,.0f}")
        if "FLVOLU7NRMN" in series:
            upsert_indicator("fred_nonfarm_employment_api", str(series["FLVOLU7NRMN"]["value"]),
                           "thousands", "Economic", fred_data["source"],
                           "https://fred.stlouisfed.org/series/FLVOLU7NRMN",
                           series["FLVOLU7NRMN"]["date"], "Nonfarm payroll employment in thousands (FRED API)")
            print(f"    Nonfarm employment: {series['FLVOLU7NRMN']['value']}K")
    else:
        print(f"    FRED: {fred_data.get('note', 'no data')}")
    
    print()
    
    # --- 2. Florida DEO ---
    print("[2] Florida DEO Labor Market...")
    deo_data = fetch_florida_deo()
    if deo_data:
        if "unemploymentRate" in deo_data:
            upsert_indicator("deo_unemployment_rate", str(deo_data["unemploymentRate"]),
                           "percent", "Economic", deo_data["source"],
                           deo_data["sourceUrl"], str(TODAY.year),
                           "Volusia County unemployment rate (FL DEO)")
            print(f"    Unemployment: {deo_data['unemploymentRate']}%")
        if "laborForce" in deo_data:
            upsert_indicator("deo_labor_force", str(deo_data["laborForce"]),
                           "persons", "Economic", deo_data["source"],
                           deo_data["sourceUrl"], str(TODAY.year),
                           "Volusia County labor force (FL DEO)")
            print(f"    Labor force: {deo_data['laborForce']:,}")
    else:
        print("    No DEO data available (page structure may have changed)")
    
    print()
    
    # --- 3. FDLE Crime ---
    print("[3] FDLE Crime Statistics...")
    crime_data = fetch_fdle_crime()
    if crime_data and "crimeRatePer100k" in crime_data:
        upsert_indicator("fdle_crime_rate", str(crime_data["crimeRatePer100k"]),
                       "per 100k", "Safety", crime_data["source"],
                       crime_data["sourceUrl"], str(TODAY.year),
                       "Volusia County crime rate per 100k population")
        print(f"    Crime rate: {crime_data['crimeRatePer100k']} per 100k")
    else:
        print("    No FDLE data available (page structure may have changed)")
    
    print()
    
    # --- 4. Florida CHARTS Health ---
    print("[4] Florida CHARTS Health Data...")
    charts_data = fetch_florida_charts()
    if charts_data:
        for key, val in charts_data.items():
            if key in ("source", "sourceUrl", "fetchedAt"):
                continue
            unit_map = {
                "uninsuredRate": "percent", "uninsuredRateAdult": "percent",
                "physiciansPer100k": "per 100k", "preventableHospitalizations": "per 100k",
                "lifeExpectancy": "years"
            }
            name_map = {
                "uninsuredRate": "charts_uninsured_rate",
                "uninsuredRateAdult": "charts_uninsured_adult_rate",
                "physiciansPer100k": "charts_physicians_per_100k",
                "preventableHospitalizations": "charts_preventable_hosp",
                "lifeExpectancy": "charts_life_expectancy"
            }
            upsert_indicator(name_map.get(key, key), str(val),
                           unit_map.get(key, "index"), "Health",
                           charts_data["source"], charts_data["sourceUrl"],
                           str(TODAY.year), f"Volusia County {key} (FL CHARTS)")
            print(f"    {key}: {val}")
    else:
        print("    No CHARTS data available (page structure may have changed)")
    
    print()
    
    # --- 5. Property Appraiser ---
    print("[5] Volusia County Property Appraiser...")
    prop_data = fetch_property_appraiser()
    if prop_data:
        if "totalParcels" in prop_data:
            upsert_indicator("property_total_parcels", str(prop_data["totalParcels"]),
                           "parcels", "Economic", prop_data["source"],
                           prop_data["sourceUrl"], str(TODAY.year),
                           "Total taxable parcels in Volusia County")
            print(f"    Total parcels: {prop_data['totalParcels']:,}")
        if "assessedValue" in prop_data:
            upsert_indicator("property_assessed_value", str(prop_data["assessedValue"]),
                           "USD", "Economic", prop_data["source"],
                           prop_data["sourceUrl"], str(TODAY.year),
                           "Total assessed property value in Volusia County")
            print(f"    Assessed value: ${prop_data['assessedValue']:,.0f}")
    else:
        print("    No property data available")
    
    print()
    
    # --- 6. Data Quality Report ---
    print("[6] Data Quality & Freshness Report...")
    freshness = get_data_freshness(DB_PATH)
    diversity = check_source_diversity(DB_PATH)
    
    print(f"    Total indicators: {freshness['total_indicators']}")
    print(f"    Fresh (< 1 yr): {freshness['fresh_count']}")
    print(f"    Stale (> 1 yr): {freshness['stale_count']}")
    print(f"    Source diversity: {diversity['source_count']} distinct sources")
    print(f"    Categories: {freshness['by_category']}")
    
    if freshness['stale_indicators']:
        print()
        print("    STALE INDICATORS (need attention):")
        for ind in freshness['stale_indicators']:
            print(f"      - {ind['name']}: vintage={ind.get('vintage', 'unknown')}")
    
    print()
    
    # --- 7. Write quality snapshot ---
    quality_snapshot = {
        "assessed_at": NOW.isoformat(),
        "freshness": {
            "total": freshness['total_indicators'],
            "fresh": freshness['fresh_count'],
            "stale": freshness['stale_count'],
            "stale_list": [{"name": i['name'], "vintage": i.get('vintage', '')} for i in freshness['stale_indicators']]
        },
        "diversity": diversity,
        "categories": freshness['by_category']
    }
    
    quality_path = CACHE_DIR / "data_quality.json"
    quality_path.write_text(json.dumps(quality_snapshot, indent=2))
    print(f"    Quality snapshot written to: {quality_path}")
    
    print()
    print("=" * 60)
    print("ENHANCEMENT COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    enhance_all()
