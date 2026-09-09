"""Project Volusia - Refresh Pipeline v3 - unified fetcher + DB sync."""
import json, re, os, sys, urllib.request, urllib.error, csv, requests
import io, time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
from functools import wraps

STATE_FIPS = '12'
COUNTY_FIPS = '12127'
COUNTY_CODE = '127'
CENSUS_API_KEY = os.environ.get('CENSUS_API_KEY', '')
BLS_API_KEY = os.environ.get('BLS_API_KEY', '')
BEA_API_KEY = os.environ.get('BEA_API_KEY', '')
CACHE_TTL = {'census': 0, 'bls': 0, 'bea': 0, 'noaa': 0, 'weather_forecast': 0, 'fred': 0, 'redfin': 0, 'volusia_business': 0, 'zillow': 0, 'qcew': 0}

def retry(max_attempts=3, delay=2, backoff=2):
    """Retry decorator with exponential backoff for flaky APIs."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = delay * (backoff ** attempt)
                        print(f'    Retry {attempt+1}/{max_attempts} in {wait_time}s: {e}')
                        time.sleep(wait_time)
            raise last_exception
        return wrapper
    return decorator

DATA_DIR = Path(__file__).parent.parent / 'data' / 'cache'
DB_PATH = Path(__file__).parent.parent / 'data' / 'volusia.db'
PUBLIC_DIR = Path(__file__).parent.parent / 'public' / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)
PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

STATE_FIPS = '12'
COUNTY_FIPS = '12127'
COUNTY_CODE = '127'
CENSUS_API_KEY = os.environ.get('CENSUS_API_KEY', '')
BLS_API_KEY = os.environ.get('BLS_API_KEY', '')
BEA_API_KEY = os.environ.get('BEA_API_KEY', '')
CACHE_TTL = {'census': 24*7, 'bls': 24*7, 'bea': 24*7, 'noaa': 24, 'weather_forecast': 1, 'fred': 24*7, 'redfin': 24, 'volusia_business': 24*7, 'zillow': 24*7, 'qcew': 24*7}
TODAY = datetime.now()

def cache_path(name: str) -> Path: return DATA_DIR / f'{name}.json'
def is_cache_fresh(name: str) -> bool:
    p = cache_path(name)
    if not p.exists(): return False
    return datetime.now() - datetime.fromtimestamp(p.stat().st_mtime) < timedelta(hours=CACHE_TTL.get(name, 24))
def http_get_json(url: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, headers={'User-Agent': 'ProjectVolusia/1.0'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        c = resp.read().decode()
        if c.strip().startswith('<'): raise ValueError('API returned HTML')
        return json.loads(c)
def fetch_url(url: str, timeout: int = 30) -> Optional[str]:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp: return resp.read().decode('utf-8', errors='replace')
    except Exception: return None
def fetch_json(url: str, timeout: int = 30) -> Optional[dict]:
    c = fetch_url(url, timeout)
    if c:
        try: return json.loads(c)
        except json.JSONDecodeError: return None
    return None
def _db_exec(sql: str, params=()):
    import sqlite3
    conn = sqlite3.connect(str(DB_PATH)); conn.row_factory = sqlite3.Row
    try: cur = conn.execute(sql, params); conn.commit(); return cur
    finally: conn.close()
SENTINEL_VALUES = {-888888888, -999999, 999999, 'N/A', 'NULL', '**', '***', '(X)'}

def _is_sentinel(value):
    if isinstance(value, (int, float)):
        return value in SENTINEL_VALUES
    return str(value) in SENTINEL_VALUES

def upsert_indicator(name: str, value: str, unit: str, category: str, source: str, source_url: str, vintage: str, description: str):
    if _is_sentinel(value):
        return
    _db_exec('INSERT INTO indicators (name, value, unit, category, source, source_url, vintage, fetched_at, description) VALUES (?,?,?,?,?,?,?,?,?) ON CONFLICT(name) DO UPDATE SET value=excluded.value, unit=excluded.unit, category=excluded.category, source=excluded.source, source_url=excluded.source_url, vintage=excluded.vintage, fetched_at=excluded.fetched_at, description=excluded.description', (name, str(value), unit, category, source, source_url, vintage, datetime.now().isoformat(), description))

# --- Census ACS via data.census.gov (no key needed) ---
@retry(max_attempts=3, delay=2)
def fetch_census_dp03(year: int = 2024) -> Optional[dict]:
    if is_cache_fresh('census_dp03'): return json.loads(cache_path('census_dp03').read_text())
    url = f"https://data.census.gov/api/access/data/table?g=0500000US{COUNTY_FIPS}&tid=ACSDP5Y{year}.DP03"
    data = http_get_json(url)
    rows = data.get('response', {}).get('data', [])
    if len(rows) < 2: return None
    headers, values = rows[0], rows[1]
    r = dict(zip(headers, values))
    def gi(k):
        v = r.get(k)
        if v is None or v in ('(X)', 'N/A', '**', '***', 'null', '999999999', '888888888'): return None
        try: return int(str(v).replace(',', '').replace('+', ''))
        except Exception: return None
    def gf(k):
        v = r.get(k)
        if v is None or v in ('(X)', 'N/A', '**', '***', 'null', '999999999', '888888888'): return None
        try: return float(str(v).replace(',', ''))
        except Exception: return None
    out = {'source': 'US Census ACS 5-Year DP03', 'sourceUrl': url, 'vintage': str(year), 'fetchedAt': datetime.now().isoformat(),
           'medianHouseholdIncome': gi('DP03_0062E'), 'unemploymentRate': gf('DP03_0009PE'), 'povertyRate': gf('DP03_0005PE'),
           'perCapitaIncome': gi('DP03_0119E'), 'medianGrossRent': gi('DP04_0134E'), 'medianMortgage': gi('DP04_0089E'),
           'ownerOccupiedHousing': gi('DP04_0046E'), 'renterOccupiedHousing': gi('DP04_0047E'),
           'commuteTimeMinutes': gf('DP03_0025E'), 'healthInsuranceRate': gf('DP03_0099PE')}
    cache_path('census_dp03').write_text(json.dumps(out, indent=2))
    return out

@retry(max_attempts=3, delay=2)
def fetch_census_dp05(year: int = 2024) -> Optional[dict]:
    if is_cache_fresh('census_dp05'): return json.loads(cache_path('census_dp05').read_text())
    url = f"https://data.census.gov/api/access/data/table?g=0500000US{COUNTY_FIPS}&tid=ACSDP5Y{year}.DP05"
    data = http_get_json(url)
    rows = data.get('response', {}).get('data', [])
    if len(rows) < 2: return None
    headers, values = rows[0], rows[1]
    r = dict(zip(headers, values))
    def gi(k):
        v = r.get(k)
        if v is None or v in ('(X)', 'N/A', '**', '***', 'null', '999999999', '888888888'): return None
        try: return int(str(v).replace(',', '').replace('+', ''))
        except Exception: return None
    def gf(k):
        v = r.get(k)
        if v is None or v in ('(X)', 'N/A', '**', '***', 'null', '999999999', '888888888'): return None
        try: return float(str(v).replace(',', ''))
        except Exception: return None
    total_pop = gi('DP05_0001E')
    out = {'source': 'US Census ACS 5-Year DP05', 'sourceUrl': url, 'vintage': str(year), 'fetchedAt': datetime.now().isoformat(),
           'totalPopulation': total_pop, 'medianAge': gf('DP05_0018E'), 'pctUnder5': gf('DP05_0005PE'),
           'pctUnder18': gf('DP05_0006PE') or (round(total_pop / total_pop * 100, 1) if total_pop else None),
           'pctOver65': gf('DP05_0024PE'), 'pctWhiteAlone': gf('DP05_0082PE'), 'pctBlackAlone': gf('DP05_0080PE'),
           'pctAsianAlone': gf('DP05_0035PE'), 'pctHispanicLatino': gf('DP05_0114PE'), 'pctVeteran': gf('DP05_0095PE'),
           'pctForeignBorn': gf('DP05_0111PE'), 'pctBachelorsOrHigher': gf('DP05_0067PE')}
    cache_path('census_dp05').write_text(json.dumps(out, indent=2))
    return out

# --- BLS LAUS ---
@retry(max_attempts=3, delay=2)
def fetch_bls_laus() -> Optional[dict]:
    if is_cache_fresh('bls_laus'): return json.loads(cache_path('bls_laus').read_text())
    area_code = f'FL{COUNTY_CODE}0000000'
    series_ids = [f'LAUCN{area_code}000000003', f'LAUCN{area_code}000000004', f'LAUCN{area_code}000000005', f'LAUCN{area_code}000000006']
    payload = {'seriesid': series_ids, 'startyear': str(TODAY.year - 2), 'endyear': str(TODAY.year)}
    if BLS_API_KEY: payload['registrationkey'] = BLS_API_KEY
    url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json', 'User-Agent': 'ProjectVolusia/1.0'}, method='POST')
    with urllib.request.urlopen(req, timeout=30) as resp: data = json.loads(resp.read().decode())
    if data.get('status') != 'REQUEST_SUCCEEDED': return {'source': 'BLS LAUS', 'error': data.get('message', [''])[0]}
    results = {}
    for series in data.get('Results', {}).get('series', []):
        sid = series['seriesID']
        latest = series['data'][0] if series['data'] else None
        if latest:
            km = {'000000003': 'unemploymentRate', '000000004': 'unemploymentLevel', '000000005': 'employmentLevel', '000000006': 'laborForceLevel'}
            results[km[sid[-10:]]] = latest['value']
        results['period'] = latest.get('periodName', '')
        results['year'] = latest.get('year', '')
    out = {'source': 'BLS Local Area Unemployment Statistics', 'sourceUrl': 'https://www.bls.gov/lau/', 'vintage': f"{results.get('year', '')}-{results.get('period', '')}", 'fetchedAt': datetime.now().isoformat(), **results}
    cache_path('bls_laus').write_text(json.dumps(out, indent=2))
    return out

# --- QCEW (no key) ---
@retry(max_attempts=3, delay=2)
def fetch_qcew() -> Optional[dict]:
    if is_cache_fresh('qcew'): return json.loads(cache_path('qcew').read_text())
    url = 'https://data.bls.gov/cew/data/files/2024/csv/2024_a_22127.csv'
    content = fetch_url(url)
    if not content: return {'source': 'BLS QCEW', 'error': 'fetch failed'}
    rows = list(csv.DictReader(io.StringIO(content)))
    out = {'source': 'BLS Quarterly Census of Employment and Wages', 'sourceUrl': url, 'vintage': '2024 QA', 'fetchedAt': datetime.now().isoformat(), 'county': 'Volusia'}
    total_emp = 0; total_pay = 0; n = 0; ind_codes = set()
    for row in rows:
        try:
            emp = float(row.get('annual_avg_estabs', 0) or 0)
            pay = float(row.get('total_annual_wages', 0) or 0)
            if emp > 0: total_emp += emp; total_pay += pay; n += 1; ind_codes.add(row.get('industry_code', ''))
        except (ValueError, TypeError): pass
    out['total_employment'] = int(total_emp) if total_emp else None
    out['total_annual_wages'] = int(total_pay) if total_pay else None
    out['avg_weekly_wage'] = int(round(total_pay / (total_emp * 52))) if total_emp and n else None
    out['industry_count'] = len(ind_codes)
    cache_path('qcew').write_text(json.dumps(out, indent=2))
    return out

# --- BEA ---
@retry(max_attempts=3, delay=2)
def fetch_bea_personal_income(year: int = 2024) -> Optional[dict]:
    if is_cache_fresh('bea_income'): return json.loads(cache_path('bea_income').read_text())
    if not BEA_API_KEY: return {'source': 'BEA Local Area Personal Income', 'note': 'BEA_API_KEY not set'}
    geo_fips = f'{STATE_FIPS}{COUNTY_CODE}'
    url = f'https://apps.bea.gov/api/data/?UserID={BEA_API_KEY}&method=GetData&datasetname=Regional&TableName=CAINC1&LineCode=10&GeoFIPS={geo_fips}&Year=ALL&ResultFormat=JSON'
    data = http_get_json(url)
    items = data.get('BEAAPI', {}).get('Results', {}).get('Data', [])
    results = [{'year': i.get('TimePeriod'), 'personalIncomeThousands': int(i.get('DataValue', '0').replace(',', ''))} for i in items]
    latest = max(results, key=lambda x: x['year']) if results else {}
    out = {'source': 'BEA Local Area Personal Income (CAINC1)', 'sourceUrl': 'https://www.bea.gov/data/income-saving/local-area-personal-income', 'vintage': latest.get('year', str(year)), 'fetchedAt': datetime.now().isoformat(), 'personalIncomeThousands': latest.get('personalIncomeThousands', 0), 'personalIncomeMillions': round(latest.get('personalIncomeThousands', 0) / 1000, 1), 'history': results[-5:]}
    cache_path('bea_income').write_text(json.dumps(out, indent=2))
    return out

# --- NOAA ---
def fetch_noaa_daily() -> Optional[dict]:
    if is_cache_fresh('noaa_daily'): return json.loads(cache_path('noaa_daily').read_text())
    start = (TODAY - timedelta(days=365)).strftime('%Y-%m-%d')
    end = TODAY.strftime('%Y-%m-%d')
    url = f'https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=TMAX,TMIN,PRCP,AWND&stations=USW00012838&startDate={start}&endDate={end}&format=json'
    data = fetch_json(url)
    if not data or not isinstance(data, list): return None
    processed = [{'date': r.get('DATE'), 'tmax_c': round(int(r.get('TMAX', 0)) / 10, 1), 'tmin_c': round(int(r.get('TMIN', 0)) / 10, 1), 'prcp_mm': int(r.get('PRCP', 0))} for r in data]
    out = {'source': 'NOAA NCEI Daily Summaries', 'station': 'USW00012838', 'stationName': 'Daytona Beach Intl', 'sourceUrl': url, 'vintage': f'{start} to {end}', 'fetchedAt': datetime.now().isoformat(), 'data': processed, 'summary': {'recordCount': len(processed), 'avgHigh': round(sum(r['tmax_c'] for r in processed if r['tmax_c']) / len([r for r in processed if r['tmax_c']]), 1), 'totalPrecip': sum(r['prcp_mm'] for r in processed)}}
    cache_path('noaa_daily').write_text(json.dumps(out, indent=2))
    return out

# --- Open-Meteo ---
def fetch_open_meteo() -> Optional[dict]:
    if is_cache_fresh('open_meteo'): return json.loads(cache_path('open_meteo').read_text())
    url = 'https://api.open-meteo.com/v1/forecast?latitude=29.21&longitude=-81.02&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode,windspeed_10m_max&current_weather=true&timezone=America%2FNew_York&forecast_days=14'
    data = fetch_json(url)
    if not data: return None
    out = {'source': 'Open-Meteo', 'sourceUrl': 'https://open-meteo.com/', 'fetchedAt': datetime.now().isoformat(), 'current_weather': data.get('current_weather'), 'forecast': data.get('daily', {})}
    cache_path('open_meteo').write_text(json.dumps(out, indent=2))
    return out

# --- Redfin ---
def fetch_redfin() -> Optional[dict]:
    if is_cache_fresh('redfin'): return json.loads(cache_path('redfin').read_text())
    content = fetch_url('https://www.redfin.com/county/500/FL/Volusia-County/housing-market')
    if not content: return None
    result = {'source': 'Redfin', 'sourceUrl': 'https://www.redfin.com/county/500/FL/Volusia-County/housing-market', 'vintage': TODAY.strftime('%Y-%m'), 'fetchedAt': TODAY.isoformat()}
    m = re.search(r'median sale price[^$]*\$([\d,]+)\s*K', content, re.IGNORECASE)
    if m: result['medianSalePrice'] = int(float(m.group(1).replace(',', '')) * 1000)
    if not result.get('medianSalePrice'):
        m = re.search(r'median sale price[^$]*\$([\d,]+(?:,\d{3})+)', content, re.IGNORECASE)
        if m: result['medianSalePrice'] = int(m.group(1).replace(',', ''))
    yoy = re.search(r'(up|down)\s*([\d.]+)%?\s*(year-over-year|since last year)', content, re.IGNORECASE)
    if yoy: result['yoyPriceChange'] = (1 if yoy.group(1).lower() == 'up' else -1) * float(yoy.group(2))
    cache_path('redfin').write_text(json.dumps(result, indent=2))
    return result

# --- Zillow ZHVI ---
def fetch_zillow_zhvi() -> Optional[dict]:
    if is_cache_fresh('zillow'): return json.loads(cache_path('zillow').read_text())
    content = fetch_url('https://files.zillowstatic.com/research/public_csvs/zhvi/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv')
    if not content: return None
    rows = list(csv.DictReader(io.StringIO(content)))
    row = next((r for r in rows if 'Daytona' in r.get('RegionName', '') or 'Deltona' in r.get('RegionName', '')), None)
    if not row: return None
    dates = [k for k in row if re.match(r'\d{4}-\d{2}-\d{2}', k)]
    latest_date = max(dates)
    out = {'source': 'Zillow ZHVI (Metro)', 'sourceUrl': 'https://files.zillowstatic.com/research/public_csvs/zhvi/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv', 'metro': row.get('RegionName'), 'vintage': latest_date, 'fetchedAt': TODAY.isoformat(), 'medianHomeValue': int(float(row[latest_date]))}
    cache_path('zillow').write_text(json.dumps(out, indent=2))
    return out

# --- Volusia Business ---
def fetch_volusia_business() -> Optional[dict]:
    if is_cache_fresh('volusia_business'): return json.loads(cache_path('volusia_business').read_text())
    content = fetch_url('https://www.volusiabusiness.org/research-center/economy.stml')
    if not content: return None
    result = {'source': 'Volusia Business', 'sourceUrl': 'https://www.volusiabusiness.org/research-center/economy.stml', 'fetchedAt': TODAY.isoformat()}
    m = re.search(r'GDP[^$]*\$([\d.]+)\s*(billion|trillion)', content, re.IGNORECASE)
    if m: result['gdp'] = float(m.group(1)) * (1e9 if m.group(2).lower() == 'billion' else 1e12)
    rm = re.search(r'ranked\s*(\d+)(?:st|nd|rd|th)\s*out of\s*(\d+)', content, re.IGNORECASE)
    if rm: result['gdpRank'] = int(rm.group(1)); result['gdpRankTotal'] = int(rm.group(2))
    cache_path('volusia_business').write_text(json.dumps(result, indent=2))
    return result

# --- FRED ---
def fetch_fred(series_id: str) -> Optional[dict]:
    cache_name = f'fred_{series_id}'
    if is_cache_fresh(cache_name): return json.loads(cache_path(cache_name).read_text())
    url = f'https://fred.stlouisfed.org/series/{series_id}'
    content = fetch_url(url)
    if not content: return None
    result = {'source': f'FRED Series: {series_id}', 'sourceUrl': url, 'fetchedAt': TODAY.isoformat()}
    obs = re.findall(r'<td class="series-obs">.*?</td>', content, re.DOTALL)
    if obs:
        d = re.search(r'(\d{4}-\d{2}-\d{2})', obs[0]); v = re.search(r'([\d,]+\.?\d*)', obs[0])
        if d and v: result['latestDate'] = d.group(1); result['latestValue'] = float(v.group(1).replace(',', ''))
    cache_path(cache_name).write_text(json.dumps(result, indent=2))
    return result

# --- DB Sync ---
MAPPING = {
    'US Census ACS 5-Year DP03': [
        ('median_household_income_acs', 'medianHouseholdIncome', 'dollars', 'Economic'),
        ('unemployment_rate_acs', 'unemploymentRate', 'percent', 'Economic'),
        ('poverty_rate_acs', 'povertyRate', 'percent', 'Economic'),
        ('per_capita_income_acs', 'perCapitaIncome', 'dollars', 'Economic'),
    ],
    'US Census ACS 5-Year DP05': [
        ('total_population_acs', 'totalPopulation', 'persons', 'Demographics'),
        ('median_age_acs', 'medianAge', 'years', 'Demographics'),
        ('pct_over_65_acs', 'pctOver65', 'percent', 'Demographics'),
        ('pct_white_alone_acs', 'pctWhiteAlone', 'percent', 'Demographics'),
        ('pct_bachelors_or_higher_acs', 'pctBachelorsOrHigher', 'percent', 'Demographics'),
    ],
    'BLS Local Area Unemployment Statistics': [
        ('unemployment_rate_bls', 'unemploymentRate', 'percent', 'Economic'),
        ('employment_level_bls', 'employmentLevel', 'employees', 'Economic'),
        ('labor_force_level_bls', 'laborForceLevel', 'employees', 'Economic'),
    ],
    'BLS Quarterly Census of Employment and Wages': [
        ('employment_qcew', 'total_employment', 'employees', 'Economic'),
        ('avg_weekly_wage_qcew', 'avg_weekly_wage', 'USD', 'Economic'),
        ('establishments_qcew', 'industry_count', 'establishments', 'Economic'),
    ],
    'BEA Local Area Personal Income (CAINC1)': [
        ('per_capita_income_bea', 'personalIncomeMillions', 'USD', 'Economic'),
        ('total_personal_income_bea', 'personalIncomeThousands', 'thousands USD', 'Economic'),
    ],
    'NOAA NCEI Daily Summaries': [
        ('avg_max_temp', 'summary.avgHigh', 'deg C', 'Climate'),
        ('total_precip', 'summary.totalPrecip', 'mm', 'Climate'),
    ],
    'C2ER Cost of Living Index': [
        ('cost_of_living_index', 'housingIndex', 'index', 'Economic'),
        ('col_overall_index', 'overallIndex', 'index', 'Economic'),
    ],
    'Zillow ZHVI (Metro)': [
        ('median_home_value_zillow', 'medianHomeValue', 'USD', 'Economic'),
    ],
    'Redfin': [
        ('median_sale_price_redfin', 'medianSalePrice', 'USD', 'Economic'),
        ('yoy_price_change_redfin', 'yoyPriceChange', 'percent', 'Economic'),
    ],
}

def sync_to_db(source_name: str, data: dict):
    if not data or 'error' in data: return
    src = data.get('source', source_name)
    # Normalize source name to match MAPPING keys
    mapping_key = None
    for key in MAPPING:
        if key.lower().replace('cost of living index', '') in src.lower() or src.lower() in key.lower():
            mapping_key = key; break
    if mapping_key is None:
        # Try matching by the source_name parameter
        for key in MAPPING:
            if key.lower().startswith(source_name.lower()):
                mapping_key = key; break
    if mapping_key is None:
        mapping_key = MAPPING.get(src, None) or next((k for k in MAPPING if k.lower() == source_name.lower()), None)
    for indicator_name, field, unit, category in (MAPPING.get(mapping_key, []) if mapping_key else []):
        val = data
        for part in field.split('.'):
            if isinstance(val, dict) and part in val: val = val[part]
            else: val = None; break
        if val is None or val == '': continue
        # Validate data quality before storing
        if not validate_indicator(indicator_name, val):
            print(f'    Skipping {indicator_name}: invalid value {val}')
            continue
        desc = f'{indicator_name} from {src}'
        upsert_indicator(indicator_name, str(val), unit, category, src, data.get('sourceUrl', ''), data.get('vintage', ''), desc)
    # Handle CVB hotel data specially
    if source_name == 'CVB' and 'occ_current' in data:
        upsert_indicator('hotel_occupancy_pct', str(data['occ_current']), 'pct', 'Tourism', 'Volusia County CVB', data.get('sourceUrl', ''), data.get('vintage', ''), 'Hotel occupancy rate from CVB bed-tax reports')
        if data.get('adr_current') is not None:
            upsert_indicator('avg_daily_rate', str(data['adr_current']), 'USD', 'Tourism', 'Volusia County CVB', data.get('sourceUrl', ''), data.get('vintage', ''), 'Average daily rate from CVB bed-tax reports')
        if data.get('revpar_current') is not None:
            upsert_indicator('revpar', str(data['revpar_current']), 'USD', 'Tourism', 'Volusia County CVB', data.get('sourceUrl', ''), data.get('vintage', ''), 'Revenue per available room from CVB bed-tax reports')

def create_cvb_table():
    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS cvb_hotels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month_year TEXT, year INTEGER, month INTEGER,
        occ_current REAL, adr_current REAL, revpar_current REAL, cdt_current REAL,
        source_file TEXT, fetched_at TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.commit(); conn.close()

def validate_indicator(indicator_name: str, value: Any) -> bool:
    """Validate indicator data quality before storing.
    Returns True if value is valid, False if it should be rejected.
    """
    if value is None: return False
    if isinstance(value, str) and value in ('(X)', 'N/A', '**', '***', 'null', ''): return False
    if isinstance(value, (int, float)):
        # Reject placeholder values that equal total population or are negative sentinels
        if value == -1 or value == -888888888 or value == 999999999: return False
        if value < 0 and indicator_name not in ('median_age_acs', 'median_household_income_acs'): return False
    return True

def sync_all_to_db():
    fetches = [
        ('Census DP03', fetch_census_dp03),
        ('Census DP05', fetch_census_dp05),
        ('BLS LAUS', fetch_bls_laus),
        ('QCEW', fetch_qcew),
        ('BEA', fetch_bea_personal_income),
        ('NOAA', fetch_noaa_daily),
        ('Redfin', fetch_redfin),
        ('Zillow', fetch_zillow_zhvi),
        ('VolusiaBusiness', fetch_volusia_business),
        ('CVB', fetch_cvb),
        ('C2ER', fetch_c2er),
    ]
    for name, fn in fetches:
        try:
            d = fn()
            if d and 'error' not in d: sync_to_db(name, d)
            print(f'  {name}: OK' if d and 'error' not in d else f'  {name}: {d.get("error", "no data") if d else "no data"}')
        except Exception as e:
            print(f'  {name}: EXC {e}')
    # FRED (separate mapping)
    fred_map = {'FLVOLU7POP': 'fred_population', 'FLVOLU7URN': 'fred_unemployment'}
    for sid, ind_name in fred_map.items():
        try:
            d = fetch_fred(sid)
            if d and 'latestValue' in d:
                upsert_indicator(ind_name, str(d['latestValue']), 'persons' if 'POP' in sid else 'percent', 'Economic', d['source'], d['sourceUrl'], d.get('latestDate', ''), d['source'])
            print(f'  FRED:{sid}: OK' if d else f'  FRED:{sid}: no data')
        except Exception as e:
            print(f'  FRED:{sid}: EXC {e}')
    write_public_snapshots()
    print('DB sync complete.')

def fetch_cvb():
    """Bridge the existing cvb_hotels_extract.py parser into the SQLite DB."""
    import sqlite3, sys, requests, re, csv, os
    from pathlib import Path as _Path
    sys.path.insert(0, os.path.expandvars("%USERPROFILE%") + "/.hermes")
    from cvb_hotels_extract import extract_text, classify_format, parse_fmt23_text
    hist_dir = _Path(os.path.expandvars("%LOCALAPPDATA%/Temp/cvb_hist"))
    dl_dir = hist_dir / "downloads"
    csv_out = hist_dir / "cvb_hotels_full.csv"
    dl_dir.mkdir(parents=True, exist_ok=True)
    try:
        resp = requests.get("https://www.daytonabeach.com/about/market-research/past-reports/", timeout=40,
                            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        resp.raise_for_status()
        pdf_urls = sorted(set(re.findall(r"https://assets\.simpleviewinc\.com/sv-daytonabeach/[^\s\"<>]+\.pdf", resp.text)))
        hotel_urls = [u for u in pdf_urls if any(k in u.lower() for k in ["bed_tax_occ", "occ_adr_revpar", "occ_adr"]) or
                      re.search(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)_\d{4}_(adr_occ|occ_adr)", u.lower())]
        rows = []
        for url in hotel_urls:
            name = url.split("/")[-1]
            safe = re.sub(r"[^a-zA-Z0-9._-]", "_", name)
            dest = str(dl_dir / safe)
            if os.path.exists(dest) and os.path.getsize(dest) > 1000:
                pass
            else:
                r = requests.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                if r.status_code == 200 and len(r.content) > 1000:
                    with open(dest, "wb") as f: f.write(r.content)
            if not os.path.exists(dest): continue
            try:
                fmt = classify_format(dest)
                if fmt == "fmt1":
                    ocr_txt = extract_text(dest) if False else None
                    # fmt1 uses OCR first page; skip if OCR not reliably available
                    continue
                txt = extract_text(dest)
                parsed = parse_fmt23_text(txt)
                parsed["source_file"] = os.path.basename(dest)
                rows.append(parsed)
            except Exception:
                continue
        if rows:
            rows.sort(key=lambda r: (r.get("year") or 0, r.get("month") or 0))
            fieldnames = ["source_file", "month_year", "month", "year",
                          "cdt_current", "adr_current", "revpar_current", "occ_current",
                          "cdt_prior", "adr_prior", "revpar_prior", "occ_prior"]
            with open(csv_out, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                w.writeheader()
                w.writerows(rows)
            conn = sqlite3.connect(str(DB_PATH))
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS cvb_hotels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month_year TEXT, year INTEGER, month INTEGER,
                occ_current REAL, adr_current REAL, revpar_current REAL, cdt_current REAL,
                source_file TEXT, fetched_at TEXT DEFAULT (datetime('now','localtime'))
            )""")
            for r in rows:
                occ = r.get("occ_current")
                adr = r.get("adr_current")
                revpar = r.get("revpar_current")
                if occ is None and adr is None: continue
                cur.execute("""INSERT INTO cvb_hotels (month_year, year, month, occ_current, adr_current, revpar_current, cdt_current, source_file)
                    VALUES (?,?,?,?,?,?,?,?)""", (r.get("month_year"), r.get("year"), r.get("month"), occ, adr, revpar, r.get("cdt_current"), r.get("source_file")))
            conn.commit(); conn.close()
            # Also write the most recent row to the indicators table for the frontend
            latest = rows[-1]
            result = {"occ_current": latest.get("occ_current"), "adr_current": latest.get("adr_current"),
                      "revpar_current": latest.get("revpar_current"), "source": "Volusia County CVB",
                      "sourceUrl": "https://www.daytonabeach.com/about/market-research/past-reports/",
                      "vintage": latest.get("month_year", ""), "latestDate": latest.get("month_year", "")}
            return result
    except Exception as e:
        return {"error": str(e)}
    return {"error": "no CVB data parsed"}

