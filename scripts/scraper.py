"""
Project Volusia — Unified Data Scraper
Fetches real data from all accessible sources for Volusia County, Florida.
"""

import json
import csv
import re
import io
import time
import hashlib
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List
import xml.etree.ElementTree as ET

# --- Configuration ---
PROJECT_DIR = Path(__file__).parent.parent
CACHE_DIR = PROJECT_DIR / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

STATE_FIPS = "12"
COUNTY_FIPS = "12127"
COUNTY_CODE = "127"  # Last 3 digits

CACHE_TTL = {
    "census": 24 * 7,  # Weekly
    "bls": 24 * 7,
    "bea": 24 * 7,
    "noaa": 24,  # Daily
    "weather_forecast": 1,  # Hourly
    "fred": 24 * 7,
    "redfin": 24,
    "volusia_business": 24 * 7,
    "zillow": 24 * 7,
    "quickfacts": 24 * 7,
    "volusia_gis": 24 * 7,
}


# --- Cache Helpers ---

def cache_path(name: str) -> Path:
    return CACHE_DIR / f"{name}.json"


def is_cache_fresh(name: str, ttl_hours: int = 24) -> bool:
    path = cache_path(name)
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text())
        fetched = data.get("fetchedAt", "")
        if fetched:
            dt = datetime.fromisoformat(fetched.replace("Z", "+00:00").replace("+00:00", ""))
            return datetime.now() - dt < timedelta(hours=ttl_hours)
    except Exception:
        pass
    return False


def fetch_url(url: str, timeout: int = 30) -> Optional[str]:
    """Fetch URL content with proper headers."""
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None


def fetch_json(url: str, timeout: int = 30) -> Optional[dict]:
    """Fetch JSON from URL."""
    content = fetch_url(url, timeout)
    if content:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return None
    return None


# --- Census Bureau ---

def scrape_census_dp03(year: int = 2023) -> Optional[dict]:
    """Fetch ACS 5-Year DP03 (Economic Characteristics) via data.census.gov."""
    path = cache_path("census_dp03")
    if is_cache_fresh("census_dp03", CACHE_TTL["census"]):
        return json.loads(path.read_text())

    url = f"https://data.census.gov/api/access/data/table?g=0500000US{COUNTY_FIPS}&tid=ACSDP5Y{year}.DP03"
    data = fetch_json(url)
    if not data or "response" not in data:
        return None

    rows = data["response"].get("data", [])
    if len(rows) < 2:
        return None

    headers = rows[0]
    values = rows[1]
    result = dict(zip(headers, values))

    output = {
        "source": "US Census ACS 5-Year DP03",
        "sourceUrl": url,
        "vintage": str(year),
        "fetchedAt": datetime.now().isoformat(),
        "medianHouseholdIncome": parse_int(result.get("DP03_0062E")),
        "medianHouseholdIncomeMoe": parse_int(result.get("DP03_0062M")),
        "unemploymentRate": parse_float(result.get("DP03_0009PE")),
        "povertyRate": parse_float(result.get("DP03_0005PE")),
        "perCapitaIncome": parse_int(result.get("DP03_0119E")),
        "medianGrossRent": parse_int(result.get("DP04_0134E")),
        "medianMortgage": parse_int(result.get("DP04_0089E")),
        "ownerOccupiedHousing": parse_int(result.get("DP04_0046E")),
        "renterOccupiedHousing": parse_int(result.get("DP04_0047E")),
        "commuteTimeMinutes": parse_float(result.get("DP03_0025E")),
        "healthInsuranceRate": parse_float(result.get("DP03_0099PE")),
    }

    path.write_text(json.dumps(output, indent=2))
    return output


