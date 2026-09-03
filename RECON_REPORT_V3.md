# Project Volusia — OSINT Recon Report v3

> Expanded data source reconnaissance for Volusia County, Florida.
> Tested 2026-09-02 using DDGS search backend.
> Classification: Internal — Private Operational Intelligence

---

## 1. FEDERAL DATA SOURCES (Free APIs)

### 1.1 SAM.gov API (Government Contracts)
- **URL:** https://open.gsa.gov/api/get-opportunities-public-api/
- **Data:** Government contract opportunities, awards
- **Status:** ✅ Free public API
- **Use:** Track federal contracts in Volusia County

### 1.2 USASpending.gov API
- **URL:** https://api.usaspending.gov/
- **Data:** Federal awards, contracts, grants
- **Status:** ✅ Free API
- **Use:** Federal spending in Volusia County

### 1.3 Census Bureau APIs
- **Economic Census API:** https://www.census.gov/programs-surveys/economic-census/data/api.html
- **County Business Patterns API:** https://www.census.gov/data/developers/data-sets/cbp.html
- **Building Permits Survey:** https://www.census.gov/construction/bps/
- **Status:** ✅ Free API keys available
- **Use:** Economic data, business patterns, construction activity

### 1.4 FBI UCR Crime Data API
- **URL:** https://github.com/fbi-cde/crime-data-api
- **Data:** Uniform Crime Reports
- **Status:** ✅ RESTful API
- **Use:** Crime statistics for Volusia County

### 1.5 BLS QCEW (Quarterly Census of Employment and Wages)
- **URL:** https://www.bls.gov/cew/
- **Data:** Employment, wages, industry data
- **Status:** ✅ Free API
- **Use:** Detailed employment and wage data

### 1.6 BEA Regional Data API
- **URL:** https://apps.bea.gov/api/signup/
- **Data:** Personal income, GDP, regional economic data
- **Status:** ✅ Free API key required
- **Use:** Economic indicators for Volusia County

### 1.7 FRED API (Federal Reserve Economic Data)
- **URL:** https://fred.stlouisfed.org/docs/api/api_key.html
- **Data:** Economic time series
- **Status:** ✅ Free API key required
- **Use:** Economic indicators, unemployment, population

### 1.8 FHFA House Price Index
- **URL:** https://www.fhfa.gov/Data/Downloads/Pages/House-Price-Index-Datasets.aspx
- **Data:** House price indices
- **Status:** ✅ Free download
- **Use:** Housing price trends

### 1.9 World Bank API
- **URL:** https://datahelpdesk.worldbank.org/knowledgebase/articles/898599-indicator-api-queries
- **Data:** Global economic indicators
- **Status:** ✅ Free API
- **Use:** Contextual economic data

---

## 2. FLORIDA STATE DATA SOURCES

### 2.1 Florida FDLE Crime Statistics
- **URL:** https://www.fdle.state.fl.us/CJAB/UCR
- **Data:** Uniform Crime Reports for Florida
- **Status:** ✅ Public data
- **Use:** Crime statistics for Volusia County

### 2.2 Florida Department of Revenue (Sales Tax Data)
- **URL:** https://floridarevenue.com/dataPortal/Pages/taxresearch.aspx
- **Data:** Taxable sales, tax collections
- **Status:** ✅ Public data portal
- **Use:** Economic activity indicator

### 2.3 Florida DBPR (Business Licenses)
- **URL:** https://www.myfloridalicense.com/
- **Data:** Business license counts, types
- **Status:** ✅ Public search
- **Use:** Business formation tracking

### 2.4 Florida Department of Education (School Report Cards)
- **URL:** https://edudata.fldoe.org/ReportCards/Schools.html
- **Data:** School performance, enrollment
- **Status:** ✅ Public data
- **Use:** Education quality metrics

### 2.5 Florida Department of Health (CHARTS)
- **URL:** https://www.flhealthcharts.gov/
- **Data:** Health statistics, vital statistics
- **Status:** ✅ Public data
- **Use:** Health outcomes for Volusia County

### 2.6 FDOT Traffic Monitoring
- **URL:** https://www.fdot.gov/statistics/trafficinfo/default.shtm
- **Data:** Traffic counts, AADT
- **Status:** ✅ Public data
- **Use:** Transportation data

### 2.7 Florida Geospatial Open Data Portal
- **URL:** https://geodata.floridagio.gov/
- **Data:** GIS data, boundaries, infrastructure
- **Status:** ✅ Public data
- **Use:** Geographic data

