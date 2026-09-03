# Project Volusia — OSINT Recon Report v2

> Expanded data source reconnaissance for Volusia County, Florida.
> Tested 2026-09-02 using DDGS search backend.
> Classification: Internal — Private Operational Intelligence

---

## 1. WORKING SOURCES (Verified Data Retrieval)

### 1.1 Census data.census.gov (Undocumented API)
- **Endpoint:** `https://data.census.gov/api/access/data/table?g=0500000US12127&tid=ACSDP5Y2023.DP03`
- **Data:** ACS 5-Year Economic Characteristics (DP03), Demographics (DP05), 1-Year (S0101)
- **Status:** ✅ Working, no API key required
- **Sample:** Median HH Income $66,581 | Unemployment 4.0% | Poverty 2.2%
- **TID format:** `ACSDP5Y2023.DP03` (DP03/DP05), `ACSST1Y2024.S0101` (1-year)
- **Geography param:** `g=0500000US12127` (state 12 + county 127)

### 1.2 NOAA NCEI Weather Data
- **Daily Summaries:** `https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=TMAX,TMIN,PRCP,AWND&stations=USW00012838&startDate=YYYY-MM-DD&endDate=YYYY-MM-DD&format=json`
- **Station:** USW00012838 (Daytona Beach International Airport)
- **Coordinates:** 29.18°N, 81.05°W
- **Status:** ✅ Working, no API key required
- **Data:** Daily TMAX, TMIN, PRCP (in tenths of units), AWND

### 1.3 Census QuickFacts
- **URL:** https://www.census.gov/quickfacts/fact/table/volusiacountyflorida/PST045225
- **Data:** Population, demographics, housing, income
- **Status:** ✅ Working, HTML scrape

### 1.4 Census Geocoder
- **URL:** `https://geocoding.geo.census.gov/geocoder/locations/address?street=...&city=Daytona+Beach&state=FL&benchmark=4&format=json`
- **Status:** ✅ Working, no API key required

### 1.5 FRED (St. Louis Fed)
- **Population:** https://fred.stlouisfed.org/series/FLVOLU7POP
- **Unemployment Rate:** https://fred.stlouisfed.org/series/FLVOLU7URN
- **ACS Total Population:** https://fred.stlouisfed.org/series/B03002001E012127
- **Status:** ✅ Working, HTML scrape

### 1.6 BEA GDP Data
- **URL:** https://www.bea.gov/data/gdp/gross-domestic-product
- **Status:** ⚠️ Requires API key for direct access

### 1.7 Volusia County GIS Data Downloads
- **URL:** https://www.volusia.org/services/financial-and-administrative-services/finance-department/information-technology/geographic-information-services/data/download-data.stml
- **Status:** ✅ Working, HTML scrape for links

### 1.8 Volusia County Budget/Financial PDFs
- **5-Year Forecast:** https://www.volusia.org/file/5892/5-Year-Forecast-FY-2024-25-to-2028-29.pdf
- **Adopted Budget FY2024-25:** https://www.volusia.org/services/financial-and-administrative-services/management-and-budget/pdf/Adopted-Budget-FY-2024-25-IT.pdf
- **CIP:** https://www.volusia.org/services/financial-and-administrative-services/management-and-budget/pdf/CIP-Book-Final-ADA.pdf
- **Status:** ✅ PDFs accessible

### 1.9 Redfin Volusia County Housing
- **URL:** https://www.redfin.com/county/500/FL/Volusia-County/housing-market
- **Data:** Median sale price ($343K), market trends
- **Status:** ✅ Working, HTML scrape

### 1.10 News-JournalOnline Real Estate Data
- **URL:** https://data.news-journalonline.com/real-estate-market-report/
- **Data:** Realtor.com market report for Volusia County
- **Status:** ✅ Working, HTML scrape

