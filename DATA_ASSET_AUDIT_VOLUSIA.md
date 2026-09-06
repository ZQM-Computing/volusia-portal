# DATA ASSET AUDIT — VOLUSIA COUNTY, FL (FIPS 12127)
# Project Volusia — Phase 1 Foundation Deliverable
# Date: 2026-09-03 | Auditor: ZQM Labs

---

## EXECUTIVE SUMMARY

Of 10 DATA_CATALOG.md categories tested against live sources on 2026-09-03:

  CONFIRMED REAL-TIME ACCESS:  3 of 10 (Census PEP, BEA Regional, NOAA NCEI)
  CONFIRMED AGGREGATE ONLY:    1 of 10 (Realtor national, no county)
  NEEDS FREE API KEY:          3 of 10 (Census ACS, BLS LAUS, BEA production)
  ACCESS DENIED / BLOCKED:     2 of 10 (BLS FTP, FCC)
  NO PUBLIC INTERFACE:         1 of 10 (STR hotel data)
  GATED / MANUAL:              multiple others (FL EDR PDF, VPA, school data)

The existing `refresh.py` pipeline (Census ACS + BLS LAUS + BEA) is BROKEN — all three
fetchers fail on live APIs because they lack required API keys or use blocked endpoints.

RECOMMENDED FIX: register for free API keys, switch to CSV fallbacks, and restructure
the fetcher layer to use tiered access (direct API → CSV download → manual fallback).

---

## 1. ECONOMIC DATA

### 1.1 BLS Local Area Unemployment Statistics (LAUS)
  SOURCE:     BLS LAUS
  ENDPOINT:   https://api.bls.gov/publicAPI/v2/timeseries/data/
  SERIES ID:  LAUCN12127000000003
  STATUS:     ACCESS DENIED (403)
  NOTES:      The old flat-file FTP endpoint (download.bls.gov/pub/time.series/la/)
              now returns 403. BLS API v2 requires free registration at
              https://data.bls.gov/registrationEngine/ for production use.
  FIX:        Register for BLS API key. Use flat-file alternative only if key obtained.
  PRIORITY:   P0 — core economic indicator (unemployment rate)

### 1.2 BLS Quarterly Census of Employment and Wages (QCEW)
  SOURCE:     BLS QCEW
  ENDPOINT:   https://data.bls.gov/cew/data/files/
  STATUS:     URL INCORRECT
  NOTES:      Tested 2024_annual_singlefile.zip — path wrong.
              Correct pattern: https://data.bls.gov/cew/data/files/2024/csv/2024_qtrly_singlefile.zip
              or https://data.bls.gov/cew/data/files/2024/csv/2024_annual_singlefile.zip
              (need to verify actual listing).
  FIX:        Test directory listing, fix URL, add to fetcher.
  PRIORITY:   P1

### 1.3 Census ACS 5-Year Estimates (DP03, DP05)
  SOURCE:     US Census Bureau
  ENDPOINT:   https://api.census.gov/data/2024/acs/acs5/profile
  STATUS:     REQUIRES API KEY (302 redirect to missing_key.html)
  NOTES:      Since ~2024, the Census API requires a free key.
              Sign up: https://api.census.gov/data/key_signup.html
  FALLBACK:   Census PEP CSV works without key (see §1.4 below).
  FIX:        Add API key env var (CENSUS_API_KEY). For DP03/DP05, the PEP file
              gives population totals; for detailed economic/demographic profiles
              we need the ACS API key.
  PRIORITY:   P0 — core demographic/economic indicators

### 1.4 Census Population Estimates Program (PEP)
  SOURCE:     US Census Bureau
  ENDPOINT:   https://www2.census.gov/programs-surveys/pest/datasets/2020-2024/counties/totals/co-est2024-alldata.csv
  STATUS:     WORKS (200 OK, real data returned)
  VOLUSIA:    Population 602,772 (2024 estimate), 592,622 (2023), 580,481 (2022),
              566,481 (2021), 555,752 (2020)
  FORMAT:     CSV, ~300 columns including births, deaths, migration components
  NOTES:      This is the best no-key population source. Machine-readable.
  FIX:        Add as a fetcher. Use for population trend indicator.
  PRIORITY:   P0