def scrape_census_dp05(year: int = 2023) -> Optional[dict]:
    """Fetch ACS 5-Year DP05 (Demographics) via data.census.gov."""
    path = cache_path("census_dp05")
    if is_cache_fresh("census_dp05", CACHE_TTL["census"]):
        return json.loads(path.read_text())

    url = f"https://data.census.gov/api/access/data/table?g=0500000US{COUNTY_FIPS}&tid=ACSDP5Y{year}.DP05"
    data = fetch_json(url)
    if not data or "response" not in data:
        return None

    rows = data["response"].get("data", [])
    if len(rows) < 2:
        return None

    headers = rows[0]
    values = rows[1]
    result = dict(zip(headers, values))

    # Census DP05 data structure:
    # E = Estimate (count), PE = Percentage estimate, M = Margin of error
    # Some PE fields may return counts if percentage is not available
    
    total_pop = parse_int(result.get("DP05_0001E"))
    
    output = {
        "source": "US Census ACS 5-Year DP05",
        "sourceUrl": url,
        "vintage": str(year),
        "fetchedAt": datetime.now().isoformat(),
        "totalPopulation": total_pop,
        "medianAge": parse_float(result.get("DP05_0018E")),
        "pctUnder5": parse_float(result.get("DP05_0005PE")),
        # DP05_0006PE may be under 18 or 5-17 depending on table version
        "pctUnder18": parse_float(result.get("DP05_0006PE")) or (
            round(parse_int(result.get("DP05_0006E")) / total_pop * 100, 1) if total_pop else None
        ),
        "pctOver65": parse_float(result.get("DP05_0024PE")),
        # Race percentages - use PE fields directly
        "pctWhiteAlone": parse_float(result.get("DP05_0082PE")),
        "pctBlackAlone": parse_float(result.get("DP05_0080PE")),
        "pctAsianAlone": parse_float(result.get("DP05_0035PE")),
        "pctHispanicLatino": parse_float(result.get("DP05_0114PE")),
        "pctVeteran": parse_float(result.get("DP05_0095PE")),
        "pctForeignBorn": parse_float(result.get("DP05_0111PE")),
        "pctBachelorsOrHigher": parse_float(result.get("DP05_0067PE")),
    }

    path.write_text(json.dumps(output, indent=2))
    return output

    path.write_text(json.dumps(output, indent=2))
    return output


def scrape_census_quickfacts() -> Optional[dict]:
    """Scrape Census QuickFacts page for Volusia County."""
    path = cache_path("census_quickfacts")
    if is_cache_fresh("census_quickfacts", CACHE_TTL["quickfacts"]):
        return json.loads(path.read_text())

    url = "https://www.census.gov/quickfacts/fact/table/volusiacountyflorida/PST045225"
    content = fetch_url(url)
    if not content:
        return None

    # Extract data using regex patterns
    result = {
        "source": "US Census QuickFacts",
        "sourceUrl": url,
        "vintage": "2025",
        "fetchedAt": datetime.now().isoformat(),
    }

    # Population estimates
    pop_match = re.search(r'Population estimates, July 1, 2024[^<]*<[^>]*>([^<]+)<', content)
    if pop_match:
        result["population2024"] = clean_number(pop_match.group(1))

    # Population change
    change_match = re.search(r'Population, Census, April 1, 2020[^<]*<[^>]*>([^<]+)<', content)
    if change_match:
        result["population2020"] = clean_number(change_match.group(1))

    # Median household income
    income_match = re.search(r'Median household income[^,]*,[^,]*, 2019-2023[^<]*<[^>]*>([^<]+)<', content)
    if income_match:
        result["medianIncome"] = clean_number(income_match.group(1))

    # Per capita income
    pc_income_match = re.search(r'Per capita income in past 12 months[^,]*,[^,]*, 2019-2023[^<]*<[^>]*>([^<]+)<', content)
    if pc_income_match:
        result["perCapitaIncome"] = clean_number(pc_income_match.group(1))

    path.write_text(json.dumps(result, indent=2))
    return result


# --- NOAA Weather ---

def scrape_noaa_daily(start_date: str = None, end_date: str = None) -> Optional[dict]:
    """Fetch daily weather summaries from NOAA NCEI."""
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    cache_name = f"noaa_daily_{start_date}_{end_date}"
    path = cache_path(cache_name)
    if is_cache_fresh(cache_name, CACHE_TTL["noaa"]):
        return json.loads(path.read_text())

    url = (
        f"https://www.ncei.noaa.gov/access/services/data/v1?"
        f"dataset=daily-summaries&dataTypes=TMAX,TMIN,PRCP,AWND,SNOW,SNWD"
        f"&stations=USW00012838&startDate={start_date}&endDate={end_date}&format=json"
    )

    data = fetch_json(url)
    if not data or not isinstance(data, list):
        return None

    # Process: convert tenths units to actual values
    processed = []
    for row in data:
        processed.append({
            "date": row.get("DATE"),
            "tmax_f": tenths_to_fahrenheit(row.get("TMAX")),
            "tmin_f": tenths_to_fahrenheit(row.get("TMIN")),
            "prcp_in": tenths_to_inches(row.get("PRCP")),
            "awnd_mph": tenths_to_mph(row.get("AWND")),
            "snow_in": tenths_to_inches(row.get("SNOW")),
        })

    output = {
        "source": "NOAA NCEI Daily Summaries",
        "station": "USW00012838",
        "stationName": "Daytona Beach International Airport",
        "sourceUrl": url,
        "vintage": f"{start_date} to {end_date}",
        "fetchedAt": datetime.now().isoformat(),
        "data": processed,
        "summary": {
            "recordCount": len(processed),
            "avgHigh": avg([r["tmax_f"] for r in processed if r["tmax_f"] is not None]),
            "avgLow": avg([r["tmin_f"] for r in processed if r["tmin_f"] is not None]),
            "totalPrecip": sum([r["prcp_in"] or 0 for r in processed]),
        },
    }

    path.write_text(json.dumps(output, indent=2))
    return output


