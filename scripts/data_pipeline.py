"""
Project Volusia — Data Pipeline v2
Fetches real economic indicators from public APIs with robust error handling.
Sources: Census ACS, BLS LAUS, BEA Personal Income.
"""

import os
import csv
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

# --- Configuration ---
DATA_DIR = Path(__file__).parent.parent / "data" / "cache"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Volusia County FIPS
STATE_FIPS = "12"
COUNTY_FIPS = "12127"

# API Keys (use environment variables or .env in production)
CENSUS_API_KEY = os.environ.get("CENSUS_API_KEY", "")
BLS_API_KEY = os.environ.get("BLS_API_KEY", "")
BEA_API_KEY = os.environ.get("BEA_API_KEY", "")

# Cache TTL (hours)
CACHE_TTL = 24


def cache_path(name: str) -> Path:
    return DATA_DIR / f"{name}.json"


def is_cache_fresh(path: Path) -> bool:
    if not path.exists():
        return False
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    return datetime.now() - mtime < timedelta(hours=CACHE_TTL)


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "ProjectVolusia/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode()
        if content.strip().startswith("<"):
            raise ValueError("API returned HTML (likely missing key or invalid request)")
        return json.loads(content)


# ============================================================
# CENSUS AMERICAN COMMUNITY SURVEY (ACS)
# ============================================================

def fetch_census_acs_dp03(year: int = 2024) -> dict:
    """
    Fetch ACS 5-Year DP03 (Economic Characteristics) for Volusia County.
    Tables: DP03_0062E (Median household income), DP03_0009PE (Unemployment rate)
    """
    base = f"https://api.census.gov/data/{year}/acs/acs5/profile"
    get_vars = "DP03_0062E,DP03_0009PE,DP03_0005PE,DP03_0119E,DP04_0134E"
    params = f"?get={get_vars}&for=county:{COUNTY_FIPS[2:]}&in=state:{STATE_FIPS}"
    if CENSUS_API_KEY:
        params += f"&key={CENSUS_API_KEY}"

    url = base + params
    data = http_get_json(url)

    # Parse: data[0] = headers, data[1] = values
    headers = data[0]
    values = data[1]
    result = dict(zip(headers, values))

    return {
        "source": "US Census ACS 5-Year DP03",
        "sourceUrl": "https://data.census.gov/",
        "vintage": f"{year}",
        "fetchedAt": datetime.now().isoformat(),
        "medianHouseholdIncome": int(result.get("DP03_0062E", 0)),
        "unemploymentRate": float(result.get("DP03_0009PE", 0)),
        "povertyRate": float(result.get("DP03_0005PE", 0)),
        "perCapitaIncome": int(result.get("DP03_0119E", 0)),
        "medianGrossRent": int(result.get("DP04_0134E", 0)),
    }


def fetch_census_acs_dp05(year: int = 2024) -> dict:
    """
    Fetch ACS 5-Year DP05 (Demographic) for Volusia County.
    Tables: DP05_0001PE (Total population %), DP05_0018E (Median age)
    """
    base = f"https://api.census.gov/data/{year}/acs/acs5/profile"
    get_vars = "DP05_0001PE,DP05_0018E,DP05_0024PE,DP05_0025PE"
    params = f"?get={get_vars}&for=county:{COUNTY_FIPS[2:]}&in=state:{STATE_FIPS}"
    if CENSUS_API_KEY:
        params += f"&key={CENSUS_API_KEY}"

    url = base + params
    data = http_get_json(url)

    headers = data[0]
    values = data[1]
    result = dict(zip(headers, values))

    return {
        "source": "US Census ACS 5-Year DP05",
        "sourceUrl": "https://data.census.gov/",
        "vintage": f"{year}",
        "fetchedAt": datetime.now().isoformat(),
        "totalPopulation": int(result.get("DP05_0001PE", 0)),
        "medianAge": float(result.get("DP05_0018E", 0)),
        "pctOver65": float(result.get("DP05_0024PE", 0)),
        "pctUnder18": float(result.get("DP05_0025PE", 0)),
    }


# ============================================================
# BUREAU OF LABOR STATISTICS (BLS) — LAUS
# ============================================================

def fetch_bls_laus(area_code: str = "FL12127") -> dict:
    """
    Fetch BLS Local Area Unemployment Statistics for Volusia County.
    """
    series_ids = [
        f"LAUCN{area_code}000000003",  # Unemployment rate
        f"LAUCN{area_code}000000004",  # Unemployment level
        f"LAUCN{area_code}000000005",  # Employment level
        f"LAUCN{area_code}000000006",  # Labor force level
    ]

    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {"Content-Type": "application/json", "User-Agent": "ProjectVolusia/1.0"}
    payload = {
        "seriesid": series_ids,
        "startyear": str(datetime.now().year - 2),
        "endyear": str(datetime.now().year),
    }
    if BLS_API_KEY:
        payload["registrationkey"] = BLS_API_KEY

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())

    if data.get("status") != "REQUEST_SUCCEEDED":
        raise ValueError(f"BLS API error: {data.get('message', [data.get('status')])[0]}")

    results = {}
    for series in data.get("Results", {}).get("series", []):
        sid = series["seriesID"]
        latest = series["data"][0] if series["data"] else None
        if latest:
            if sid.endswith("000000003"):
                results["unemploymentRate"] = float(latest["value"])
            elif sid.endswith("000000004"):
                results["unemploymentLevel"] = int(latest["value"])
            elif sid.endswith("000000005"):
                results["employmentLevel"] = int(latest["value"])
            elif sid.endswith("000000006"):
                results["laborForceLevel"] = int(latest["value"])
            results["period"] = latest.get("periodName", "")
            results["year"] = latest.get("year", "")

    return {
        "source": "BLS Local Area Unemployment Statistics",
        "sourceUrl": "https://www.bls.gov/lau/",
        "vintage": f"{results.get('year', '')}-{results.get('period', '')}",
        "fetchedAt": datetime.now().isoformat(),
        **results,
    }