### 2.8 Florida DEP Geospatial Open Data
- **URL:** https://geodata.dep.state.fl.us/
- **Data:** Environmental data, permits
- **Status:** ✅ Public data
- **Use:** Environmental permits, data

---

## 3. VOLUSIA COUNTY LOCAL SOURCES

### 3.1 Volusia County Open Data (ArcGIS Hub)
- **URL:** https://opendata-volusiacountyfl.hub.arcgis.com/
- **Data:** Permits, zoning, parcels, infrastructure
- **Status:** ✅ Public portal
- **Use:** Local government data

### 3.2 Volusia County Tax Collector
- **URL:** https://vctaxcollector.org/
- **Data:** Tax roll, payment records
- **Status:** ✅ Public data
- **Use:** Property tax data

### 3.3 Volusia County Sheriff (Crime Mapping)
- **URL:** https://www.vcso.us/CrimeMapping/
- **Data:** Crime incidents, statistics
- **Status:** ✅ Public data
- **Use:** Local crime data

### 3.4 Volusia County Property Appraiser
- **URL:** https://vcpa.volusia.org/
- **Data:** Parcel data, sales history, assessments
- **Status:** ✅ Public search
- **Use:** Real estate data

### 3.5 Volusia County Permit Center
- **URL:** https://www.volusia.org/services/growth-and-resource-management/building-and-zoning/permit-and-zoning-center/
- **Data:** Building permits, zoning
- **Status:** ✅ Public data
- **Use:** Construction activity

### 3.6 Volusia County Economic Development (VolusiaBusiness.org)
- **URL:** https://www.volusiabusiness.org/research-center/economy.stml
- **Data:** GDP, rankings, economic indicators
- **Status:** ✅ Public data
- **Use:** Economic development metrics

---

## 4. HEALTH DATA SOURCES

### 4.1 CDC PLACES Data Portal
- **URL:** https://www.cdc.gov/places/tools/data-portal.html
- **Data:** Health statistics by census tract
- **Status:** ✅ Public data portal
- **Use:** Health outcomes for Volusia County

### 4.2 County Health Rankings
- **URL:** https://www.countyhealthrankings.org/
- **Data:** Health rankings, outcomes, factors
- **Status:** ✅ Public data
- **Use:** Health rankings for Volusia County

### 4.3 CDC Wonder
- **URL:** https://wonder.cdc.gov/
- **Data:** Public health data, vital statistics
- **Status:** ✅ Public data
- **Use:** Detailed health statistics

### 4.4 Florida CHARTS
- **URL:** https://www.flhealthcharts.gov/
- **Data:** Florida health statistics
- **Status:** ✅ Public data
- **Use:** State-level health data

---

## 5. WEATHER & ENVIRONMENT

### 5.1 Open-Meteo Weather API
- **URL:** https://open-meteo.com/
- **Data:** Weather forecasts, historical data
- **Status:** ✅ Free, no API key required
- **Use:** Weather data for Daytona Beach

### 5.2 Visual Crossing Weather API
- **URL:** https://www.visualcrossing.com/weather-api/
- **Data:** Historical weather, forecasts
- **Status:** ✅ Free tier available (1,000 records/day)
- **Use:** Historical weather data

### 5.3 Weatherbit API
- **URL:** https://www.weatherbit.io/pricing
- **Data:** Weather forecasts, historical data
- **Status:** ✅ Free tier available (100 calls/day)
- **Use:** Weather data

### 5.4 EPA AQS API (Air Quality)
- **URL:** https://aqs.epa.gov/aqsweb/documents/data_api.html
- **Data:** Air quality measurements
- **Status:** ✅ Free API
- **Use:** Air quality data for Volusia County

### 5.5 USGS Water Data API
- **URL:** https://api.waterdata.usgs.gov/
- **Data:** Water quality, flow, levels
- **Status:** ✅ Free API
- **Use:** Water data for Volusia County

### 5.6 NOAA Tides and Currents
- **URL:** https://tidesandcurrents.noaa.gov/
- **Data:** Tidal data, currents
- **Status:** ✅ Free API
- **Use:** Coastal data for Volusia County

---

## 6. REAL ESTATE DATA SOURCES

### 6.1 Zillow Research Data
- **URL:** https://www.zillow.com/research/data/
- **Data:** ZHVI, ZORI, home values, rents
- **Status:** ✅ Free CSV downloads
- **Use:** Housing market data

### 6.2 Redfin Data Center
- **URL:** https://www.redfin.com/data-center
- **Data:** Housing market data, prices
- **Status:** ✅ Free data
- **Use:** Real estate trends

### 6.3 ATTOM Data Solutions
- **URL:** https://api.developer.attomdata.com/
- **Data:** Property data, assessments
- **Status:** ⚠️ Paid API (has free trial)
- **Use:** Detailed property data