def scrape_open_meteo_forecast() -> Optional[dict]:
    """Fetch weather forecast from Open-Meteo (no API key needed)."""
    path = cache_path("open_meteo_forecast")
    if is_cache_fresh("open_meteo_forecast", CACHE_TTL["weather_forecast"]):
        return json.loads(path.read_text())

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=29.21&longitude=-81.02"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode,windspeed_10m_max,uv_index_max"
        "&current_weather=true&timezone=America%2FNew_York&forecast_days=14"
    )

    data = fetch_json(url, timeout=30)
    if not data:
        return None

    current = data.get("current_weather", {})
    daily = data.get("daily", {})

    output = {
        "source": "Open-Meteo",
        "sourceUrl": "https://open-meteo.com/",
        "station": "Daytona Beach, FL (29.21°N, 81.02°W)",
        "fetchedAt": datetime.now().isoformat(),
        "current": {
            "temperature_f": celsius_to_fahrenheit(current.get("temperature")),
            "windspeed_mph": current.get("windspeed"),
            "weathercode": current.get("weathercode"),
            "is_day": current.get("is_day"),
        },
        "forecast": [
            {
                "date": daily["time"][i] if i < len(daily.get("time", [])) else None,
                "temp_max_f": celsius_to_fahrenheit(daily["temperature_2m_max"][i]) if i < len(daily.get("temperature_2m_max", [])) else None,
                "temp_min_f": celsius_to_fahrenheit(daily["temperature_2m_min"][i]) if i < len(daily.get("temperature_2m_min", [])) else None,
                "precipitation_in": daily["precipitation_sum"][i] / 25.4 if i < len(daily.get("precipitation_sum", [])) else None,
                "weathercode": daily["weathercode"][i] if i < len(daily.get("weathercode", [])) else None,
            }
            for i in range(len(daily.get("time", [])))
        ],
    }

    path.write_text(json.dumps(output, indent=2))
    return output


# --- Redfin / Real Estate ---

def scrape_redfin_volusia() -> Optional[dict]:
    """Scrape Redfin Volusia County housing market data."""
    path = cache_path("redfin_volusia")
    if is_cache_fresh("redfin_volusia", CACHE_TTL["redfin"]):
        return json.loads(path.read_text())

    url = "https://www.redfin.com/county/500/FL/Volusia-County/housing-market"
    content = fetch_url(url)
    if not content:
        return None

    result = {
        "source": "Redfin",
        "sourceUrl": url,
        "vintage": datetime.now().strftime("%Y-%m"),
        "fetchedAt": datetime.now().isoformat(),
    }

    # Median sale price - try multiple patterns
    # Pattern 1: $349K
    median_match = re.search(r'median sale price[^$]*\$([\d,]+)\s*K', content, re.IGNORECASE)
    if median_match:
        result["medianSalePrice"] = int(float(median_match.group(1).replace(",", "")) * 1000)
    
    # Pattern 2: $349,000
    if not result.get("medianSalePrice"):
        median_match = re.search(r'median sale price[^$]*\$([\d,]+(?:,\d{3})+)', content, re.IGNORECASE)
        if median_match:
            result["medianSalePrice"] = int(median_match.group(1).replace(",", ""))

    # Pattern 3: Just numbers after "median sale price"
    if not result.get("medianSalePrice"):
        median_match = re.search(r'median sale price[^0-9]*([\d,]+)', content, re.IGNORECASE)
        if median_match:
            val = int(median_match.group(1).replace(",", ""))
            result["medianSalePrice"] = val * 1000 if val < 10000 else val

    # Price change YoY
    yoy_match = re.search(r'(up|down)\s*([\d.]+)%?\s*(year-over-year|since last year)', content, re.IGNORECASE)
    if yoy_match:
        direction = 1 if yoy_match.group(1).lower() == "up" else -1
        result["yoyPriceChange"] = direction * float(yoy_match.group(2))

    path.write_text(json.dumps(result, indent=2))
    return result