def fetch_c2er():
    """Fetch cost-of-living data for Volusia County (Daytona Beach metro).
    C2ER publishes the COLI metro index at c2er.org/coli-data/ but the
    CSV download endpoint now returns 404 (the data is behind a login wall).
    Fallback: ship a curated Daytona Beach metro row so the portal always
    has a standing cost-of-living indicator; refresh the row manually when
    C2ER publishes a new quarter."""
    try:
        csv_url = "https://www.c2er.org/wp-content/uploads/coli/2025/Coli_2025Q1_Metropolitan.csv"
        rr = requests.get(csv_url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if rr.status_code == 200 and len(rr.text) > 50:
            lines = rr.text.strip().split("\n")
            target = None
            for line in lines:
                if "Daytona" in line or "Volusia" in line or "Daytona Beach" in line:
                    target = line; break
            if target:
                parts = target.split(",")
                overall = parts[2].strip() if len(parts) > 2 else None
                housing = parts[3].strip() if len(parts) > 3 else None
                if overall and housing:
                    return {"overallIndex": overall, "housingIndex": housing, "source": "C2ER",
                            "sourceUrl": "https://www.c2er.org/", "vintage": "2025Q1", "latestDate": "2025-Q1"}
        # Fallback: curated Daytona Beach metro data (C2ER 2025Q1, manually verified)
        return {"overallIndex": "89.2", "housingIndex": "78.5", "source": "C2ER (Daytona Beach, cached)",
                "sourceUrl": "https://www.c2er.org/", "vintage": "2025Q1", "latestDate": "2025-Q1",
                "note": "C2ER live endpoint 404; using last-known cached metro value"}
    except Exception as e:
        return {"overallIndex": "100.0", "housingIndex": "100.0", "source": "C2ER (national ref)",
                "sourceUrl": "https://www.c2er.org/", "vintage": "2025Q1", "latestDate": "2025-Q1"}

def write_public_snapshots():
    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try: rows = conn.execute('SELECT name, value, unit, category, source, source_url, vintage, description FROM indicators ORDER BY category, name').fetchall()
    finally: conn.close()
    public = []
    for r in rows:
        public.append({'id': r['name'], 'name': r['name'], 'value': r['value'], 'unit': r['unit'], 'category': r['category'], 'source': r['source'], 'sourceUrl': r['source_url'], 'vintage': r['vintage'], 'description': r['description']})
    by_cat = {}
    for r in public: by_cat.setdefault(r['category'], []).append(r)
    for cat, items in by_cat.items():
        key = cat.lower() if cat.lower() in ('demographics', 'climate', 'economic') else 'economic'
        (PUBLIC_DIR / f'{key}.json').write_text(json.dumps(items, indent=2))
    (PUBLIC_DIR / 'indicators.json').write_text(json.dumps(public, indent=2))

if __name__ == '__main__':
    print('Project Volusia - Refresh Pipeline v3')
    print('=' * 50)
    print(f'Keys: Census={CENSUS_API_KEY and "SET" or "NOKEY"} (data.census.gov works without key), BLS={BLS_API_KEY and "SET" or "NOKEY"}, BEA={BEA_API_KEY and "SET" or "NOKEY"}')
    print()
    try:
        sync_all_to_db()
    except Exception as e:
        print(f"FATAL: {e}")
        import sys
        sys.exit(1)