### 1.11 Florida DEO Labor Market Statistics
- **URL:** https://www.floridajobs.org/economic-data/local-area-unemployment-statistics-(laus)
- **Status:** ⚠️ Blocked (Akamai) but data referenced in search results

### 1.12 Volusia County Economic Development (VolusiaBusiness.org)
- **Economy:** https://www.volusiabusiness.org/research-center/economy.stml
- **Q3 2024 Report:** https://www.volusiabusiness.org/media-center/news-and-stories/volusia-county-economic-development-3rd-quarter-2024-report-available.stml
- **Data:** GDP $22.9B, ranked 14th/67 FL counties
- **Status:** ✅ Working, HTML scrape

### 1.13 BLS County Employment and Wages
- **URL:** https://www.bls.gov/regions/southeast/news-release/countyemploymentandwages_florida.htm
- **Status:** ✅ Working, HTML scrape (Q4 2025 release)

### 1.14 Florida Health (Volusia County)
- **URL:** https://volusia.floridahealth.gov/index.html
- **Status:** ✅ Working, HTML scrape

### 1.15 HealthByCounty
- **URL:** https://healthbycounty.com/florida
- **Data:** CDC PLACES 2022-2023, health scores
- **Status:** ✅ Working, HTML scrape

---

## 2. WEB SEARCH BACKEND STATUS

**Current backend:** `ddgs` (DuckDuckGo search)
**Status:** ✅ Working — no API key required
**Config:** `web.backend: ddgs` in config.yaml

**Tested queries that returned useful Volusia County results:**
- "Volusia County Florida economic indicators 2024"
- "Volusia County Florida tourism statistics 2024"
- "Volusia County Florida real estate market data"
- "Volusia County Florida demographics census 2024"
- "Volusia County Florida traffic data FDOT"
- "Volusia County Florida health data CDC PLACES"
- "site:volusia.org filetype:pdf economic development 2024"
- "site:bls.gov Volusia County unemployment 2024"
- "site:census.gov Volusia County quickfacts"
- "site:fred.stlouisfed.org Volusia County"

---

## 3. SUMMARY OF NEW SOURCES

| # | Source | Data Type | Access Method | Status |
|---|--------|-----------|---------------|--------|
| 1 | Census data.census.gov | ACS DP03/DP05/S0101 | Undocumented API | ✅ Direct |
| 2 | NOAA NCEI | Daily weather | REST API | ✅ Direct |
| 3 | Census QuickFacts | Population, income | HTML scrape | ✅ Direct |
| 4 | Census Geocoder | Address geocoding | REST API | ✅ Direct |
| 5 | FRED | Population, unemployment | HTML scrape | ✅ Direct |
| 6 | Volusia GIS | Parcel, boundary data | HTML scrape | ✅ Direct |
| 7 | Volusia.org PDFs | Budget, forecast, CIP | PDF download | ✅ Direct |
| 8 | Redfin | Housing market | HTML scrape | ✅ Direct |
| 9 | News-JournalOnline | Real estate data | HTML scrape | ✅ Direct |
| 10 | VolusiaBusiness.org | Economic development | HTML scrape | ✅ Direct |
| 11 | BLS SE Region | Employment & wages | HTML scrape | ✅ Direct |
| 12 | Florida Health | Health data | HTML scrape | ✅ Direct |
| 13 | HealthByCounty | CDC PLACES | HTML scrape | ✅ Direct |
| 14 | BEA | GDP | API key needed | ⚠️ Key required |
| 15 | Florida DEO | Labor statistics | HTML scrape | ⚠️ Blocked |

---

## 4. RECOMMENDED NEXT STEPS

1. Build HTML scrapers for sources 3-13 above
2. Register for free Census/BLS/BEA API keys for direct access
3. Use DDGS for ongoing discovery of new sources
4. Cache all scraped data locally with freshness tracking

---

Document owner: Project Volusia Leadership
Related: DATA_CATALOG.md, REPO_SUPPORT_MATRIX.md