### 6.4 FHFA House Price Index
- **URL:** https://www.fhfa.gov/
- **Data:** House price indices
- **Status:** ✅ Free download
- **Use:** Housing price trends

### 6.5 AirDNA (Short-Term Rentals)
- **URL:** https://www.airdna.co/
- **Data:** Airbnb, Vrbo rental data
- **Status:** ⚠️ Paid API
- **Use:** Tourism/rental market data

---

## 7. TRANSPORTATION DATA SOURCES

### 7.1 FDOT Traffic Monitoring
- **URL:** https://www.fdot.gov/statistics/trafficinfo/default.shtm
- **Data:** Traffic counts, AADT
- **Status:** ✅ Public data
- **Use:** Traffic volume data

### 7.2 National Bridge Inventory
- **URL:** https://www.fhwa.dot.gov/bridge/nbi.cfm
- **Data:** Bridge conditions, locations
- **Status:** ✅ Public data
- **Use:** Infrastructure data

### 7.3 National Transit Database
- **URL:** https://www.transit.dot.gov/ntd
- **Data:** Transit ridership, performance
- **Status:** ✅ Public data
- **Use:** Public transit data

### 7.4 511 API (Florida Traffic)
- **URL:** https://511.org/open-data/traffic
- **Data:** Real-time traffic
- **Status:** ⚠️ Regional API (check Florida availability)
- **Use:** Traffic conditions

---

## 8. EDUCATION DATA SOURCES

### 8.1 Florida School Report Cards
- **URL:** https://edudata.fldoe.org/ReportCards/Schools.html
- **Data:** School performance, grades
- **Status:** ✅ Public data
- **Use:** Education quality metrics

### 8.2 NCES School District Data
- **URL:** https://nces.ed.gov/ccd/schoolsearch/
- **Data:** School district demographics
- **Status:** ✅ Public data
- **Use:** Education statistics

### 8.3 Census Bureau Education Data
- **URL:** https://www.census.gov/topics/education/data.html
- **Data:** Educational attainment
- **Status:** ✅ Public data
- **Use:** Education levels

---

## 9. PUBLIC SAFETY DATA SOURCES

### 9.1 FBI UCR Crime Data API
- **URL:** https://github.com/fbi-cde/crime-data-api
- **Data:** Crime statistics
- **Status:** ✅ RESTful API
- **Use:** National crime data

### 9.2 Florida FDLE Uniform Crime Reports
- **URL:** https://www.fdle.state.fl.us/CJAB/UCR
- **Data:** Florida crime statistics
- **Status:** ✅ Public data
- **Use:** State crime data

### 9.3 Volusia County Sheriff Crime Mapping
- **URL:** https://www.vcso.us/CrimeMapping/
- **Data:** Local crime incidents
- **Status:** ✅ Public data
- **Use:** Local crime statistics

---

## 10. PRIORITY IMPLEMENTATION

### Tier 1 (Free, No Key, Immediate)
1. **Open-Meteo** — Weather (already working)
2. **Census data.census.gov** — Economic/Demographic (already working)
3. **NOAA NCEI** — Historical weather (already working)
4. **Redfin** — Housing (already working)
5. **VolusiaBusiness.org** — Economic data (already working)

### Tier 2 (Free, Key Required - Register)
1. **Census API** — Full ACS access
2. **BLS API** — Employment/wages
3. **BEA API** — Personal income, GDP
4. **FRED API** — Economic time series
5. **FBI UCR API** — Crime data

### Tier 3 (Free, Scrape/Download)
1. **SAM.gov API** — Government contracts
2. **USASpending.gov API** — Federal spending
3. **FHFA HPI** — House price index
4. **EPA AQS API** — Air quality
5. **USGS Water API** — Water data
6. **NOAA Tides** — Tidal data
7. **Florida FDLE** — Crime statistics
8. **Florida CHARTS** — Health data
9. **CDC PLACES** — Health data
10. **County Health Rankings** — Health rankings

### Tier 4 (Paid, Future)
1. **AirDNA** — Short-term rental data
2. **ATTOM Data** — Property data
3. **STR** — Hotel data

---

## 11. NEXT STEPS

1. Register for free API keys (Census, BLS, BEA, FRED, FBI)
2. Build scrapers for Tier 2 and Tier 3 sources
3. Test all endpoints for Volusia County data availability
4. Integrate into data pipeline
5. Schedule regular data refreshes

---

Document owner: Project Volusia Leadership
Related: RECON_REPORT_V2.md, DATA_CATALOG.md