# --- Volusia Business / Economic Development ---

def scrape_volusia_business() -> Optional[dict]:
    """Scrape VolusiaBusiness.org for economic data."""
    path = cache_path("volusia_business")
    if is_cache_fresh("volusia_business", CACHE_TTL["volusia_business"]):
        return json.loads(path.read_text())

    url = "https://www.volusiabusiness.org/research-center/economy.stml"
    content = fetch_url(url)
    if not content:
        return None

    result = {
        "source": "Volusia Business",
        "sourceUrl": url,
        "fetchedAt": datetime.now().isoformat(),
    }

    # GDP
    gdp_match = re.search(r'GDP[^$]*\$([\d.]+)\s*(billion|trillion)', content, re.IGNORECASE)
    if gdp_match:
        multiplier = 1e9 if gdp_match.group(2).lower() == "billion" else 1e12
        result["gdp"] = float(gdp_match.group(1)) * multiplier

    # GDP rank
    rank_match = re.search(r'ranked\s*(\d+)(?:st|nd|rd|th)\s*out of\s*(\d+)', content, re.IGNORECASE)
    if rank_match:
        result["gdpRank"] = int(rank_match.group(1))
        result["gdpRankTotal"] = int(rank_match.group(2))

    path.write_text(json.dumps(result, indent=2))
    return result


# --- Zillow Metro Data ---

def scrape_zillow_metro_zhvi() -> Optional[dict]:
    """Download Zillow metro-level ZHVI data."""
    path = cache_path("zillow_zhvi")
    if is_cache_fresh("zillow_zhvi", CACHE_TTL["zillow"]):
        return json.loads(path.read_text())

    url = "https://files.zillowstatic.com/research/public_csvs/zhvi/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
    content = fetch_url(url)
    if not content:
        return None

    reader = csv.DictReader(io.StringIO(content))
    daytona_row = None
    for row in reader:
        if "Daytona" in row.get("Metro", "") or "Deltona" in row.get("Metro", ""):
            daytona_row = row
            break

    if not daytona_row:
        return None

    # Get latest value and historical
    dates = [k for k in daytona_row.keys() if re.match(r"\d{4}-\d{2}-\d{2}", k)]
    latest_date = max(dates)
    latest_value = float(daytona_row[latest_date])

    # Get year ago
    year_ago_date = (datetime.strptime(latest_date, "%Y-%m-%d") - timedelta(days=365)).strftime("%Y-%m-%d")
    year_ago_value = None
    for d in sorted(dates, reverse=True):
        if d <= year_ago_date:
            year_ago_value = float(daytona_row[d])
            break

    yoy_change = None
    if year_ago_value and latest_value:
        yoy_change = round((latest_value - year_ago_value) / year_ago_value * 100, 1)

    output = {
        "source": "Zillow ZHVI (Metro)",
        "sourceUrl": url,
        "metro": daytona_row.get("Metro"),
        "vintage": latest_date,
        "fetchedAt": datetime.now().isoformat(),
        "medianHomeValue": int(latest_value),
        "yoyChange": yoy_change,
        "history": [
            {"date": d, "value": float(daytona_row[d])}
            for d in sorted(dates[-24:])  # Last 24 months
        ],
    }

    path.write_text(json.dumps(output, indent=2))
    return output


# --- FRED Economic Data ---

def scrape_fred_series(series_id: str) -> Optional[dict]:
    """Scrape FRED HTML page for a series (no API key needed)."""
    path = cache_path(f"fred_{series_id}")
    if is_cache_fresh(f"fred_{series_id}", CACHE_TTL["fred"]):
        return json.loads(path.read_text())

    url = f"https://fred.stlouisfed.org/series/{series_id}"
    content = fetch_url(url)
    if not content:
        return None

    result = {
        "source": f"FRED Series: {series_id}",
        "sourceUrl": url,
        "fetchedAt": datetime.now().isoformat(),
    }

    # Try to find observation data in page
    obs_match = re.findall(r'<td class="series-obs">.*?</td>', content, re.DOTALL)
    if obs_match:
        # Extract most recent observation
        latest = obs_match[0]
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', latest)
        val_match = re.search(r'([\d,]+\.?\d*)', latest)
        if date_match and val_match:
            result["latestDate"] = date_match.group(1)
            result["latestValue"] = float(val_match.group(1).replace(",", ""))

    path.write_text(json.dumps(result, indent=2))
    return result


# --- Volusia County GIS ---