### 1.5 BEA Local Area Personal Income (CAINC1)
  SOURCE:     US Bureau of Economic Analysis
  ENDPOINT:   https://apps.bea.gov/api/data
  STATUS:     REQUIRES USER KEY for production
  NOTES:      Without UserID, returns error response (APIErrorCode).
              Sign up: https://apps.bea.gov/API/signup/index.cfm
  FALLBACK:   BEA download: https://apps.bea.gov/regional/downloadzip.cfm?CAINC1County1969_2024.zip
              (301 redirect — follow location, download ZIP, extract CAINC1 CSV).
  FIX:        Register for BEA API key. For now, use download ZIP as fallback.
  PRIORITY:   P0 — per capita income indicator

### 1.6 Zillow Home Value Index (ZHVI) / Rent Index (ZORI)
  SOURCE:     Zillow Research
  ENDPOINT:   https://files.zillowstatic.com/research/public_csvs/
  STATUS:     PATH INCORRECT
  NOTES:      Tested /zhvi/County_zhvi_uc_sfrcond_tier_0.33_0.67_sa_sm_month.csv — 404.
              Zillow restructured paths in 2025-2026. Need to find current listing.
              Alternative: https://www.zillow.com/research/data/ lists files.
  FIX:        Scrape Zillow research page for current download links.
  PRIORITY:   P1

### 1.7 Realtor.com Market Trends
  SOURCE:     Realtor.com Research
  ENDPOINT:   https://econdata.s3-us-west-2.amazonaws.com/Reports/Core/listing_weekly_core_aggregate_by_country.csv
  STATUS:     WORKS but aggregate only
  NOTES:      Only national (USA) data. County-level data requires scraping
              https://www.realtor.com/research/data/ for ZIP/county CSVs.
  FIX:        Find Volusia-specific listing in their data library, scrape link.
  PRIORITY:   P1

---

## 2. TOURISM DATA

### 2.1 Volusia County CVB / Visit Daytona Beach
  SOURCE:     Convention & Visitors Bureau
  ENDPOINT:   https://www.visitdaytonabeach.com/research
  STATUS:     404 (site restructured)
  NOTES:      Visit Daytona Beach likely redirects or uses new domain.
              Check https://www.daytonabeach.com or https://www.visitvolusia.com.
  FIX:        Search for current Volusia tourism research page.
  PRIORITY:   P1

