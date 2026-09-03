# Project Volusia — OSINT Recon Report

> Data source reconnaissance for Volusia County, Florida.
> Tested 2026-09-02 for accessibility, API availability, and data freshness.

**Classification:** Internal — Private Operational Intelligence

---

## 1. ACCESSIBLE — No API Key Required

These sources return real data immediately. Fetchers ready to build.

| Source | Endpoint | Data | Status |
|--------|----------|------|--------|
| **Census data.census.gov** | `https://data.census.gov/api/access/data/table?g=0500000US12127&tid=ACSDP5Y2023.DP03` | ACS DP03 Economic (income, employment, poverty) | ✅ Working |
| **Census data.census.gov** | `https://data.census.gov/api/access/data/table?g=0500000US12127&tid=ACSDP5Y2023.DP05` | ACS DP05 Demographics (age, sex, race) | ✅ Working |
| **Census data.census.gov** | `https://data.census.gov/api/access/data/table?g=0500000US12127&tid=ACSST1Y2024.S0101` | ACS 1-Year S0101 (Age/Sex) | ✅ Working |
| **NOAA NCEI** | `https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=TMAX,TMIN,PRCP,AWND&stations=USW00012838&startDate=YYYY-MM-DD&endDate=YYYY-MM-DD&format=json` | Daily weather (Daytona Beach station) | ✅ Working |
| **Census TIGER** | `https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip` | County boundary shapefiles | ✅ Working |
| **Census Geocoder** | `https://geocoding.geo.census.gov/geocoder/locations/address?...` | Address geocoding | ✅ Working |

### Sample Data Verified:

**Census DP03 (2023 5-Year ACS):**
- Median Household Income: $66,581
- Unemployment Rate: 4.0%
- Poverty Rate: 2.2%

**NOAA Daily Summaries (Summer 2024):**
- Station: USW00012838 (Daytona Beach)
- TMAX: 306 (30.6°C / 87°F) — June 1, 2024
- TMIN: 256 (25.6°C / 78°F) — June 1, 2024
- PRCP: 0 (mm) — June 1, 2024

---

## 2. REQUIRES FREE API KEY

These sources have valid endpoints but need registration. Keys are free.

| Source | Signup URL | Endpoint | Data |
|--------|-----------|----------|------|
| **Census API** | https://api.census.gov/data/key_signup.html | `https://api.census.gov/data/2024/acs/acs5/profile?...` | ACS 5-Year, 1-Year, all tables |
| **BLS API** | https://data.bls.gov/registrationEngine/ | `https://api.bls.gov/publicAPI/v2/timeseries/data/` | LAUS unemployment, QCEW employment/wages |
| **BEA API** | https://apps.bea.gov/api/signup/ | `https://apps.bea.gov/api/data/?...` | Personal income, GDP by county |

### BLS Series IDs for Volusia County:
- LAUCN12127000000003 (unemployment rate)
- LAUCN12127000000004 (unemployment level)
- LAUCN12127000000005 (employment level)
- LAUCN12127000000006 (labor force level)

### BEA Parameters:
- TableName: CAINC1
- LineCode: 10 (Total personal income)
- GeoFIPS: 12127

---

## 3. INACCESSIBLE — No Public API or Blocked

These sources have no working public endpoint. Scraping or manual download required.

| Source | URL | Issue |
|--------|-----|-------|
| **Volusia Open Data** | data.volusia.org | Domain doesn't exist |
| **Volusia GIS Hub** | gis.volusia.org | Domain doesn't exist |
| **Volusia Property Appraiser** | vcpa.volusia.org | No public API; scraping required |
| **FCC Broadband Map** | broadbandmap.fcc.gov/api | Access denied (Akamai block) |
| **Florida DOE** | fldoe.org/accountability | Access denied (Akamai block) |
| **Florida DEO** | floridajobs.org | No public API |
| **CDC PLACES** | places.cdc.gov/api | No public API endpoint |
| **County Health Rankings** | countyhealthrankings.org/api | 404 (no API) |
| **Zillow County ZHVI** | files.zillowstatic.com | County-level not in CSV; metro-level only |
| **Realtor.com** | realtor.com/research | No public download |