# ============================================================
# BUREAU OF ECONOMIC ANALYSIS (BEA) — Personal Income
# ============================================================

def fetch_bea_personal_income(year: int = 2024) -> dict:
    """
    Fetch BEA Local Area Personal Income (CAINC1) for Volusia County.
    """
    table_name = "CAINC1"
    line_code = "10"
    geo_fips = f"{STATE_FIPS}{COUNTY_FIPS[2:]}"

    url = (
        f"https://apps.bea.gov/api/data/"
        f"?UserID={BEA_API_KEY}"
        f"&method=GetData"
        f"&datasetname=Regional"
        f"&TableName={table_name}"
        f"&LineCode={line_code}"
        f"&GeoFIPS={geo_fips}"
        f"&Year=ALL"
        f"&ResultFormat=JSON"
    )

    if not BEA_API_KEY:
        return {
            "source": "BEA Local Area Personal Income",
            "sourceUrl": "https://www.bea.gov/data/income-saving/local-area-personal-income",
            "vintage": str(year),
            "fetchedAt": datetime.now().isoformat(),
            "note": "BEA_API_KEY not set — returning empty result",
        }

    data = http_get_json(url)

    results = []
    for item in data.get("BEAAPI", {}).get("Results", {}).get("Data", []):
        results.append({
            "year": item.get("TimePeriod"),
            "personalIncomeThousands": int(item.get("DataValue", "0").replace(",", "")),
        })

    latest = max(results, key=lambda x: x["year"]) if results else {}

    return {
        "source": "BEA Local Area Personal Income (CAINC1)",
        "sourceUrl": "https://www.bea.gov/data/income-saving/local-area-personal-income",
        "vintage": latest.get("year", str(year)),
        "fetchedAt": datetime.now().isoformat(),
        "personalIncomeThousands": latest.get("personalIncomeThousands", 0),
        "personalIncomeMillions": round(latest.get("personalIncomeThousands", 0) / 1000, 1),
        "history": results[-5:] if len(results) > 5 else results,
    }


# ============================================================
# ORCHESTRATOR
# ============================================================

def run_pipeline() -> dict:
    """Run all fetchers and cache results."""
    results = {}

    # Census ACS DP03
    try:
        path = cache_path("census_dp03")
        if is_cache_fresh(path):
            results["census_dp03"] = json.loads(path.read_text())
        else:
            data = fetch_census_acs_dp03()
            path.write_text(json.dumps(data, indent=2))
            results["census_dp03"] = data
    except Exception as e:
        results["census_dp03"] = {"error": str(e)}

    # Census ACS DP05
    try:
        path = cache_path("census_dp05")
        if is_cache_fresh(path):
            results["census_dp05"] = json.loads(path.read_text())
        else:
            data = fetch_census_acs_dp05()
            path.write_text(json.dumps(data, indent=2))
            results["census_dp05"] = data
    except Exception as e:
        results["census_dp05"] = {"error": str(e)}

    # BLS LAUS
    try:
        path = cache_path("bls_laus")
        if is_cache_fresh(path):
            results["bls_laus"] = json.loads(path.read_text())
        else:
            data = fetch_bls_laus()
            path.write_text(json.dumps(data, indent=2))
            results["bls_laus"] = data
    except Exception as e:
        results["bls_laus"] = {"error": str(e)}

    # BEA Personal Income
    try:
        path = cache_path("bea_income")
        if is_cache_fresh(path):
            results["bea_income"] = json.loads(path.read_text())
        else:
            data = fetch_bea_personal_income()
            path.write_text(json.dumps(data, indent=2))
            results["bea_income"] = data
    except Exception as e:
        results["bea_income"] = {"error": str(e)}

    return results


def check_api_keys() -> dict:
    """Check which API keys are configured."""
    return {
        "CENSUS_API_KEY": "SET" if CENSUS_API_KEY else "NOT SET",
        "BLS_API_KEY": "SET" if BLS_API_KEY else "NOT SET",
        "BEA_API_KEY": "SET" if BEA_API_KEY else "NOT SET",
    }


if __name__ == "__main__":
    print("Project Volusia — Data Pipeline")
    print("=" * 40)
    print()
    print("API Key Status:")
    for key, status in check_api_keys().items():
        print(f"  {key}: {status}")
    print()
    print("Running pipeline...")
    results = run_pipeline()
    for name, data in results.items():
        if "error" in data:
            print(f"  ✗ {name}: {data['error']}")
        else:
            print(f"  ✓ {name}: vintage={data.get('vintage', '?')}")
    print()
    print("Done.")