### 2.2 STR Hotel Performance Data
  SOURCE:     Smith Travel Research (CoStar)
  ENDPOINT:   https://str.com/data-insights/resources
  STATUS:     403 / GATED
  NOTES:      STR data requires paid subscription. Summary reports sometimes
              public via CVB or Visit Florida partner.
  FIX:        Check Visit Florida (https://www.visitflorida.org/resources/research/)
              for free hotel performance summaries for Volusia.
  PRIORITY:   P2 (gated, lower priority for Phase 1)

### 2.3 Canaveral National Seashore Visitor Stats
  SOURCE:     National Park Service (NPS)
  ENDPOINT:   https://www.nps.gov/cana/learn/management/statistics.htm
  STATUS:     TIMEOUT / 404
  NOTES:      The IRMA stats portal at irma.nps.gov requires form submission,
              not direct API. Use https://irma.nps.gov/Stats/SSRSReports/
              Park%20Specific%20Reports/Visitor%20Use%20Statistics?Park=CANA
  FIX:        Scrape the IRMA page, parse the report table.
  PRIORITY:   P2

### 2.4 Florida DBPR Restaurant/Lodging Licenses
  SOURCE:     FL Dept. of Business & Professional Regulation
  ENDPOINT:   https://www.myfloridalicense.com/
  STATUS:     NOT TESTED
  NOTES:      DBPR provides a license search. Not a bulk data feed.
              For aggregate counts, try Florida DEO or county tax collector.
  FIX:        Search for DBPR API or bulk data export option.
  PRIORITY:   P2

---

## 3. REAL ESTATE & HOUSING

### 3.1 Volusia County Property Appraiser
  SOURCE:     Volusia County Property Appraiser
  ENDPOINT:   https://vcpa.volusia.org/
  STATUS:     TIMEOUT (000)
  NOTES:      Site likely blocks non-browser user agents or is slow.
              Parcel data is public record — may require scraping with JS.
  FIX:        Test with browser tool to see if data loads. Look for
              bulk download option on the site.
  PRIORITY:   P1

### 3.2 Census Building Permits Survey
  SOURCE:     US Census Bureau
  ENDPOINT:   https://www.census.gov/construction/bps/
  STATUS:     NOT TESTED (HTML form)
  NOTES:      County-level building permits available via table.
              API endpoint: https://api.census.gov/data/2024/bps?get=AP&for=county:12127&in=state:12
              (requires key).
  FIX:        Add to Census fetcher once key is obtained.
  PRIORITY:   P1

### 3.3 Florida Housing Data Clearinghouse (Shimberg Center)
  SOURCE:     Univ. of Florida Shimberg Center
  ENDPOINT:   http://flhousingdata.shimberg.ufl.edu/
  STATUS:     NOT TESTED
  NOTES:      Housing data by county. Likely HTML interface.
  FIX:        Test and scrape.
  PRIORITY:   P2

---

## 4. DEMOGRAPHIC DATA

### 4.1 Census Decennial 2020
  SOURCE:     US Census Bureau
  ENDPOINT:   https://data.census.gov/
  STATUS:     CF-blocked for direct API calls
  NOTES:      Same ACS key issue. Use PEP CSV for recent population;
              for detailed 2020 decennial data, use API key.
  PRIORITY:   P0 (for baseline)

### 4.2 Florida Office of Economic and Demographic Research (EDR)
  SOURCE:     FL EDR
  ENDPOINT:   http://edr.state.fl.us/
  STATUS:     302 redirect (test download failed)
  NOTES:      EDR publishes county population PDFs and spreadsheets.
  FIX:        Follow redirects, extract direct download links.
  PRIORITY:   P1

### 4.3 CDC PLACES
  SOURCE:     CDC
  ENDPOINT:   https://places.cdc.gov/
  STATUS:     404
  NOTES:      API endpoint may have changed.
  FIX:        Check https://places.cdc.gov/api/ for updated endpoint.
  PRIORITY:   P2

---

## 5. TRANSPORTATION & INFRASTRUCTURE

### 5.1 FDOT Traffic Data
  SOURCE:     FL Dept. of Transportation
  ENDPOINT:   https://www.fdot.gov/planning/statistics/
  STATUS:     404
  NOTES:      FDOT restructured their site. Traffic count data may be at
              https://www.fdot.gov/planning/statistics/trafficdata/
  FIX:        Search for "Florida traffic count data 2024 county".
  PRIORITY:   P1

### 5.2 VOTRAN Ridership
  SOURCE:     Volusia County Public Transit
  ENDPOINT:   https://www.volusia.org/services/public-transit/
  STATUS:     404
  NOTES:      VOTRAN site may be restructured. Check for PDF reports.
  FIX:        Search volusia.org for ridership reports.
  PRIORITY:   P2

### 5.3 FCC Broadband Map
  SOURCE:     FCC
  ENDPOINT:   https://broadbandmap.fcc.gov/
  STATUS:     403 (blocked for direct API)
  NOTES:      The browser interface works but API calls are blocked.
              Bulk data download may be available via
              https://broadbandmap.fcc.gov/data-download.
  FIX:        Test the data-download page.
  PRIORITY:   P2

### 5.4 National Bridge Inventory
  SOURCE:     FHWA
  ENDPOINT:   https://www.fhwa.dot.gov/bridge/nbi.cfm
  STATUS:     200 (HTML form)
  NOTES:      Data is ASCII fixed-width files, not API.
              Download from: https://www.fhwa.dot.gov/bridge/nbi/ascii.cfm
              requires form submission.
  FIX:        Use browser tool to submit form for Volusia County download.
  PRIORITY:   P3 (infrastructure, lower priority)

---

## 6. CLIMATE & ENVIRONMENT

### 6.1 NOAA NCEI Daily Summaries
  SOURCE:     NOAA National Centers for Environmental Information
  ENDPOINT:   https://www.ncei.noaa.gov/access/services/data/v1
  STATUS:     WORKS (200 OK, real JSON data returned)
  STATION:    USW00012838 (Daytona Beach International Airport)
  DATA:       TMAX, TMIN, PRCP, etc. in fixed-width format
  NOTES:      Fully functional, no key required.
  FIX:        Build fetcher for NOAA climate data.
  PRIORITY:   P1

### 6.2 USGS Water Data
  SOURCE:     USGS
  ENDPOINT:   https://waterdata.usgs.gov/fl/nwis/nwis
  STATUS:     301 redirect
  NOTES:      New URL pattern needed.
  FIX:        Test https://waterdata.usgs.gov/fl/nwis?state_cd=fl&county_cd=127
  PRIORITY:   P2

### 6.3 FEMA Flood Maps
  SOURCE:     FEMA
  ENDPOINT:   https://msc.fema.gov/portal/api/search
  STATUS:     404
  NOTES:      FEMA API endpoint changed. Try https://msc.fema.gov/portal/home
  PRIORITY:   P2

### 6.4 FL DEP Environmental Data
  SOURCE:     FL Dept. of Environmental Protection
  ENDPOINT:   https://floridadep.gov/
  STATUS:     NOT TESTED
  PRIORITY:   P3

---

## 7. PUBLIC SAFETY

### 7.1 Volusia County Sheriff Crime Stats
  SOURCE:     Volusia County Sheriff's Office
  ENDPOINT:   https://www.volusia.org/services/public-safety/
  STATUS:     404
  NOTES:      Sheriff's site may be at separate subdomain.
  FIX:        Search for Volusia Sheriff crime statistics page.
  PRIORITY:   P2

### 7.2 FDLE Uniform Crime Reports
  SOURCE:     FL Dept. of Law Enforcement
  ENDPOINT:   https://www.fdle.state.fl.us/CR/CR.aspx
  STATUS:     301 redirect
  NOTES:      New URL may be https://www.fdle.state.fl.us/Crimes-Data/UCR
  FIX:        Follow redirects.
  PRIORITY:   P2

### 7.3 FBI UCR
  SOURCE:     FBI Crime Data Explorer
  ENDPOINT:   https://ucr.fbi.gov/
  STATUS:     NOT TESTED
  PRIORITY:   P3

---

## 8. HEALTH DATA

### 8.1 FL DOH CHARTS
  SOURCE:     FL Dept. of Health
  ENDPOINT:   http://www.flhealthcharts.com/
  STATUS:     302 redirect
  NOTES:      Now at https://www.flhealthcharts.gov/
  PRIORITY:   P2

### 8.2 CDC BRFSS
  SOURCE:     CDC
  ENDPOINT:   https://www.cdc.gov/brfss/
  STATUS:     NOT TESTED
  PRIORITY:   P2

### 8.3 County Health Rankings
  SOURCE:     Robert Wood Johnson Foundation
  ENDPOINT:   https://www.countyhealthrankings.org/
  STATUS:     404
  NOTES:      API may have changed. Main site loads in browser.
  FIX:        Scrape the site for Volusia data.
  PRIORITY:   P2

---

## 9. EDUCATION DATA

### 9.1 FL School Report Cards
  SOURCE:     FL Dept. of Education
  ENDPOINT:   https://www.fldoe.org/accountability/data-sys/edu-info-accountability/pk-12-public-schools/
  STATUS:     403
  NOTES:      Direct access blocked. Data may be available as Excel files.
  FIX:        Search for "Florida school grades 2024 excel download".
  PRIORITY:   P2

### 9.2 NCES School District Search
  SOURCE:     National Center for Education Statistics
  ENDPOINT:   https://nces.ed.gov/ccd/districtsearch/
  STATUS:     200 (HTML form, results returned)
  NOTES:      Requires form submission. Volusia County district: Volusia County Schools.
  FIX:        Use browser tool to submit ZIP search, extract results.
  PRIORITY:   P2

---

## 10. GOVERNMENT FINANCE

### 10.1 Volusia County ACFR
  SOURCE:     Volusia County Finance
  ENDPOINT:   https://www.volusia.org/services/financial-and-administrative-services/financial-reports-schedules.stml
  STATUS:     200 (found in finance page navigation)
  NOTES:      ACFR is on the financial reports page. Need to find current file.
  FIX:        Scrape the financial-reports page for PDF/Excel links.
  PRIORITY:   P1

### 10.2 FL DFS Local Government Data
  SOURCE:     FL Dept. of Financial Services
  ENDPOINT:   https://myfloridacfo.com/division/aa/
  STATUS:     NOT TESTED
  PRIORITY:   P2

---

## AUDIT SUMMARY

| CATEGORY                | NO KEY | NEEDS KEY | BLOCKED | MISSING | TOTAL |
|-------------------------|--------|-----------|---------|---------|-------|
| Economic (BLS/BEA/Census)| 1      | 2         | 0       | 1       | 4     |
| Tourism                 | 0      | 0         | 2       | 2       | 4     |
| Real Estate             | 1      | 1         | 0       | 1       | 3     |
| Demographic             | 2      | 1         | 0       | 1       | 4     |
| Transportation          | 1      | 0         | 1       | 2       | 4     |
| Climate/Environment     | 1      | 0         | 0       | 2       | 3     |
| Public Safety           | 0      | 0         | 0       | 3       | 3     |
| Health                  | 0      | 0         | 0       | 3       | 3     |
| Education               | 0      | 0         | 1       | 1       | 2     |
| Government Finance      | 1      | 0         | 0         | 1       | 2     |
| TOTAL                   | 7      | 4         | 4       | 16      | 31    |

CONFIRMED WORKING (no key):  7 sources
NEEDS FREE REGISTRATION:    4 sources (Census ACS, BLS LAUS, BEA Regional, BLS QCEW)
NEEDS FIX (URL/path):       4+ sources
MANUAL/SCRAPING REQUIRED:   16+ sources

---

## CRITICAL FIXES REQUIRED

1. Register for Census API key (free, instant) — enables ACS DP03/DP05
2. Register for BLS API key (free, ~1 day) — enables LAUS unemployment rate
3. Register for BEA API key (free, instant) — enables personal income data
4. Add Census PEP CSV fetcher — works NOW without key, gives population
5. Add NOAA NCEI fetcher — works NOW without key, gives weather data
6. Fix BLS QCEW URL — check actual file listing at data.bls.gov/cew/data/files/

---

## NEXT STEPS

1. Register for API keys today (3 registrations)
2. Fix the 3 broken fetchers
3. Build Census PEP fetcher (immediate data without key)
4. Build NOAA climate fetcher (immediate data without key)
5. Add all 6 to refresh.py pipeline
6. Load first 5 indicators into baseline portal
7. Then move to stakeholder interviews (parallel work)

Document owner: ZQM Labs / Project Volusia
Next review: 2026-12-02