---

## 4. ALTERNATIVE SOURCES DISCOVERED

### Zillow Metro-Level Data (Daytona Beach MSA)
- ZHVI (Home Value Index): Metro-level CSV available
- ZORI (Rent Index): Metro-level CSV available
- URL pattern: `https://files.zillowstatic.com/research/public_csvs/zhvi/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv`

### Census ACS 1-Year (More Current)
- Available via data.census.gov API
- Table S0101 (Age and Sex)
- More current than 5-year but smaller sample size

### NOAA Weather Station
- **Station ID:** USW00012838
- **Name:** DAYTONA BEACH INTERNATIONAL AIRPORT
- **Coordinates:** 29.18°N, 81.05°W
- **Elevation:** 10.4m
- **Data Types Available:** TMAX, TMIN, PRCP, EVAP, AWND, SNOW, SNWD

---

## 5. RECOMMENDED DATA ARCHITECTURE

```
                    ┌─────────────────────────────────────┐
                    │        volusia-portal (PUBLIC)       │
                    │   React + Vite + Tailwind + Nivo     │
                    │   Leaflet maps, 7 constituency pages  │
                    └──────────────┬──────────────────────┘
                                   │ REST API
                    ┌──────────────▼──────────────────────┐
                    │      FastAPI Backend (:8000)         │
                    │   /indicators, /indicators/economic  │
                    │   /indicators/demographics           │
                    │   /indicators/income                 │
                    │   /indicators/weather                │
                    └──────────────┬──────────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
┌─────────▼────────┐  ┌───────────▼──────────┐  ┌─────────▼────────┐
│  Census Fetcher  │  │  NOAA Fetcher        │  │  BLS/BEA Fetcher │
│  (data.census)   │  │  (NCEI API)          │  │  (needs keys)    │
│  ✅ No key       │  │  ✅ No key           │  │  ⚠️ Keys needed  │
└─────────┬────────┘  └───────────┬──────────┘  └─────────┬────────┘
          │                        │                        │
┌─────────▼────────┐  ┌───────────▼──────────┐  ┌─────────▼────────┐
│  ACS DP03        │  │  Daily Summaries     │  │  LAUS            │
│  (Economic)      │  │  (TMAX,TMIN,PRCP)   │  │  (Unemployment)  │
│  ACS DP05        │  │  Monthly Normals     │  │  QCEW            │
│  (Demographic)   │  │  (1991-2020)         │  │  (Employment)    │
│  ACS 1-Year      │  │                      │  │  CAINC1          │
│  (Current)       │  │                      │  │  (Income)        │
└──────────────────┘  └──────────────────────┘  └──────────────────┘
```

---

## 6. IMPLEMENTATION PRIORITY

### Phase 1 — Immediate (No Keys Needed)
1. **Census data.census.gov fetcher** — ACS DP03, DP05, S0101
2. **NOAA NCEI fetcher** — Daily weather, monthly normals
3. **Census TIGER fetcher** — County boundary GeoJSON for maps

### Phase 2 — Register for Free Keys
4. **Census API key** — Full ACS access, all tables
5. **BLS API key** — LAUS unemployment, QCEW employment/wages
6. **BEA API key** — Personal income by county

### Phase 3 — Scrape/Manual (No API)
7. **Volusia Property Appraiser** — Parcel data via scraping
8. **Zillow Metro ZHVI/ZORI** — Daytona Beach MSA data
9. **CDC PLACES** — Health data via manual download
10. **County Health Rankings** — Health data via manual download

---

## 7. DATA FRESHNESS

| Source | Vintage | Refresh |
|--------|---------|---------|
| Census ACS 5-Year | 2023 | Annual (Dec) |
| Census ACS 1-Year | 2024 | Annual (Sep) |
| NOAA Daily | Real-time | Daily |
| BLS LAUS | Monthly | Monthly |
| BEA CAINC1 | 2024 | Annual (Sep) |
| Zillow ZHVI | Monthly | Monthly |

---

Document owner: Project Volusia Leadership
Related: DATA_CATALOG.md, REPO_SUPPORT_MATRIX.md