def scrape_volusia_gis_data() -> Optional[dict]:
    """Scrape Volusia GIS data download page for available datasets."""
    path = cache_path("volusia_gis")
    if is_cache_fresh("volusia_gis", CACHE_TTL["volusia_gis"]):
        return json.loads(path.read_text())

    url = "https://www.volusia.org/services/financial-and-administrative-services/finance-department/information-technology/geographic-information-services/data/download-data.stml"
    content = fetch_url(url)
    if not content:
        return None

    # Extract download links
    links = re.findall(r'href="([^"]+\.(?:zip|csv|kml|geojson|shp|gdb))"', content, re.IGNORECASE)

    output = {
        "source": "Volusia County GIS",
        "sourceUrl": url,
        "fetchedAt": datetime.now().isoformat(),
        "availableDatasets": links[:20],
    }

    path.write_text(json.dumps(output, indent=2))
    return output


# --- Helpers ---

def parse_int(value) -> Optional[int]:
    if value is None:
        return None
    s = str(value).replace(",", "").replace("+", "").replace("-", "").strip()
    if not s or s in ("888888888", "999999999", "(X)", "null", "N/A", "**", "***"):
        return None
    try:
        return int(s)
    except (ValueError, TypeError):
        return None


def parse_float(value) -> Optional[float]:
    if value is None:
        return None
    s = str(value).replace(",", "").replace("%", "").strip()
    if not s or s in ("888888888", "999999999", "(X)", "null", "N/A", "**", "***"):
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def clean_number(s: str) -> Optional[int]:
    if not s:
        return None
    try:
        return int(re.sub(r"[^\d]", "", s))
    except ValueError:
        return None


def tenths_to_fahrenheit(value) -> Optional[float]:
    if value is None:
        return None
    try:
        return round(int(value) / 10 * 9 / 5 + 32, 1)
    except (ValueError, TypeError):
        return None


def tenths_to_celsius(value) -> Optional[float]:
    if value is None:
        return None
    try:
        return round(int(value) / 10, 1)
    except (ValueError, TypeError):
        return None


def tenths_to_inches(value) -> Optional[float]:
    if value is None:
        return None
    try:
        return round(int(value) / 10 / 25.4, 2)  # mm to inches
    except (ValueError, TypeError):
        return None


def tenths_to_mph(value) -> Optional[float]:
    if value is None:
        return None
    try:
        return round(int(value) / 10 * 2.237, 1)  # m/s to mph
    except (ValueError, TypeError):
        return None


def celsius_to_fahrenheit(c) -> Optional[float]:
    if c is None:
        return None
    try:
        return round(c * 9 / 5 + 32, 1)
    except (ValueError, TypeError):
        return None


def avg(values: list) -> Optional[float]:
    vals = [v for v in values if v is not None]
    if not vals:
        return None
    return round(sum(vals) / len(vals), 1)


# --- Orchestrator ---

def run_all_scrapers() -> dict:
    """Run all scrapers and return results."""
    results = {}

    print("Scraping Census DP03...")
    results["census_dp03"] = scrape_census_dp03()

    print("Scraping Census DP05...")
    results["census_dp05"] = scrape_census_dp05()

    print("Scraping Census QuickFacts...")
    results["census_quickfacts"] = scrape_census_quickfacts()

    print("Scraping NOAA Daily Weather...")
    results["noaa_daily"] = scrape_noaa_daily()

    print("Scraping Open-Meteo Forecast...")
    results["open_meteo"] = scrape_open_meteo_forecast()

    print("Scraping Redfin...")
    results["redfin"] = scrape_redfin_volusia()

    print("Scraping Volusia Business...")
    results["volusia_business"] = scrape_volusia_business()

    print("Scraping Zillow Metro ZHVI...")
    results["zillow_zhvi"] = scrape_zillow_metro_zhvi()

    print("Scraping FRED Population...")
    results["fred_population"] = scrape_fred_series("FLVOLU7POP")

    print("Scraping FRED Unemployment...")
    results["fred_unemployment"] = scrape_fred_series("FLVOLU7URN")

    print("Scraping Volusia GIS...")
    results["volusia_gis"] = scrape_volusia_gis_data()

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("Project Volusia — Unified Data Scraper")
    print("=" * 60)
    print()

    results = run_all_scrapers()

    print()
    print("Results:")
    for name, data in results.items():
        if data:
            print(f"  ✓ {name}: {data.get('source', 'N/A')}")
        else:
            print(f"  ✗ {name}: Failed")

    print()
    print("Done.")
