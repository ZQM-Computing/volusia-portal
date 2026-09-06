PUBLIC DATA SOURCE RECON — VOLUSIA COUNTY, FL
==============================================
Project Volusia — Open Data Inventory
ZQM Labs / Project Volusia

Version: 1.0
Date: 2026-09-02
Author: Alex Zelenski
Classification: Internal Strategic Document / Public-Facing Ready

---

0. PURPOSE AND SCOPE

This document is the consolidated output of a wide public data source
recon for Volusia County, Florida (FIPS 12127, pop ~580-590K, Deltona-
Daytona Beach-Ormond Beach MSA).

It enumerates public data sources across six domains:
  1. Economic, Labor, Business, Workforce, Industry
  2. Real Estate, Housing, Property, Construction, Land Use
  3. Tourism, Hospitality, Visitor Economy, Events, Recreation
  4. Demographics, Population, Education, Health, Public Safety
  5. Transportation, Infrastructure, Broadband, Environment, Climate
  6. Government, Public Finance, Permitting, Open Government, Elections

For each source, it records: publisher, what it provides, Volusia
coverage, access method, update frequency, license/terms, friction,
priority, why it matters for Project Volusia, and notes.

It closes each domain with a prioritized top-picks list and a
caveats/flags section.

This document feeds directly into DATA_CATALOG.md and the baseline
data portal (Q4_2026_EXECUTION_PLAN Item 3).

---

1. DOMAIN 1 — ECONOMIC, LABOR, BUSINESS, WORKFORCE, INDUSTRY

---

1.1 SOURCE LIST

### BLS — Local Area Unemployment Statistics (LAUS)
- **Publisher:** U.S. Bureau of Labor Statistics (BLS), U.S. Department of Labor
- **What it provides:** Monthly and annual employment, unemployment, and
  labor force data for counties, MSAs, cities, states, and national.
  Volusia County monthly unemployment rate, labor force, employment,
  unemployment counts. Can be pulled at the county level (FIPS 12127).
- **Volusia coverage:** DIRECT — Volusia County is a reporting county.
  Monthly series available. Also covers Deltona-Daytona Beach-Ormond
  Beach MSA as a metro area.
- **Access method:** Public API (BLS Public Data API v2), bulk flat files
  via ftp.bls.gov, web UI at bls.gov/lau, data tools (Alt+). API requires
  free registration for some series; flat files are open.
- **Update frequency:** Monthly (preliminary then revised), plus annual.
- **License/terms:** Public domain / U.S. government work. No restrictions
  on use or redistribution.
- **Friction:** LOW. API key optional for some endpoints; flat files open.
  Data has standard lag (preliminary ~1 month after reference month).
  Series IDs need to be known (e.g. area Code 12127 for Volusia County).
- **Priority:** HIGH
- **Why:** Core economic indicator for all stakeholders. Monthly
  unemployment is the single most-watched local economic metric. Feeds
  the baseline portal's first indicator set and the quarterly economic
  briefing.
- **Notes:** LAUS is a place-of-residence measure (not jobs located in
  county). Does not capture commuting in/out. Compare with CES (Current
  Employment Statistics) for establishment-based payroll employment if
  needed. BLS also publishes QCEW (below) which is more granular on
  wages and establishment counts. LAUS sample-based for counties; margins
  of error exist (see caveats).

### BLS — Quarterly Census of Employment and Wages (QCEW)
- **Publisher:** U.S. Bureau of Labor Statistics
- **What it provides:** Quarterly counts of establishments, employment,
  wages, and location by industry (NAICS) at county, MSA, state, and
  national levels. Annual averages and quarterly. Coverage down to
  county level with industry detail. High breadth — covers most
  establishments subject to UI taxes.
- **Volusia coverage:** DIRECT — Volusia County (FIPS 12127), quarterly
  and annual, by NAICS industry. Also MSA-level.
- **Access method:** BLS QCEW data tools (web UI download), flat files
  via ftp.bls.gov, BLS API for some aggregate series. Open access.
- **Update frequency:** Quarterly (with lag ~6-9 months for final).
  Annual averages published after each year.
- **License/terms:** Public domain.
- **Friction:** LOW-MEDIUM. Flat files are large and require parsing.
  API access to granular QCEW is more limited than LAUS. Confidentiality
  rules suppress very small cells (no individual employer identification,
  small industry x county cells may be suppressed). Value: very high for
  industry composition analysis.
- **Priority:** HIGH
- **Why:** Industry structure, wages by sector, establishment counts —
  direct input to business owner benchmarks, industry mover intelligence,
  and the "is this industry growing?" question. Superior to LAUS for
  industry detail.
- **Notes:** QCEW is an administrative data source (UI records), largely
  complete but subject to some coverage gaps (very small employers,
  certain industries). Suppressed cells require attention when analyzing
  small geographies or niche industries.

### BLS — Occupational Employment and Wage Statistics (OES)
- **Publisher:** U.S. Bureau of Labor Statistics
- **What it provides:** Employment and wage estimates by occupation at
  the MSA level (and state/national). Median, mean, percentiles by
  occupation. Useful for workforce skill and wage analysis.
- **Volusia coverage:** MSA-level — Deltona-Daytona Beach-Ormond Beach
  MSA. Not county-only (OES is MSA or higher). Still highly relevant —
  Volusia is the dominant part of this MSA.
- **Access method:** BLS web UI (OES data tools), downloadable tables.
  Public.
- **Update frequency:** Annual (most recent reference period ~1 year old
  at publication; e.g. May 2024 data published in spring 2025).
- **License/terms:** Public domain.
- **Friction:** LOW. Web UI download. Lag notable (annual, ~1 year behind).
- **Priority:** MEDIUM-HIGH
- **Why:** Workforce wage benchmarks by occupation for residents, job
  seekers, educators, and industry movers. Answers "what occupations
  pay what in this market?"
- **Notes:** MSA-level only (not pure Volusia County). Use alongside
  QCEW and ACS for triangulation. OES is a sample survey, not a census.

### BEA — Local Area Personal Income (LAPI) / CAINC1
- **Publisher:** U.S. Bureau of Economic Analysis (BEA), U.S. Department
  of Commerce
- **What it provides:** Personal income by county, MSA, state, metro, and
  nation — total personal income, disposable personal income, population,
  per capita personal income, earnings by industry (NAICS), property
  income, transfer receipts, etc. Component detail (wages and salaries,
  supplements, proprietor income, etc.).
- **Volusia coverage:** DIRECT — Volusia County (FIPS 12127), annual.
  Also MSA.
- **Access method:** BEA API (free, requires registration), web download
  (BEA data tools), flat files, BEA Regional Data API. Public.
- **Update frequency:** Annual, typically released spring of following
  year (e.g. 2024 data released in 2025). Some quarterly state/national
  series but county is annual.
- **License/terms:** Public domain.
- **Friction:** LOW. API access is straightforward once registered.
  Historical depth is good (decades). Lag is annual.
- **Priority:** HIGH
- **Why:** County-level income and earnings trends are a core economic
  indicator. Personal income by source (wages, transfers, proprietor,
  etc.) tells the income composition story. Compare vs. peers. Essential
  for the quarterly and annual economic briefings and the industry mover
  intelligence brief.
- **Notes:** BEA personal income is a measure of income received, not
  GDP/output. For output/GDP at county level, BEA publishes county GDP
  (see below). Both are useful.

### BEA — Gross Domestic Product by County (GDP by County)
- **Publisher:** U.S. Bureau of Economic Analysis
- **What it provides:** GDP (gross domestic product) by county — total
  GDP, GDP by industry (NAICS), GDP per capita. Measures economic output
  located in the county (not residence-based like personal income).
- **Volusia coverage:** DIRECT — Volusia County, annual.
- **Access method:** BEA API, web download, flat files. Public.
- **Update frequency:** Annually (released ~1 year after reference year;
  e.g. 2023 GDP released in 2024). Recent years subject to revision.
- **License/terms:** Public domain.
- **Friction:** LOW. Same BEA access infrastructure as LAPI.
- **Priority:** HIGH
- **Why:** The most direct measure of county economic output and industry
  shares. Complements personal income (which is residence-based). Key
  for "is the county economy growing" and industry mix analysis.
- **Notes:** County GDP has a long lag and revisions. Use with LAUS/QCEW/
  ACS for a fuller picture. Combine with BEA industry earnings for
  detail.

### U.S. Census Bureau — American Community Survey (ACS) 5-Year Estimates
- **Publisher:** U.S. Census Bureau
- **What it provides:** Annual survey estimates for demographics, housing,
  economic characteristics (income, employment, occupation, industries,
  class of worker, commute, poverty, etc.), education, and more — at
  census tract, ZIP (ZCTA), county, state, and national levels. Key
  tables for economic analysis: DP03 (economic characteristics),
  S1901 (income), S2301 (employment status), S0801 (commuting),
  DP05 (demographics), plus occupational and industry tables (S2601,
  S2501, etc.).
- **Volusia coverage:** DIRECT — Volusia County, census tracts, ZCTAs.
  5-year estimates are the most reliable for small geographies (tracts).
  1-year estimates available for Volusia County but with larger margins
  of error; tracts require 5-year.
- **Access method:** Census Bureau API (free, no key required for many
  endpoints but recommended), data.census.gov web UI (download tables),
  FTP, Census data products. API is the preferred programmatic access.
- **Update frequency:** ACS 5-year estimates released annually (new
  release each December, covering 5-year pooled period ending 2 years
  prior; e.g. 2019-2023 released December 2024). ACS 1-year released
  annually with ~1 year lag.
- **License/terms:** Public domain (U.S. government).
- **Friction:** LOW-MEDIUM. API is well-documented and accessible. Data
  tools web UI is user-friendly for downloads. Caveats on survey error,
  especially for tract-level estimates (large relative MOEs). ACS does
  not cover everything (see caveats).
- **Priority:** HIGH
- **Why:** Primary source for tract-level demographic and economic
  characteristics. Only source with tract resolution for income,
  employment, occupation, industry, poverty, commuting for the whole
  population. Essential for maps (Map folder), resident analysis, and
  small-area economic patterns.
- **Notes:** ACS 5-year estimates are NOT a point-in-time snapshot — they
  are an average over a 5-year period. Margins of error matter at tract
  level. ACS 1-year has better timeliness but worse small-area reliability
  (county-level is okay; tract is not). Use the Census API with the area
  parameter for Volusia County (state=12, county=127).

### U.S. Census Bureau — County Business Patterns (CBP)
- **Publisher:** U.S. Census Bureau (from administrative data: Business
  Register / payroll UI)
- **What it provides:** Annual statistics on number of establishments,
  employment, and payroll by industry (NAICS) at county, ZIP, place,
  MSA, state, and national. Covers most non-farm businesses with
  payroll.
- **Volusia coverage:** DIRECT — Volusia County, ZIP codes, places.
- **Access method:** Census Bureau API, data.census.gov, Census FTP.
  Public.
- **Update frequency:** Annual (released ~1 year after reference year).
- **License/terms:** Public domain.
- **Friction:** LOW. API and web UI. Lag annual.
- **Priority:** MEDIUM-HIGH
- **Why:** Business density, industry composition, establishment counts
  by ZIP/tract — useful for business owner dashboards (competition
  landscape), economic maps (business density), industry mover analysis.
  Complements QCEW (which is broader and has wages; CBP has payroll and
  geography down to ZIP/place).
- **Notes:** CBP excludes some business types (e.g. some non-employer
  businesses without payroll, certain industries). Suppressed cells for
  small areas/industries. Compare with QCEW for completeness.

### U.S. Census Bureau — Business Formation Statistics (BFS)
- **Publisher:** U.S. Census Bureau (from IRS business formation data)
- **What it provides:** Monthly and annual business applications and
  formations (new business starts) at state and national level. New
  Business Trends. High-frequency indicator of entrepreneurial activity.
- **Volusia coverage:** STATE-level only (Florida). Not county. Limited
  direct Volusia coverage, but Florida BFS is useful context for
  comparing Volusia's environment to state trends and national.
- **Access method:** Census Bureau website (BFS page), CSV/Excel downloads,
  API (some series). Public.
- **Update frequency:** Monthly (with lag ~1-2 months).
- **License/terms:** Public domain.
- **Friction:** LOW.
- **Priority:** MEDIUM
- **Why:** Business formation trend context. Florida-level formation
  trends inform investor/developer outlook and small business climate
  narrative. Not county-level, so use as context, not direct Volusia
  indicator.
- **Notes:** County-level business formation data is harder to get
  publicly at high frequency. BEA/County Business Patterns have
  establishment counts but not formation dynamics. See also state/local
  business license data (Volusia County business tax receipts, DBPR
  licenses — those are local/state sources, see Domain 6).

### Local Area Personal Income (LAPI) — County/State detail (BEA)
- **Publisher:** BEA
- **What it provides:** (already covered above in BEA LAPI; this line is a
  reminder that BEA also publishes detailed earnings by industry and
  transfer receipts which are valuable for Volusia.)
- **Volusia coverage:** DIRECT at county level.
- **Notes:** Industry earnings detail from BEA is a strong complement to
  QCEW industry wages.

### Bureau of Economic Analysis — REIS / economic profile
- **Publisher:** BEA
- **What it provides:** County Economic Profiles (detail on income,
  employment, population, industry). Part of BEA's regional data.
- **Volusia coverage:** DIRECT — county.
- **Notes:** Good summary product; BEA API provides the underlying series.
  Use API for programmatic use; web UI for quick profiles.

### Florida Department of Economic Opportunity (DEO) — Labor Market
Statistics / FloridaJobs.com Labor Market Information
- **Publisher:** Florida Department of Economic Opportunity (DEO), Division
  of Workforce Innovation / Labor Market Statistics
- **What it provides:** Florida and county-level employment, unemployment,
  labor force, industry data, occupational data, employment projections,
  workforce indicators, CareerSource Florida region data. Often mirrors
  or supplements BLS with Florida-specific detail and sometimes faster
  local turnaround. Includes Florida unemployment by county, industry
  employment, and labor market regions.
- **Volusia coverage:** DIRECT — Volusia County and Volusia County as part
  of a Florida labor market region.
- **Access method:** FloridaJobs.org labor market information pages,
  DEO website, data downloads, some API. Public.
- **Update frequency:** Monthly (employment/unemployment), plus periodic
  publications (annual/county profiles, projections).
- **License/terms:** Public (Florida state government).
- **Friction:** LOW-MEDIUM. Web access good; some data behind state
  portals. May have Florida-specific series not in BLS (e.g. employment
  by industry at county level with Florida detail).
- **Priority:** MEDIUM-HIGH
- **Why:** State-level labor market detail, Florida workforce context,
  local labor market region data. Helpful companion to BLS; sometimes
  provides more Florida-relevant breakdowns. Industry movers and business
  owners care about local labor market conditions.
- **Notes:** Florida has CareerSource Florida network (local workforce
  development boards) which may have additional local workforce data —
  Volusia is served by a CareerSource board (CareerSource Volusia/Flagler?
  — verify exact name). That local workforce board may have job seeker/
  employer data that is less public. Note as potential source with access
  friction.

### Florida Office of Economic and Demographic Research (EDR)
- **Publisher:** Florida Legislature / Office of Economic and Demographic
  Research (edr.state.fl.us)
- **What it provides:** Florida population projections (county-level),
  demographic estimates, economic and revenue forecasts for Florida —
  including county-level population projections, district-level data,
  and analysis supporting legislative decisions. County population
  projections are a valuable forward-looking demographic source.
- **Volusia coverage:** DIRECT — Volusia County population projections
  and estimates.
- **Access method:** EDR website (edr.state.fl.us), reports, data tables,
  some downloadable data. Public.
- **Update frequency:** Annual/Biennial (population projections updated;
  revenue forecasts periodic).
- **License/terms:** Public (Florida state government).
- **Friction:** LOW-MEDIUM. Reports and tables downloadable.
- **Priority:** MEDIUM
- **Why:** Forward-looking population projections for Volusia County —
  essential for planning, resident demographic outlook, and feeding
  demand models. Deeper and more Florida-specific than Census PEP
  projections.
- **Notes:** Florida EDR projections are widely used in Florida planning.
  Compare with Census Population Estimates Program (PEP) and ACS.

### U.S. Bureau of Labor Statistics — Current Employment Statistics (CES)
- **Publisher:** BLS
- **What it provides:** Monthly payroll employment, hours, earnings by
  industry (NAICS supersectors) at state and metro area level (and
  national). Not county-level for CES (CES is state and MSA); for
  county detail use QCEW.
- **Volusia coverage:** MSA-level — Deltona-Daytona Beach-Ormond Beach MSA.
  State of Florida also.
- **Access method:** BLS data tools, API, flat files. Public.
- **Update frequency:** Monthly (monthly employment by industry, with lag).
- **License/terms:** Public domain.
- **Friction:** LOW.
- **Priority:** MEDIUM
- **Why:** Monthly employment by industry at MSA level — faster than QCEW
  for tracking recent employment shifts at the MSA scale. Useful
  complement to LAUS and QCEW.
- **Notes:** Not county-specific; MSA includes Flagler County portion.
  Use QCEW for county and NAICS detail. CES is sample-based.

### Regional Economic Accounts / Input-Output / IMPLAN (industry multipliers)
- **Publisher:** IMPLAN (private, subscription) — NOT public. Mention for
  completeness: economic impact modeling and multipliers are valuable
  for event/ project impact analysis, but IMPLAN is a paid tool.
- **Public alternative:** BEA can provide some industry multiplier context;
  Census and BEA data can feed simple multipliers. County-level economic
  impact studies are sometimes published by CVBs or consultants (see
  tourism economic impact reports in Domain 3) — those are public outputs
  even if the underlying model is private.
- **Friction:** HIGH for public (no free county-level I-O model).
- **Priority:** LOW as a data source (no public equivalent at county
  resolution). Economic impact reports using IMPLAN are published by
  others and may be public PDFs.
- **Notes:** If Project Volusia needs economic impact analysis for an
  event or project, look for existing published studies (CVB economic
  impact reports, university studies) rather than building an I-O model
  from scratch. Those studies may use IMPLAN but the outputs are public.

### U.S. Census Bureau — Nonemployer Statistics (NES)
- **Publisher:** Census Bureau
- **What it provides:** Annual data on nonemployer businesses (businesses
  with no paid employees, e.g. sole proprietorships, freelancers) by
  industry at county, state, ZIP, place levels.
- **Volusia coverage:** DIRECT — Volusia County, ZIP, places.
- **Access method:** Census API, data.census.gov, FTP. Public.
- **Update frequency:** Annual.
- **License/terms:** Public domain.
- **Friction:** LOW.
- **Priority:** MEDIUM
- **Why:** Sole proprietors and nonemployers are a huge part of small
  business landscape. CBP misses them (they have no payroll). NES fills
  that gap. Relevant for small business owners, business density mapping,
  local economy characterization.
- **Notes:** Combine CBP (employer businesses) + NES (nonemployers) for a
  more complete business count by industry. Both are Census Bureau.

### IRS — Statistics of Income (SOI) — County Business / Income data
- **Publisher:** IRS Statistics of Income Division
- **What it provides:** County-level business data (business patterns by
  county from IRS admin data), county income data (adjusted gross income
  by county, income tax returns, etc.). Some data at county level.
- **Volusia coverage:** DIRECT — Volusia County.
- **Access method:** IRS SOI website, data tables, some downloadable data.
  Public but may lag.
- **Update frequency:** Annual, with significant lag (multi-year).
- **License/terms:** Public domain (U.S. government).
- **Friction:** MEDIUM — IRS SOI data is public but not as easily
  programmatic as Census/BLS; some tables are in PDF/Excel reports.
- **Priority:** LOW-MEDIUM
- **Why:** Alternative income and business source. Can fill gaps or
  triangulate. Not a primary source for Project Volusia given better
  alternatives (BEA, ACS, QCEW), but worth knowing.
- **Notes:** IRS SOI county data is useful for income distribution and
  business counts, but lags and access friction make it supplementary.

### Bureau of Economic Analysis — Foreign Direct Investment (FDI) / BE-12
- **Publisher:** BEA
- **What it provides:** FDI data by state and some local (county-level may
  be limited). BE-12 is survey of foreign-owned businesses; BEA publishes
  aggregates.
- **Volusia coverage:** Limited direct county; Florida FDI is available.
- **Access method:** BEA website, BEA FDI data.
- **Priority:** LOW for Volusia-specific; Florida FDI is context.
- **Notes:** Industry movers interested in foreign investment may want
  this, but county-level FDI is sparse publicly.

### Florida Department of Revenue — Tax Data / Sales Tax / Tourist
Development Tax
- **Publisher:** Florida Department of Revenue (DOR) — fldor.org
- **What it provides:** Florida sales tax collections by county (consumer
  confidence proxy, tourist spending proxy via tourist development tax),
  county tax data, local government tax data. Florida DOR publishes
  monthly/annual sales tax and other tax collections by county. Tourist
  Development Tax (bed tax) collections by county are relevant to tourism
  economy (see Domain 3 and Domain 6).
- **Volusia coverage:** DIRECT — Volusia County tax collections.
- **Access method:** Florida DOR website, data reports, monthly/annual
  tax collection reports. Public.
- **Update frequency:** Monthly/annual.
- **License/terms:** Public (Florida state government).
- **Friction:** LOW-MEDIUM. Reports and data available; may need to parse
  published reports.
- **Priority:** MEDIUM
- **Why:** Sales tax collections are a high-frequency proxy for consumer
  spending and tourism spending at the county level. Tourist development
  tax is directly tied to tourism economy. Useful for tourism and economic
  monitoring.
- **Notes:** DOR data is a proxy, not a direct measure. Combine with
  CVB tourism data for triangulation. Sales tax excludes some categories
  (e.g. groceries, some services). See Domain 6 for local tourist
  development tax administration.

### U.S. Census Bureau — Annual Survey of State and Local Government
Finances (partly economic)
- **Publisher:** Census Bureau
- **What it provides:** Government finance data (covered in Domain 6). Some
  economic relevance (government employment, government spending as share
  of economy). Covered under Domain 6.

---

1.2 TOP PICKS FOR PROJECT VOLUSIA — ECONOMIC/LABOR/BUSINESS/WORKFORCE

1. BLS LAUS — monthly county unemployment (HIGH — baseline portal core)
2. BLS QCEW — quarterly county employment/wages by industry (HIGH —
   industry structure, wages)
3. BEA LAPI (CAINC1) — county personal income by source, annual (HIGH —
   income trends)
4. BEA GDP by County — county output by industry, annual (HIGH — output
   and industry shares)
5. Census ACS 5-Year — tract-level economic + demographic (HIGH — small
   area resolution, maps)
6. Census County Business Patterns — establishment counts by industry at
   county/ZIP (MEDIUM-HIGH — business density)
7. Census Nonemployer Statistics — sole proprietors by industry (MEDIUM —
   complete business count)
8. Florida DEO labor market statistics — Florida/county labor market detail
   (MEDIUM-HIGH — companion to BLS, Florida-specific)
9. Florida EDR population projections — forward-looking county population
   (MEDIUM — planning, demand)
10. BLS OES — MSA occupation wages (MEDIUM-HIGH — workforce wages)
11. BLS CES — MSA monthly employment by industry (MEDIUM — faster MSA
    employment signal)
12. Florida DOR sales tax / tourist tax collections — county spending proxy
    (MEDIUM — consumer/tourism spending proxy)

---

1.3 CAVEATS AND FLAGS — ECONOMIC/LABOR/BUSINESS

- LAUS county unemployment is survey-based at county level; small counties
  have larger sampling error. Volusia County (pop ~580K) is large enough
  for reasonably reliable monthly LAUS, but treat monthly fluctuations
  with caution; look at trends. ACS-based unemployment (S2301) is
  complementary but annual.
- LAUS is residence-based (people who live in Volusia and are employed/
  unemployed). It does NOT measure jobs located in Volusia. Commuters
  out and in are not visible. QCEW and CES measure jobs/establishments
  located in the area (establishment-based). Use both for a complete
  picture.
- QCEW is comprehensive but has suppressions for small cells; some
  industry x county cells may be missing. Wages are total annual wages /
  employment (average, not median). Use with ACS occupation/industry data
  for median context.
- BEA personal income is residence-based income received; BEA GDP is
  output located in the area. They differ for communities with high
  commuter inflows or outflows, retiree communities (transfers), etc.
- ACS margins of error matter. At tract level, many estimates have MOEs
  that are a large fraction of the estimate. Report with MOEs or use
  the "compare" features carefully. Do not over-interpret small tract
  differences.
- ACS 1-year vs 5-year tradeoff: timeliness vs. small-area reliability.
  For Volusia County level, 1-year is usable. For tracts, 5-year only.
  Be explicit which vintage you're using.
- Business Formation Statistics are Florida-level only, not county.
- Industry classification differences: NAICS codes differ in detail between
  sources (QCEW may use more detailed NAICS than some ACS tables). Be
  careful when comparing across sources.
- High-frequency indicators (LAUS monthly, CES monthly, BFS monthly) are
  useful for recent trends but are noisy. Annual data (BEA, QCEW annual,
  ACS, CBP) are more stable.
- Economic impact studies: some are published by CVBs, consultants, or
  universities using private models (IMPLAN, etc.). The published report
  is public; the model is not. Use with caution and note the source.
- Tourism economic impact is covered in Domain 3 but overlaps here —
  tourist spending (CVB reports, DOR tourist tax) is an economic indicator
  too.

---

2. DOMAIN 2 — REAL ESTATE, HOUSING, PROPERTY, CONSTRUCTION, LAND USE

---

2.1 SOURCE LIST

### Zillow Research — ZHVI, ZORI, and market data
- **Publisher:** Zillow Research (Zillow Group)
- **What it provides:** Zillow Home Value Index (ZHVI) — typical home value
  (35th-65th percentile) by geography; Zillow Observed Rent Index (ZORI)
  — typical asking rent by geography; plus for-sale inventory, new
  listings, median list/sale price, days to pending, sale-to-list ratio,
  market heat index, rental inventory, etc. Geography: national, state,
  metro, county, city, ZIP, neighborhood. ZHVI from Jan 2000; ZORI from
  ~2015; most series monthly.
- **Volusia coverage:** DIRECT — Volusia County (county-level ZHVI/ZORI),
  ZIP-level (many Volusia ZIPs), city-level (Daytona Beach, DeLand, New
  Smyrna Beach, Ormond Beach, Port Orange, Deltona, etc.), neighborhood
  where available. Zillow has data for Volusia County cities and ZIPs.
- **Access method:** Public CSV downloads — NO API key required. Files at
  files.zillowstatic.com/research/public_csvs/<metric>/. Data page at
  zillow.com/research/data lists the download links. Bulk CSVs, one per
  metric, wide format (id columns + one column per month). No sign-up.
  Web UI at zillow.com/research/data for browsing.
- **Update frequency:** Monthly (ZHVI/ZORI updated monthly; some series
  weekly).
- **License/terms:** Free to download and use. Zillow requests citation.
  Not open-source licensed per se, but no cost, no key, no rate limit.
  Zillow's terms: use for analysis; attribution requested. Not public
  domain but effectively open for analysis use. (Check current terms —
  Zillow research data page states citation requested.)
- **Friction:** LOW. Direct CSV downloads, no key, no auth. Files are
  wide-format CSVs, need to parse (columns are months). Geography
  identifiers are Zillow's internal geography IDs; match to ZIP/county/
  city via metadata or the Zillow-provided geo files. Neighborhood-level
  data may not exist for all Volusia neighborhoods (coverage varies).
- **Priority:** HIGH
- **Why:** Home values and rents at county, city, and ZIP resolution are
  core to the real estate/housing picture for residents, business owners,
  and investors. The most accessible public-ish housing market data with
  good time series and geography resolution. Feeds the baseline portal,
  real estate maps, and the housing affordability analysis.
- **Notes:** ZHVI is a smoothed, seasonally adjusted index of typical home
  value (mid-tier, 35-65th percentile), NOT the median sale price of
  actually closed transactions (though Zillow also publishes median sale
  price at metro level). ZORI is an index of observed rents (asking rents
  of listed rentals), quality-adjusted. These are model-based indices,
  not raw transaction data. Understand methodology before using as
  authoritative transaction prices. Zillow's "median sale price" series
  is at metro level only (not county/ZIP). For actual transaction prices
  at county level, use the Volusia Property Appraiser sales data (below)
  or public records. Zillow indices are excellent for trends but are not
  raw deed data.

### Realtor.com Research & Insights
- **Publisher:** Realtor.com (News Corp / Move, Inc.)
- **What it provides:** Market trends data — median list price, median
  sale price, days on market, inventory, price cuts, new listings, by
  metro and some other geographies. Some data downloadable.
- **Volusia coverage:** Likely MSA (Daytona Beach MSA) level — county/city
  resolution may be limited. Verify current coverage.
- **Access method:** Realtor.com research page, data downloads (some
  free), reports. Some data may require sign-up or have limited free
  access.
- **Update frequency:** Monthly (for key series).
- **License/terms:** Public-ish (research data available; terms vary).
- **Friction:** MEDIUM — some data free, some gated. MSA resolution.
- **Priority:** MEDIUM
- **Why:** Alternative market metrics (days on market, list vs sale price,
  inventory) that complement Zillow. Good for triangulation. MSA-level
  may be limiting for tract/ZIP work.
- **Notes:** Confirm geography coverage for Volusia before treating as
  primary. Realtor.com data comes from MLS listings (may not capture
  all transactions, especially off-market or cash).

### U.S. Census Bureau — Building Permits Survey (BPS)
- **Publisher:** U.S. Census Bureau
- **What it provides:** Annual and monthly building permits data —
  new private housing units authorized by building permits, by
  geography (state, county, MSA, place, ZIP) and by type (1-unit, 2-4
  unit, multifamily), and sometimes by characteristics. Covers permit-
  issuing places.
- **Volusia coverage:** DIRECT — Volusia County, places (cities), ZIP.
  Permit-issuing jurisdictions within Volusia report to BPS.
- **Access method:** Census Bureau API, data.census.gov, Census FTP,
  web UI. Public.
- **Update frequency:** Monthly (preliminary) and annual (final).
- **License/terms:** Public domain.
- **Friction:** LOW. API and web UI. Data is permit counts, not unit
  addresses (so it's an aggregate, not parcel-level). Geography is
  place/county/ZIP.
- **Priority:** HIGH
- **Why:** Construction activity indicator — new housing supply. Building
  permits are a leading indicator of housing development and a direct
  measure of construction pipeline. Useful for residents (housing supply),
  investors (development activity), and the real estate/housing analysis.
  Feeds into the "is housing supply keeping up" question.
- **Notes:** Building permits are not the same as starts or completions
  (permits precede starts and completions). Some jurisdictions are
  non-permit-issuing and are imputed. BPS covers new residential only
  (not commercial). For commercial construction, see other sources.

### Volusia County Property Appraiser (VCPA) — Parcel Data, Sales,
Assessments
- **Publisher:** Volusia County Property Appraiser's Office (vcpa.vcgov.org)
- **What it provides:** Parcel-level property data — ownership, assessed
  value, property characteristics (land use, square footage, year built,
  beds/baths, etc.), legal description, parcel boundaries (GIS), sales
  history, tax roll data (working tax roll and prior years final tax
  roll). Weekly working tax roll extract and annual final tax roll.
  Sales search (recent sales). Parcel ID system. Custom map/data requests
  available (for a fee).
- **Volusia coverage:** DIRECT — Volusia County, parcel-level, all
  parcels. Also city-level via parcel data.
- **Access method:** 
  - Public access web search (by owner, parcel ID, address, map search)
    at vcpa.vcgov.org.
  - Database download: Microsoft Access database of the working tax roll
    (updated weekly) and prior years' final tax rolls, available on the
    Downloads page (vcpa.vcgov.org/download). Zip file with Access DB.
  - GIS/parcel layer: Volusia County Open Data portal (ArcGIS Hub) has
    Parcels feature layer (polygon) via ArcGIS REST API / GeoJSON / 
    downloadable. URL: opendata-volusiacountyfl.hub.arcgis.com/datasets/
    parcels-1/about. ArcGIS REST endpoint: maps5.vcgov.org/arcgis/rest/
    services/Open_Data/Open_Data_3/FeatureServer/36 (Parcels layer).
  - Custom data/map requests: email VCPA@Volusia.org; fee-based (e.g.
    $25 data delivery via email, $40/hr programming fee). Two-week
    turnaround for custom map requests.
- **Update frequency:** Weekly working tax roll extract; annual final
  tax roll; parcel GIS layer updated as maintained. Sales data updated
  as recorded.
- **License/terms:** Public record (Florida law — property appraiser data
  is public record). Some custom services have fees. Free downloads.
- **Friction:** MEDIUM. Access database (Access format) requires MS Access
  or conversion to parse; GIS parcel layer is accessible via ArcGIS REST/
  GeoJSON and can be used with geopandas/QGIS. Custom data requests have
  fees and turnaround. Parcel data is rich and authoritative but the
  database format requires processing. GIS parcel layer may not include
  all the attribute data (assessment values, etc.) — combine with tax
  roll data.
- **Priority:** HIGH
- **Why:** The authoritative local source for property, parcel, assessment,
  and sales data. Parcel-level resolution is essential for real estate
  maps, property analysis, land use, housing value distribution, and
  property tax context. Far more granular and local than Zillow.
- **Notes:** VCPA data is Florida public record — it is genuinely public
  and accessible. The weekly Access DB is the most current tax roll.
  The parcel GIS layer from the Open Data portal is the geometry. Combine
  for a complete picture. Custom data requests (e.g. "all parcels with
  X") are available for a fee if the public download doesn't serve a
  specific need. See also FL Assessment / Just Values reports (VCPA
  publishes "Just Values" estimate reports — June 1 estimate, e.g.
  vcpa.vcgov.org/files/historical/2026/VCARD.pdf).

### Zillow Transaction & Assessment Dataset (ZTRAX) — DISCONTINUED /
GATED
- **Publisher:** Zillow (formerly)
- **What it provides:** Parcel-level transaction and assessment microdata
  (deed-level). Was a separate academic/research dataset with application
  gate.
- **Volusia coverage:** Was national/county/parcel-level.
- **Status:** DISCONTINUED for new agreements (per Zillow research data
  documentation). No longer available as a free/public source.
- **Priority:** N/A — unavailable. Note for completeness: ZTRAX is no
  longer an option. Use VCPA sales data + public records for parcel-level
  transaction data instead.
- **Notes:** Don't spend time pursuing ZTRAX. Already discontinued.

### Realtor.com / ATTOM / CoreLogic / other private real estate data
- **Publisher:** Various private companies (ATTOM, CoreLogic, Black Knight,
  etc.)
- **What they provide:** Parcel-level or address-level real estate data,
  transaction history, valuations, tax data, liens, etc.
- **Volusia coverage:** Yes, typically national with county/parcel detail.
- **Access method:** Subscription / commercial. NOT public.
- **Priority:** Mention as gated alternatives. Not for Project Volusia
  as public sources. If a specific dataset becomes available via
  partnership or open release, reassess.
- **Notes:** These are the commercial-grade sources. Project Volusia's
  charter emphasizes open/public data. If a specific private dataset
  proves essential and no public equivalent exists, that's a flag to
  evaluate cost/benefit, but default is public.

### Florida Department of Revenue — Property Tax / Assessment Data
- **Publisher:** Florida Department of Revenue (DOR), Division of
  Accounting and Financial Reporting
- **What it provides:** Florida property tax data — assessed values,
  millage rates, tax collections by county and taxing authority. Some
  data by county. Florida DOR publishes property tax statistics.
- **Volusia coverage:** DIRECT — Volusia County, and individual taxing
  authorities (cities, school board, special districts) within Volusia.
- **Access method:** Florida DOR website, reports, data downloads.
  Public.
- **Update frequency:** Annual (tax year data).
- **License/terms:** Public (Florida state government).
- **Friction:** LOW-MEDIUM. Published reports and tables.
- **Priority:** MEDIUM
- **Why:** Property tax is a real cost for residents and businesses.
  Millage rates and assessed values by jurisdiction help answer "what's
  the tax burden" and "how do cities compare." Useful for residents and
  business owners. For parcel-level assessment detail, VCPA is better
  (more granular).
- **Notes:** Use VCPA for parcel-level; FL DOR for county/jurisdiction
  aggregate tax stats. The Volusia County ACFR (see Domain 6) also has
  property tax revenue in the government finance picture.

### Volusia County — Building & Zoning / Permits (Growth and Resource
Management)
- **Publisher:** Volusia County Growth and Resource Management Department,
  Building and Code Administration / Permit Center
- **What it provides:** Building permits, zoning, land use, code
  enforcement. Permit Center online (volusia.org/services/growth-and-
  resource-management/building-and-zoning/permit-and-zoning-center).
  Permit data may include permit applications, issued permits, inspections.
  Zoning maps and land use designations.
- **Volusia coverage:** DIRECT — Volusia County (unincorporated) and
  potentially city permits if integrated. County building permits.
- **Access method:** Online Permit Center (web UI), some data may be
  accessible via GIS/Open Data portal (see Volusia County Open Data
  portal and ArcGIS — zoning layers, 토지 sử dụng). Public records.
  Some data may require interaction with the Permit Center or public
  records request.
- **Update frequency:** Real-time/as permits issued; data availability
  depends on system.
- **License/terms:** Public record (Florida). Some system access may be
  interactive.
- **Friction:** MEDIUM. The Permit Center is an interactive system;
  bulk permit data may not be trivially downloadable (may need to query
  or request). Zoning/land use GIS layers may be on the Open Data portal.
- **Priority:** HIGH for permitting velocity and land use; MEDIUM for
  bulk data access (depends on what's downloadable).
- **Why:** Permitting velocity is a key industry mover indicator (how fast
  can development happen?). Zoning/land use is critical for development
  analysis, real estate, and land use maps. Building permits are also
  captured in Census BPS but county permit data has local detail (permit
  type, address, status).
- **Notes:** Verify what permit data is actually bulk-accessible vs.
  interactive-only. The Census BPS is the easy public proxy for building
  permit counts by geography. County-level detail (address-level permits,
  permit status, inspection) may require interaction with the Permit
  Center or a public records request. Addresses the "is the permitting
  process fast or slow" question that industry movers care about.

### Volusia County — Land Use / Zoning / Comprehensive Plan
- **Publisher:** Volusia County Growth and Resource Management / Planning
  Division
- **What it provides:** Official land use designations (comprehensive plan),
  future land use map, zoning maps, zoning codes, planning documents.
- **Volusia coverage:** DIRECT — Volusia County (unincorporated) land use
  and zoning. Cities have their own comprehensive plans/zoning.
- **Access method:** Volusia County website, GIS/Open Data portal (zoning
  GIS layers), planning documents. Public.
- **Update frequency:** Land use/zoning changes with amendments; GIS layers
  updated periodically.
- **License/terms:** Public.
- **Friction:** LOW-MEDIUM. GIS layers on Open Data portal preferred for
  programmatic use. Planning documents may be PDFs.
- **Priority:** HIGH
- **Why:** Official land use and zoning is the regulatory foundation for
  development analysis. Essential for industry movers (where can I build
  what?), real estate (what can be built here?), and land use maps.
- **Notes:** Combine with parcel data and building permits for a full
  development picture. Cities (Daytona Beach, DeLand, etc.) have their
  own zoning — get city zoning from city GIS/open data if needed.

### City-level zoning / land use (Daytona Beach, DeLand, New Smyrna
Beach, Ormond Beach, Port Orange, Deltona, etc.)
- **Publisher:** Individual city governments
- **What it provides:** City zoning maps, land use, comprehensive plans,
  city permit data (where applicable).
- **Volusia coverage:** City-specific. Each incorporated city has its own
  zoning. Some cities may have open data portals; others may require
  interaction.
- **Access method:** City websites, GIS/open data (some cities use ArcGIS
  Online or similar), public records. Varies by city.
- **Friction:** MEDIUM — varies; some cities have good GIS data, others
  less so. Public records requests may be needed for some data.
- **Priority:** MEDIUM (incremental to county data; important for city-
  level analysis)
- **Why:** A lot of development happens within city limits; city zoning
  and permits matter. For a full land use picture, need both county and
  city.
- **Notes:** Daytona Beach, DeLand, New Smyrna Beach, Ormond Beach, Port
  Orange, Deltona are the largest. Check each for open data availability.

### Florida Department of Environmental Protection (DEP) — Land Use /
Environmental / Permits
- **Publisher:** Florida DEP
- **What it provides:** Environmental permits, stormwater, land use
  (Florida uses a coordinated land use system with state involvement),
  environmental resource permits, DEP GIS data.
- **Volusia coverage:** DIRECT — Volusia County environmental permits and
  land use context.
- **Access method:** FL DEP website, data portals, GIS data. Public.
- **Friction:** MEDIUM.
- **Priority:** MEDIUM (overlapping with Domain 5 environment; DEP data
  is partly environmental/man-made land use)
- **Why:** Environmental constraints and permits affect development (wetlands,
  stormwater, environmental resource permits). Useful for land use /
  development analysis and environment maps.
- **Notes:** Overlaps with Domain 5 (environment/climate). DEP data is
  also relevant to land use constraints.

### Other housing data sources (HUD, Freddie Mac, Fannie Mae, etc.)
- **HUD:** HUD publishes Fair Market Rents (FMRs) by county/metro (used
  for Section 8), HUD housing market data, HUD USER data (CPS-H, AHS).
  HUD's American Housing Survey (AHS) has data for some metros (may not
  include Volusia separately — check). HUD data is public. FMRs for the
  Daytona Beach MSA are available. AHS may have Miami or Orlando but not
  Volusia specifically — verify.
- **Freddie Mac / Fannie Mae:** Private; some public data (e.g. housing
  price indexes, multifamily data) but limited county-level free data.
- **Priority:** HUD FMRs are useful (rent benchmarks for the MSA). AHS
  likely not Volusia-specific. Others are supplementary/gated.
- **Notes:** HUD FMRs are a public rent benchmark at MSA level. Useful
  complement to ZORI (which is observed asking rents). HUD also has
  housing finance data (FHA, etc.).

---

2.2 TOP PICKS FOR PROJECT VOLUSIA — REAL ESTATE/HOUSING/PROPERTY

1. Zillow Research (ZHVI, ZORI, market data) — county/city/ZIP home
   values and rents, free no-key CSVs (HIGH — primary housing market
   trends, accessible)
2. Volusia County Property Appraiser — parcel data, assessments, sales,
   tax roll, GIS parcels (HIGH — authoritative parcel-level local data)
3. Census Building Permits Survey — new housing permits by county/ZIP/place
   (HIGH — construction activity, supply)
4. Volusia County Permit Center / Growth & Resource Management — local
   building permits, zoning, land use (HIGH — permitting velocity, local
   detail)
5. Volusia County Open Data portal (ArcGIS Hub) — parcels, zoning, and
   other GIS layers (HIGH — geospatial access to parcels, zoning, etc.)
6. Realtor.com research — market trends (days on market, inventory) at MSA
   level (MEDIUM — triangulation)
7. Florida DOR property tax data — county/jurisdiction tax stats (MEDIUM —
   tax burden context)
8. HUD Fair Market Rents (FMRs) — MSA rent benchmark (MEDIUM — public rent
   benchmark)
9. Census ACS housing tables (B25001-B25077, etc.) — housing unit counts,
   tenure, vacancy, value, rent, year built, at tract/county (MEDIUM-HIGH —
   already covered via ACS in Domain 1/4; ACS housing is fundamental)
10. City zoning/land use (Daytona Beach, DeLand, etc.) — city-level
    regulatory data (MEDIUM — incremental to county)
11. Florida DEP land use / environmental permits — development constraints
    (MEDIUM — development feasibility)
12. ZTRAX / ATTOM / CoreLogic — gated/private; note as unavailable/gated
    (N/A or gated — use public equivalents)

---

2.3 CAVEATS AND FLAGS — REAL ESTATE/HOUSING

- Zillow ZHVI/ZORI are model-based indices, not transaction prices. They
  are useful for trends and relative comparison but are not raw deed data.
  Do not confuse ZHVI with median sale price of closed transactions (Zillow
  publishes median sale price only at metro level). For actual transaction
  prices, use VCPA sales data and public records.
- Zillow data coverage varies by geography — neighborhood level may not
  exist for all Volusia neighborhoods. County and ZIP are solid; city
  likely available; neighborhood spotty.
- Zillow research data is free to use but is not "open data" with a public
  domain dedication. Zillow requests citation. Check current terms at
  zillow.com/research/data. For most analysis use it's effectively open,
  but don't claim it's public domain.
- VCPA data (Access database, parcel GIS) is authoritative and public
  record, but requires processing (Access DB needs conversion; GIS layer
  may need attribute joining). Weekly working roll is the freshest tax
  roll; annual final roll is the official roll. Custom requests cost money
  and time.
- Building permits (Census BPS) are permit counts, not unit addresses or
  completions. Local permit data (Volusia Permit Center) may have address-
  level detail but access is interactive. Census BPS is the easy public
  aggregate.
- ACS housing data is survey-based; at tract level, margins of error are
  large for some variables (e.g. median home value at tract level).
  Combine ACS housing with VCPA/Zillow for triangulation.
- Zoning/land use data: county and cities may not be perfectly synchronized
  in GIS format; verify currentness. Zoning changes via amendments; GIS
  layers may lag.
- Short-term rental data is covered in Domain 3 (tourism). STR regulation
  is a local policy matter (Volusia County and cities regulate STRs) —
  relevant to housing (STRs remove units from long-term rental market) and
  tourism. Note the overlap.
- Property tax: Florida has a "Save Our Homes" cap on homestead assessed
  value growth; assessed value ≠ market value for homesteaded properties.
  VCPA assessed values are for taxation, not pure market value (though
  "Just Values" estimates are market-value-oriented). Understand the
  difference when using assessment data as a market signal.

---

3. DOMAIN 3 — TOURISM, HOSPITALITY, VISITOR ECONOMY, EVENTS, RECREATION

---

3.1 SOURCE LIST

### Volusia County Convention & Visitors Bureau (CVB) — Visit Daytona
Beach Area CVB / Daytona Beach Area Convention & Visitors Bureau
- **Publisher:** Halifax Area Advertising Authority dba Daytona Beach Area
  Convention & Visitors Bureau (daytonabeach.com). Also "Volusia County
  CVB" / Visit Daytona Beach.
- **What it provides:** Tourism market research — visitor tracking studies,
  visitor profiles, economic impact reports (visitor spending, economic
  impact), hotel occupancy and ADR/RevPAR data (may be from STR or own
  research), event impact, tourism industry statistics. Publishes reports
  like "Annual Visitor Tracking and Economic Impact Report," visitor
  profiles, occupancy studies, competitive market analysis. Some reports
  are public PDFs; some data may require partner status or direct request.
- **Volusia coverage:** DIRECT — Volusia County / Daytona Beach area /
  Halifax Taxing District. Covers the greater Daytona Beach area and
  Volusia County tourism.
- **Access method:** CVB website (daytonabeach.com/about/market-research)
  publishes some reports as public PDFs (e.g. "April 2024 through March
  2025 Annual Visitor Tracking and Economic Impact Report" is a public
  PDF). "Past Market and Investor Research" page lists prior reports.
  Some data/rates may require being a tourism partner or direct request
  to research@daytonabeach.com (verify current contact — the CVB site
  mentions partner resources and research). Reports are public; raw data
  may be gated.
- **Update frequency:** Periodic — annual visitor tracking reports, annual
  economic impact reports, periodic occupancy/market studies. Not
  necessarily monthly public data.
- **License/terms:** Public reports (PDF) are free to read/download. Data
  behind them may be more restricted (partner access). CVB is a public-
  purpose tourism organization funded by the tourist development tax.
- **Friction:** MEDIUM. Reports are publicly accessible as PDFs; the
  granular data (e.g. monthly hotel stats, survey microdata) may require
  partner status or request. The CVB is the primary local tourism data
  source — establishing a relationship with them is valuable.
- **Priority:** HIGH
- **Why:** The central local source for Volusia tourism intelligence —
  visitor numbers, origin, spending, economic impact, hotel performance,
  event impact. The CVB's economic impact reports and visitor tracking
  studies are gold for the tourist experience report, monthly tourism
  update, and industry mover intelligence. The CVB is funded by the 3%
  Convention Development Tax (bed tax) — public-purpose data.
- **Notes:** Establish contact with the CVB research team early (Q4).
  They may share data or reports beyond what's public, or point to data
  sources. The CVB's market research page (daytonabeach.com/about/
  market-research) and past reports page are the public entry points.
  Note: the CVB covers the Halifax Taxing District (Daytona Beach area)
  and promotes all of Volusia County — clarify geographic scope of each
  report.

### STR (Smith Travel Research) — Hotel Performance Data
- **Publisher:** STR (now part of CoStar Group)
- **What it provides:** Hotel performance benchmarking — occupancy, ADR
  (average daily rate), RevPAR (revenue per available room) by market
  (competitive set, market, metro, state, national). The hospitality
  industry standard. STR reports cover hotel performance by market.
- **Volusia coverage:** STR has a market for the Daytona Beach area / Volusia
  County (the "Daytona Beach" market or similar). STR data is typically
  sold by market. The question is public access.
- **Access method:** STR data is SUBSCRIPTION-based (commercial). Hotels
  subscribe to STR Benchmark/STR Report to get their market data. STR
  publishes some summary data and press releases, but detailed market
  data is gated.
  - Visit Florida provides monthly STR reports to up to 200 partners per
    month — partners can request STR reports via Visit Florida (visitflorida.org/
    resources/research/str-reports). You must be a Visit Florida Marketing
    Partner to access the request form. Contact research@visitflorida.org
    for assistance. So STR market data for Volusia is accessible IF
    Project Volusia becomes a Visit Florida partner (or gets a partner to
    share).
  - STR also publishes some public market summaries / press releases /
    industry data (e.g. national/state occupancy snapshots), but not
    granular local market data publicly.
- **Update frequency:** Monthly (STR reports monthly).
- **License/terms:** STR data is proprietary/commercial. Gated by
  subscription or partner access (Visit Florida partner route).
- **Friction:** HIGH (gated). Public access is limited to aggregate
  summaries. The Visit Florida partner route (200 partners/month get STR
  reports) is the most viable public-access path — Project Volusia should
  evaluate becoming a Visit Florida Marketing Partner or partnering with
  one to get monthly STR reports for the Daytona Beach market.
- **Priority:** HIGH (if accessible) / MEDIUM (if gated). STR is the gold
  standard for hotel performance; access is the challenge. The Visit
  Florida partner route makes it realistically accessible. Without it,
  STR data is gated and you rely on CVB reports (which may include STR
  data) and public summaries.
- **Why:** Hotel occupancy, ADR, RevPAR are THE core tourism/hospitality
  metrics. Essential for the monthly tourism update, tourist experience
  report, and hospitality industry stakeholders. The Visit Florida partner
  route is the way to get them for Volusia.
- **Notes:** The CVB may already have STR data and publish it in their
  reports (many CVBs get STR data and include market-level occupancy/
  ADR/RevPAR in their reports). Check the CVB's published reports first —
  if they include STR market stats, that's public access to STR data via
  the CVB. The Visit Florida partner route is the direct STR access path.
  Also note: CoStar/STR has moved to subscription models; "STR Benchmark"
  is the current product.

### Inside Airbnb — Public Airbnb data
- **Publisher:** Inside Airbnb (insideairbnb.com) — academic/research
  project, data by Murray Cox and community.
- **What it provides:** Publicly available Airbnb listing data — listings
  CSV (listing details, price, room type, location, etc.), calendar CSV
  (availability/booking), reviews CSV (review text, ratings), summary
  metrics. Data collected from public Airbnb pages. Quarterly updates
  (generally). Archived data available for past periods.
- **Volusia coverage:** CHECK — Inside Airbnb coverage for Daytona Beach /
  Volusia County is NOT confirmed in the sources retrieved. Inside Airbnb
  covers many cities globally but coverage is city-specific and not
  guaranteed for every city. Search insideairbnb.com/get-the-data for
  "Daytona Beach" or "Volusia" — if not listed, Volusia may not be
  covered. (The retrieved search results did NOT show a Daytona Beach or
  Volusia County entry on the Inside Airbnb get-the-data page — it showed
  Broward County, FL and other cities, but not Daytona Beach/Volusia
  explicitly.) This is a gap — Inside Airbnb may not cover Volusia.
  Verify directly on insideairbnb.com/get-the-data.
- **Access method:** Free public download (CSV files) from insideairbnb.com/
  get-the-data. No key. Direct downloads.
- **Update frequency:** Quarterly (generally), with archived data for past
  periods.
- **License/terms:** Open/free (creative commons-like, for research/
  analysis). Attribution requested.
- **Friction:** LOW IF covered. If not covered for Volusia, irrelevant.
  Need to verify coverage first.
- **Priority:** HIGH IF COVERED / N/A IF NOT. Inside Airbnb is a great
  public source for STR data (listing-level, calendar, reviews) if it
  covers Volusia. If it doesn't, you need AirDNA/AirROI/Airbtics (gated/
  commercial summaries) or the CVB/airbnb insights from other sources.
- **Why:** STR data at listing level (availability, pricing, occupancy
  inferred, reviews) — excellent for the short-term rental analysis,
  tourist experience report, and tourism analytics. Public and free if
  covered.
- **Notes:** CRITICAL GAP TO VERIFY: does Inside Airbnb cover Daytona Beach
  or Volusia County? The get-the-data page needs to be checked. If not,
  the alternatives are: AirDNA (commercial), AirROI (commercial summaries),
  Airbtics (commercial summaries), the CVB (may have STR-type data), or
  scraping (aggressive; Airbnb terms of service concerns). For a public/
  open charter, Inside Airbnb is the preferred route if available.

### AirDNA / AirROI / Airbtics — Commercial STR market data
- **Publisher:** AirDNA, AirROI, Airbtics (private companies)
- **What they provide:** Short-term rental market analytics — occupancy,
  revenue, ADR, RevPAR, listing counts, seasonality, by market. Summaries
  and market reports (some free summaries, detailed data paid).
- **Volusia coverage:** Direct — Daytona Beach market data (AirROI and
  Airbtics confirmed showing Daytona Beach STR data: occupancy ~32-34%,
  ADR ~$238-242, RevPAR ~$79-85, ~1,500-1,700 active listings, annual
  revenue ~$20-21K per listing, peak in March, etc. from AirROI/Airbtics
  public summaries). AirDNA also has Daytona Beach data (5,557 vacation
  rentals per AirDNA summary). These are PUBLIC SUMMARIES (market overview
  pages) but detailed data is paid.
- **Access method:** Public market overview pages (free to view summary
  stats); detailed data and API are paid subscription.
- **Update frequency:** Monthly/quarterly updates (summaries updated).
- **License/terms:** Commercial. Public summaries are free to view but
  not to redistribute in detail; data behind is paid.
- **Friction:** MEDIUM — public summaries give you a top-line picture
  (occupancy, ADR, RevPAR, listing counts, seasonality) but not the
  granular data or historical time series without paying. Good for a
  top-line snapshot and triangulation, not for building a full STR dataset.
- **Priority:** MEDIUM (public summaries are useful; detailed data is
  gated). Public summaries from AirDNA/AirROI/Airbtics provide an
  accessible snapshot of the Daytona Beach STR market. Use as a cross-
  check and top-line source. For a deeper STR dataset, need Inside Airbnb
  (if covered) or paid data.
- **Why:** STR market overview is useful for the tourist experience report
  and tourism analysis. The public summaries give you occupancy, ADR,
  RevPAR, listing counts, seasonality for Daytona Beach without a paid
  subscription — good enough for top-line reporting and benchmarking.
- **Notes:** AirDNA, AirROI, Airbtics all show similar metrics for Daytona
  Beach with some variation (occupancy 32-58% depending on source/method;
  ADR $177-243; listing counts 1,500-5,500 depending on scope). Different
  methodologies produce different numbers. The public summaries are
  directional; don't over-precision them. The City of Daytona Beach STR
  regulation (4 tourist commercial zones + 13 redevelopment corridors;
  DBPR vacation rental license ~$300/yr; combined lodging tax 12.5%)
  is also relevant — it's public regulatory data from the city.

### Volusia County Tourist Development Tax (Bed Tax) / Convention
Development Tax — receipts
- **Publisher:** Volusia County Tax Collector / Revenue Services (volusia.org/
  services/financial-and-administrative-services/revenue-services/tourist-
  and-convention-development-tax). Also administered by the Halifax Area
  Advertising Authority / CVB for the Halifax Taxing District.
- **What it provides:** Tourist Development Tax (also called Convention
  Development Tax / bed tax / hotel tax) — a 6% tax on short-term
  accommodations in the Halifax Taxing District (Daytona Beach area) and
  other Volusia taxing districts. Tax receipts by month/taxing district
  are a proxy for short-term lodging volume and tourism spending. Some
  districts have 3% (Convention Development Tax) and 6% (Tourist
  Development Tax) components.
- **Volusia coverage:** DIRECT — Volusia County taxing districts. Halifax
  Taxing District (Daytona Beach area) is the main one; other districts
  (e.g. New Smyrna Beach, Ormond Beach, Port Orange, etc.) may have their
  own tourist development taxes.
- **Access method:** Volusia County website (volusia.org) — tourist and
  convention development tax page. Tax receipts may be in monthly/annual
  reports or available via public records. The CVB administers the Halifax
  district tax and may have receipts data. Public record.
- **Update frequency:** Monthly/quarterly/annual receipts.
- **License/terms:** Public record (Florida).
- **Friction:** MEDIUM — receipts data may be in reports or available via
  request; not necessarily a clean downloadable dataset. The CVB may have
  it. The Volusia County tax collector publishes tax data.
- **Priority:** MEDIUM-HIGH
- **Why:** Tourist development tax receipts are a high-frequency, direct
  proxy for short-term lodging activity — a core tourism economy indicator.
  Growing bed tax receipts = growing short-term lodging/ tourism. Useful
  for the monthly tourism update and economic briefing. Combine with CVB
  visitor data and STR data for triangulation.
- **Notes:** Different Volusia districts have different tourist development
  taxes (Halifax District 6%+TTC, etc.), so receipts need to be attributed
  to the right district. The CVB and Tax Collector are the sources. Public
  record but may require pulling from reports/requests.

### Visit Florida — State tourism data / research
- **Publisher:** Visit Florida (state's tourism marketing organization)
- **What it provides:** Florida tourism data — visitor statistics, tourism
  economic impact, market research, STR reports (to partners), state and
  regional tourism data. Visit Florida publishes state tourism data and
  some regional breakdowns. Also the gateway to STR reports via partner
  program.
- **Volusia coverage:** Florida statewide and regional (Volusia is part of
  a Florida tourism region). Visit Florida may have regional 관광 data.
- **Access method:** Visit Florida website (visitflorida.org/resources/
  research), research reports, partner research requests. Public reports;
  STR reports to partners.
- **Update frequency:** Periodic (annual tourism data, economic impact;
  STR reports monthly to partners).
- **License/terms:** Public reports; STR data to partners (see STR entry).
- **Friction:** MEDIUM — some data public, some gated. Visit Florida is
  the entry to STR reports via partner program.
- **Priority:** MEDIUM
- **Why:** State tourism context and the STR partner gateway. Useful for
  comparing Volusia to Florida overall and other destinations.
- **Notes:** Visit Florida's STR report program (200 partners/month) is
  the most accessible route to STR market data for Volusia if Project
  Volusia becomes a partner. Contact research@visitflorida.org.

### National Park Service — Visitor Use Statistics (including Canaveral
National Seashore)
- **Publisher:** National Park Service (NPS), U.S. Department of Interior
- **What it provides:** Monthly and annual recreation visitation for all
  NPS units, including Canaveral National Seashore (which is in Volusia
  County / adjacent to it — Canaveral NS is on the Atlantic coast, near
  Titusville/New Smyrna area, part of Volusia County coastline). Visitation
  numbers, recreation visits, overnight stays, etc. NPS Visitor Use
  Statistics data package (1979-2025) available as CSV on data.gov. IRMA
  portal (irma.nps.gov/Stats) for queries. NPS Visitor Use Statistics
  Dashboard for quick visuals.
- **Volusia coverage:** DIRECT — Canaveral National Seashore is in/volusia
  County area (the seashore spans Volusia and Brevard counties; the
  Volusia portion is relevant). NPS data gives visitor numbers for the
  seashore. Other nearby NPS units (e.g. Gateway National Recreation Area
  is not in FL; nearby is Canaveral NS). Also consider neighboring
  recreation areas.
- **Access method:** 
  - NPS Visitor Use Statistics Data Package (2025) on data.gov: 
    catalog.data.gov/dataset/nps-visitor-use-statistics-data-package-2025
    — CSV downloads (Main_Data.csv 1979-2025, Main_State_Data.csv
    2016-2025, metadata). Public domain (CC0).
  - IRMA portal (irma.nps.gov/Stats) — query by park, get reports.
  - NPS dashboard (nps.gov/subjects/socialscience/visitor-use-statistics-
    dashboard.htm) — quick visuals.
  - Park-specific statistics pages (e.g. nps.gov/cana) may have visitation
    summaries.
- **Update frequency:** Monthly visitation data (with lag); annual
  summaries. Data package updated annually (2025 package March 2026).
- **License/terms:** Public domain (NPS data is public domain; data.gov
  package is CC0).
- **Friction:** LOW. CSV downloads are straightforward. IRMA query tool
  is usable. Good time series (1979+).
- **Priority:** HIGH
- **Why:** Canaveral National Seashore is a major Volusia County natural/
  recreation attraction with significant visitation. NPS visitor data is
  public, high-quality, and long time series — valuable for the tourism/
  recreation analysis, tourist experience report, and nature tourism
  narratives. Also covers other NPS units if relevant (e.g. should check
  if any other NPS units are in or near Volusia — Canaveral NS is the
  main one).
- **Notes:** NPS visitor use statistics have known limitations (estimation
  methods, some parks count differently, rounding, etc.) — see NPS data
  limitations page. Use with awareness. Canaveral NS visitation is a
  strong proxy for nature-based tourism in the county.

### Florida State Parks — Visitor data
- **Publisher:** Florida Department of Environmental Protection / Florida
  State Parks (floridastateparks.org)
- **What it provides:** Florida State Parks visitation data — some parks
  publish visitation numbers. Volusia County has state parks? Check:
  Volusia County has state parks (e.g. Tomoka State Park is in Volusia
  County — actually Tomoka is in Volusia County near Ormond Beach/Edgewater;
  Bulow Creek, etc.). Florida State Parks publishes some visitation stats.
- **Volusia coverage:** DIRECT — Tomoka State Park (Volusia County), other
  FL state parks in/near Volusia.
- **Access method:** Florida State Parks website, some visitation data
  public, FL DEP data portals. Public.
- **Update frequency:** Periodic.
- **License/terms:** Public.
- **Friction:** MEDIUM — visitation data for individual parks may not be
  as easily bulk-accessible as NPS; some is in reports.
- **Priority:** MEDIUM
- **Why:** State parks are recreation/tourism attractions. Tomoka State
  Park is in Volusia County — its visitation is relevant. Good for
  recreation/tourism analysis.
- **Notes:** Verify visitation data availability for individual FL state
  parks. NPS (Canaveral NS) is the stronger public source for park
  visitation in the area. FL State Parks data is supplementary.

### Daytona Beach International Airport (DAB) — passenger traffic
- **Publisher:** Daytona Beach International Airport / Daytona Beach
  Aviation Authority (flydaytonafirst.com). Owned by Volusia County.
- **What it provides:** Passenger traffic statistics (annual and monthly
  passenger counts), aircraft operations. DAB is the primary commercial
  airport serving Volusia County. Historical passenger counts: 2016-2025
  (676K to 772K; 2025 = 772K per Wikipedia/FAA data; 2025 was a record).
  Top routes and carriers. Wikipedia has annual passenger counts 2016-2025
  compiled from FAA/BTS sources.
- **Volusia coverage:** DIRECT — DAB is in Volusia County (Daytona Beach).
  Represents the county's air travel market.
- **Access method:** 
  - Airport website (flydaytonafirst.com/about-dab/traffic-statistics.stml)
    — "The traffic statistics reports are available upon request by
    contacting Joanne Magley at jmagley@flydab.com." So monthly passenger
    data is BY REQUEST, not a public download.
  - FAA data: FAA publishes airport data (airport form 5010, operations,
    based aircraft) — public. FAA DAB page (faa.gov/flight_deck/dab).
  - BTS TranStats / TranStats aviation data: Bureau of Transportation
    Statistics publishes airline traffic data (T-100, enplanements,
    passenger counts by airport) — public, downloadable. TranStats has
    airline data by airport (including DAB). The BTS data is useful for
    passenger traffic at DAB. (Wikipedia's DAB passenger numbers cite
    BTS TranStats as a source — transtats.bts.gov/airports.asp.)
  - Wikipedia DAB page compiles annual passenger counts 2016-2025 from
    FAA/BTS (useful as a quick reference, but go to primary sources for
    analysis).
- **Update frequency:** FAA data annual; BTS data periodic (monthly/
  annual airline traffic). Airport monthly stats by request.
- **License/terms:** FAA/BTS data public domain. Airport stats by request.
- **Friction:** MEDIUM. BTS TranStats requires query/download (can get
  enplanements/passenger data by airport). Airport monthly stats require
  email request to the airport. FAA airport data is public. Wikipedia is
  a summary (not a primary source but points to BTS/FAA).
- **Priority:** MEDIUM-HIGH
- **Why:** Airport passenger traffic is a tourism and economic indicator —
  Volusia County's air access and visitor volume proxy. DAB is the county's
  airport; passenger trends reflect tourism and business travel. Useful
  for the monthly tourism update, economic briefing, and transportation
  analysis. Also relevant for tourism (visitors flying in) and economic
  (business travel).
- **Notes:** BTS TranStats is the public programmatic source for airline
  passenger data by airport — get enplanements/passenger counts for DAB
  from BTS. The airport's own monthly stats require an email request
  (Joanne Magley). FAA data gives operations and based aircraft. Combine
  for a full airport picture. Also consider Orlando International (MCO) as
  the regional air gateway — many Volusia visitors fly into MCO and drive;
  MCO is a better proxy for total regional air access. DAB is more local-
  specific. Both matter.

### Bureau of Transportation Statistics — Air traffic data (T-100,
enplanements)
- **Publisher:** U.S. Bureau of Transportation Statistics (BTS), DOT
- **What it provides:** Airline traffic data — T-100 (airline traffic by
  airport, origin-destination, carrier, passengers, freight), enplanements
  (passengers boarding) by airport, monthly and annual. Public data.
- **Volusia coverage:** DIRECT — DAB airport data (and other Florida
  airports). T-100 has DAB. Can get passenger traffic for DAB from BTS.
- **Access method:** TranStats portal (transtats.bts.gov) — query and
  download aviation data. T-100 data download. Public.
- **Update frequency:** Monthly (T-100 monthly, with lag), annual.
- **License/terms:** Public domain (U.S. government).
- **Friction:** LOW-MEDIUM. TranStats query interface; some data requires
  selection and download. Good data, but interface may require some
  navigation. T-100 is detailed.
- **Priority:** MEDIUM-HIGH
- **Why:** Public airline passenger data for DAB — useful for tourism and
  transportation analysis. The public programmatic source for airport
  passenger traffic (complement to the airport's own stats).
- **Notes:** BTS TranStats is the source to use for a reproducible airport
  passenger time series for DAB. Combine with FAA data and airport-request
  stats. Also use for other Florida airports if relevant.

### Cruise port / marine tourism (Port Canaveral, etc.)
- **Publisher:** Port Canaveral (Port Authority), Florida Seaports, etc.
- **What it provides:** Port Canaveral is the cruise port for the region
  (cruise passengers, ships). Port Canaveral is near Volusia County (in
  Brevard County, but serves the region including Volusia). Cruise traffic
  is a tourism indicator for the region.
- **Volusia coverage:** REGIONAL — Port Canaveral is in Brevard County but
  serves Volusia visitors/cruisers. Not in Volusia County but relevant to
  regional tourism.
- **Access method:** Port Canaveral website, press releases, some public
  data. Florida Seaports. Public.
- **Priority:** LOW-MEDIUM (regional tourism context, not Volusia-specific)
- **Notes:** Port Canaveral cruise data is regional tourism context. If
  Project Volusia cares about broader regional tourism, include. But it's
  Brevard County, not Volusia.

### Events data — Daytona 500, Bike Week, Spring Break, etc.
- **Publisher:** Various — Daytona International Speedway ( NASCAR /
  International Speedway Corporation / Daytona Motorsports), event
  promoters, CVB event calendars, local news.
- **What it provides:** Major events in Volusia County — Daytona 500 (and
  Speedweeks), Bike Week (February), Spring Break, black bike week, concerts
  at the Speedway/bandshell, festivals (e.g. New Smyrna Beach events, DeLand
  events), etc. Event attendance, dates, economic impact (some events have
  published economic impact estimates).
- **Volusia coverage:** DIRECT — Volusia County major events.
- **Access method:** Event organizers' websites, CVB event calendars, local
  news, some published economic impact studies. Public.
- **Update frequency:** Event-specific; annual recurring events. Economic
  impact studies may be periodic.
- **License/terms:** Public (event info).
- **Friction:** MEDIUM — event attendance numbers and economic impact may
  be in press releases, news, or studies, not a clean dataset. Some events
  publish attendance (e.g. Daytona 500 attendance is widely reported).
- **Priority:** MEDIUM
- **Why:** Major events (Daytona 500, Bike Week, Spring Break) are huge
  tourism drivers for Volusia County — they bring large visitor volumes
  and economic impact. Event calendars and attendance are important for
  the tourist experience report, monthly tourism update, and tourism
  analysis. Events are a distinctive Volusia tourism feature.
- **Notes:** Hard data (attendance, economic impact) may be in press
  releases, CVB reports, or event organizer publications. Daytona 500
  attendance is widely reported (but verify sources). Bike Week attendance
  is also reported. The CVB may have event impact data. Build an events
  calendar/ dataset from public sources. For economic impact, look for
  published studies (some may use IMPLAN — see Domain 1 caveats).

### Hotel tax / lodging tax data (see also Domain 6)
- **Publisher:** Volusia County and cities (see Domain 6 and the bed tax
  entry above)
- **Notes:** Covered in Domain 6 (government finance) and partially above
  (Tourist Development Tax). Lodging taxes are both a tourism indicator and
  a government revenue line.

### Review/sentiment data (TripAdvisor, Google, Yelp)
- **Publisher:** TripAdvisor, Google, Yelp (private platforms)
- **What it provides:** Tourist/business reviews, ratings, review volume,
  sentiment. Publicly viewable (you can read reviews on the platforms).
  Bulk review data is NOT public (platforms don't offer bulk review export
  without API/commercial access). Google Places API, Yelp Fusion API,
  TripAdvisor (no public API — scraping restricted) offer some access but
  with rate limits and terms.
- **Volusia coverage:** DIRECT — Volusia County businesses and attractions
  have reviews on these platforms.
- **Access method:** Manual viewing (free), platform APIs (Google Places
  API, Yelp Fusion API — rate-limited, may require API key, some cost),
  scraping (restricted by ToS — caution). TripAdvisor has no official
  public API; scraping is against ToS.
- **Update frequency:** Real-time (reviews posted continuously).
- **License/terms:** Platform terms govern. Google/Yelp APIs have terms
  and rate limits. TripAdvisor scraping is ToS-restricted. Public review
  viewing is free; bulk extraction is gated/restricted.
- **Friction:** HIGH for bulk analysis. Manual review reading is feasible
  for small samples. APIs exist but with limits. TripAdvisor scraping is
  problematic. For the tourist experience report and sentiment analysis,
  use sample-based review reading or API access where available, not bulk
  scraping.
- **Priority:** MEDIUM (sample-based review analysis) / LOW for bulk
  (not publicly accessible at scale)
- **Why:** Tourist reviews and sentiment are part of the tourist experience
  — relevant for the tourist experience report (review sentiment analysis)
  and tourist-facing reputation monitoring. But bulk review data is not
  publicly accessible; use sampling or API-limited access.
- **Notes:** The methodology doc (METHODOLOGY.md) section 4.3 mentions
  review sentiment analysis (TripAdvisor, Google, Yelp) as part of the
  tourist experience report. Do this via sample-based analysis (read a
  sample of reviews) or API access (Google Places/Yelp) within terms.
  Don't scrape TripAdvisor in bulk (ToS). Note the limitation in the
  methodology.

### Tourism economic impact studies (published)
- **Publisher:** CVB, Visit Florida, consultants, universities, chambers
- **What it provides:** Published tourism economic impact studies for
  Volusia County / Daytona Beach area — visitor spending, economic impact
  (output, income, jobs), tax impact. The CVB publishes annual visitor
  tracking and economic impact reports (e.g. "Annual Visitor Tracking and
  Economic Impact Report" — public PDF). These studies may use IMPLAN or
  similar models but the published report is public.
- **Volusia coverage:** DIRECT.
- **Access method:** CVB website (public PDFs), Visit Florida, chamber
  reports, university studies. Public.
- **Update frequency:** Periodic (annual CVB economic impact report).
- **License/terms:** Public (published reports).
- **Friction:** LOW-MEDIUM (reports are public PDFs; underlying model is
  not public but the outputs are).
- **Priority:** HIGH
- **Why:** Tourism economic impact (visitor spending, jobs, tax revenue)
  is a headline tourism metric. The CVB's annual economic impact report is
  the primary local source. Essential for the annual state of the county,
  tourist experience report, and industry mover intelligence.
- **Notes:** These studies often use economic multipliers (IMPLAN or similar)
  — see Domain 1 caveats. Use the published numbers but note the method.
  The CVB report is the go-to local source; establish access early.

### Attractions / recreation data (museums, theaters, amusement, etc.)
- **Publisher:** Individual attractions, CVB, OpenStreetMap, local tourism
  directories.
- **What it provides:** Listings and some attendance/operations data for
  Volusia attractions — museums (e.g. Daytona Beach Museum?), theaters,
  amusement/ attractions (e.g. Daytona International Speedway, educational
  attractions, nature attractions, etc.). Most attraction attendance is
  NOT publicly reported (unlike theme parks which publish attendance — but
  Volusia doesn't have major theme parks; Disney is in Orange County).
- **Volusia coverage:** DIRECT (listed attractions) but attendance data
  limited.
- **Access method:** Attraction websites, CVB, OSM, tourism directories.
  Public.
- **Friction:** HIGH for attendance data (mostly not public). Listings are
  easy (OSM, CVB).
- **Priority:** MEDIUM (listings) / LOW (attendance)
- **Why:** Attractions are part of the tourism offering. Listings and
  locations are useful (maps, tourist info). Attendance data is sparse.
- **Notes:** Unlike Orlando, Volusia doesn't have big theme park attendance
  numbers publicly available. Focus on listing/location data and the
  events/ recreation data that IS available (NPS, state parks, events).

---

3.2 TOP PICKS FOR PROJECT VOLUSIA — TOURISM/HOSPITALITY

1. Volusia County CVB (Daytona Beach Area CVB) — visitor tracking,
   economic impact reports, market research (HIGH — primary local tourism
   source, public reports)
2. STR / CoStar hotel data via Visit Florida partner route — monthly hotel
   occupancy/ADR/RevPAR for Daytona Beach market (HIGH — gold standard,
   accessible via partner program)
3. NPS Visitor Use Statistics (Canaveral National Seashore) — public,
   long time series park visitation (HIGH — public, high quality, nature
   tourism)
4. Zillow/AirDNA/AirROI/Airbtics public STR summaries — top-line STR
   market data for Daytona Beach (MEDIUM-HIGH — accessible public summaries
   for occupancy/ADR/RevPAR/listing counts)
5. Volusia County Tourist Development Tax (bed tax) receipts — short-term
   lodging proxy (MEDIUM-HIGH — public record, high-frequency proxy)
6. Inside Airbnb (IF coverage confirmed for Volusia) — free public listing-
   level STR data (HIGH IF COVERED — excellent public STR data; VERIFY FIRST)
7. BTS TranStats / FAA airport passenger data (DAB) — public airline
   passenger traffic (MEDIUM-HIGH — public airport data)
8. Visit Florida — state tourism data and STR partner gateway (MEDIUM —
   state context, STR access path)
9. CVB economic impact studies / published event impact (MEDIUM-HIGH —
   visitor spending impact)
10. Florida State Parks visitation (Tomoka State Park, etc.) (MEDIUM —
    recreation visitation)
11. Major events (Daytona 500, Bike Week, etc.) — attendance, calendars
    (MEDIUM — event tourism)
12. Review/sentiment (TripAdvisor, Google, Yelp) — sample-based analysis
    (MEDIUM — sample only, bulk gated)

---

3.3 CAVEATS AND FLAGS — TOURISM/HOSPITALITY

- STR data is gated by default. The Visit Florida partner route (200
  partners/month get STR reports) is the realistic public-access path.
  Project Volusia should evaluate becoming a Visit Florida Marketing Partner
  or partnering with one to get monthly STR reports for the Daytona Beach
  market. Alternatively, rely on CVB reports if they include STR market
  data.
- Inside Airbnb coverage for Volusia County / Daytona Beach is UNCONFIRMED
  — must verify on insideairbnb.com/get-the-data before relying on it. If
  not covered, then STR data options are: CVB reports, Visit Florida STR
  partner reports, commercial summaries (AirDNA/AirROI/Airbtics public
  summaries), or paid data. This is a key gap.
- Commercial STR summaries (AirDNA, AirROI, Airbtics) give public top-line
  numbers for Daytona Beach STR market, but different sources report
  different numbers (occupancy 32-58%, ADR $177-243, listing counts
  1,500-5,500) due to methodology differences. Treat as directional.
- STR regulation in Volusia County / Daytona Beach is relevant — Daytona
  Beach permits STRs in 4 tourist commercial zones + 13 redevelopment
  corridors; requires DBPR vacation rental license (~$300/yr); combined
  lodging tax 12.5% (6% FL sales tax + 0.5% Volusia discretionary surtax +
  6% Volusia Tourist Development Tax). Airbnb/Vrbo collect and remit state/
  county taxes on platform bookings. This is public regulatory data — note
  for STR analysis.
- CVB reports are the primary local source; establish contact early. The
  CVB may share data or point to sources beyond public PDFs.
- NPS visitor data has estimation limitations; use with awareness.
- Airport passenger data: BTS TranStats is the public programmatic source;
  the airport's own monthly stats require a request (Joanne Magley at
  flydab.com). FAA data gives operations/based aircraft. DAB passenger
  counts 2016-2025: 676K, 684K, 726K, 670K, 320K (2020 COVID), 543K,
  554K, 687K, 665K, 772K (2025 record) — from Wikipedia/BTS/FAA. 2025
  was a record year per the airport.
- Tourism economic impact studies often use private I-O models (IMPLAN);
  the published report is public but the model is not. Use outputs with
  noted caveats.
- Review sentiment: bulk review data is not publicly accessible; use
  sample-based analysis or API-limited access (Google Places, Yelp) within
  platform terms. TripAdvisor scraping is ToS-restricted.
- Regional tourism context: Port Canaveral (cruises) is in Brevard but
  serves the region; Orlando (MCO) is the regional air gateway many
  visitors use. Both are relevant context but not Volusia-specific.

---

4. DOMAIN 4 — DEMOGRAPHICS, POPULATION, EDUCATION, HEALTH, PUBLIC SAFETY

---

4.1 SOURCE LIST

### U.S. Census Bureau — Decennial Census 2020
- **Publisher:** U.S. Census Bureau
- **What it provides:** Full population count and basic demographics (age,
  sex, race, Hispanic origin, household composition, housing occupancy,
  etc.) at census block, tract, county, state, and national levels — the
  official population count.
- **Volusia coverage:** DIRECT — Volusia County, tracts, blocks. 2020
  Census population for Volusia County was ~517,000 (official 2020 count).
  (2020 Census: Volusia County population 517,026 per Census.)
- **Access method:** Census Bureau API, data.census.gov, Census FTP,
  Decennial Census data products (P.L. 94-171 re-districting data, Summary
  File 1, etc.). Public.
- **Update frequency:** Decennial (2020 is the most recent; 2030 next).
  Supplemental surveys (ACS, PEP) fill the intercensal years.
- **License/terms:** Public domain.
- **Friction:** LOW. Census data is the foundation. API and web UI.
- **Priority:** HIGH
- **Why:** The official population count and baseline demographics. The
  anchor for all demographic analysis. 2020 Census is the most recent
  full count. Essential for the annual state of the county, demographic
  profile, and maps.
- **Notes:** 2020 Census has the official count and basic demographics.
  For detailed characteristics and intercensal updates, use ACS and PEP
  (below). Redistricting data (P.L. 94-171) has basic demographic detail
  at low geography. Summary File 1 has full detail.

### U.S. Census Bureau — Population Estimates Program (PEP)
- **Publisher:** U.S. Census Bureau
- **What it provides:** Annual population estimates for counties, states,
  MSAs, cities, etc. — total population, by age, sex, race, Hispanic
  origin, housing units, etc. Updated annually (vintage each year).
  Between-decade official population estimates.
- **Volusia coverage:** DIRECT — Volusia County, cities (Daytona Beach,
  DeLand, etc.), MSA. Annual estimates.
- **Access method:** Census Bureau API, data.census.gov, Census FTP,
  PEP web tools. Public.
- **Update frequency:** Annual (new vintage each year, typically December/
  following year; e.g. July 1, 2024 estimates released 2025).
- **License/terms:** Public domain.
- **Friction:** LOW. API and web UI.
- **Priority:** HIGH
- **Why:** Annual official population estimates — the current population
  number (most recent is ~590K for Volusia County per PEP). The standard
  "current population" source between censuses. Essential for all reports
  and the baseline.
- **Notes:** PEP estimates have methodology (components of change: births,
  deaths, migration). Compare with ACS and Florida EDR projections.
  PEP is the Census Bureau's official estimate; Florida EDR projections
  are a different (forecasting) product.

### U.S. Census Bureau — American Community Survey (ACS)
- **Publisher:** Census Bureau
- **What it provides:** (Covered in Domain 1 for economic tables, but ACS
  is also the primary source for demographic detail — age distribution,
  race/ethnicity, household composition, educational attainment, language,
  disability, vehicle access, marital status, fertility, veterans, etc. at
  tract, ZIP, county, state, national. Demographic tables: DP05 (demographic
  and housing estimates), S1501 (educational attainment), S1601 (language),
  S1810 (disability), S0802 (vehicle access), S1101 (households), etc.)
- **Volusia coverage:** DIRECT — Volusia County, tracts, ZCTAs.
- **Access method:** Census API, data.census.gov, FTP. Public.
- **Update frequency:** 5-year estimates annual (December release);
  1-year estimates annual.
- **License/terms:** Public domain.
- **Friction:** LOW-MEDIUM. API is good; tract-level MOEs matter.
- **Priority:** HIGH
- **Why:** The primary source for tract-level demographic detail — age,
  race/ethnicity, education, language, disability, vehicle access, etc.
  Essential for demographic maps, resident analysis, equity analysis, and
  the demographic profile in reports.
- **Notes:** ACS is a survey; margins of error apply. At tract level, some
  estimates are unreliable (large MOE relative to estimate). Use 5-year
  for tracts; 1-year for county. ACS doesn't cover everything (e.g. no
  health outcomes, no crime). For health and safety, see below.

### Florida Office of Economic and Demographic Research (EDR) —
Population Projections
- **Publisher:** Florida Legislature / EDR (edr.state.fl.us)
- **What it provides:** Florida county-level population projections
  (future population by county, age, etc.) and demographic estimates.
  Florida's official population projections used for planning and
  budgeting.
- **Volusia coverage:** DIRECT — Volusia County projections.
- **Access method:** EDR website, reports, data tables. Public.
- **Update frequency:** Periodic (projections updated; annual/biennial).
- **License/terms:** Public (Florida state government).
- **Friction:** LOW-MEDIUM. Reports/tables downloadable.
- **Priority:** HIGH
- **Why:** Forward-looking population projections for Volusia County —
  planning, demand forecasting, demographic outlook. Florida EDR
  projections are widely used in Florida and are more Florida-specific
  than Census projections. Essential for the forward-looking analysis in
  the annual state of the county and strategic planning.
- **Notes:** EDR projections are Florida's official projections; compare
  with Census PEP for current estimates and with ACS for characteristics.
  EDR projections often break down by age cohort — useful for aging
  analysis (Volusia has a significant retiree population).

### CDC PLACES — Local Data for Better Health
- **Publisher:** CDC (Centers for Disease Control and Prevention)
- **What it provides:** Model-based population-level health data for
  chronic disease, health outcomes, health behaviors, and health risk
  factors at county, place (city), census tract, and ZCTA levels. A large
  set of health indicators (e.g. diabetes, obesity, smoking, physical
  inactivity, coronary heart disease, asthma, cancer, mental health, etc.)
  modeled from BRFSS and other data.
- **Volusia coverage:** DIRECT — Volusia County, census tracts, ZCTAs,
  cities (places). CDC PLACES provides tract-level health estimates.
- **Access method:** CDC PLACES data portal (places.cdc.gov), API, data
  downloads (CSV/GeoJSON). Public. CDC PLACES API available.
- **Update frequency:** Periodic (new releases; e.g. 2024 release covers
  data through prior years). Updated as new BRFSS data available.
- **License/terms:** Public domain (U.S. government).
- **Friction:** LOW-MEDIUM. API and data portal. Tract-level model-based
  estimates (not direct measurement — modeled from BRFSS). Good geography
  coverage.
- **Priority:** HIGH
- **Why:** The best public source for tract-level health data — health
  outcomes, behaviors, and risk factors by geography. Essential for the
  resident well-being report, health maps, and equity analysis. Fill a
  major gap (health data is otherwise sparse at tract level publicly).
- **Notes:** CDC PLACES estimates are MODEL-BASED (small area estimation
  from BRFSS + Census). They are estimates with uncertainty, not direct
  measurements. Use with that understanding. PLACES is an excellent public
  source but is modeled — don't treat as ground truth. For Florida-
  specific health data, see FL DOH CHARTS.

### Florida Department of Health — CHARTS (Community Health Status)
- **Publisher:** Florida Department of Health (FL DOH), flhealthcharts.gov
- **What it provides:** Florida county and community health data — vital
  statistics (births, deaths, infant mortality), disease incidence (e.g.
  HIV, STD, tuberculosis, reportable diseases), behavioral risk factor
  data, county health profiles, health indicators by county. Florida-
  specific health data not available at the national level.
- **Volusia coverage:** DIRECT — Volusia County health data.
- **Access method:** FLHealthCHARTS.gov web portal (interactive queries,
  data downloads), FL DOH website. Public (may require creating a CHARTS
  account for some data — "Create your CHARTS account to instantly view
  your county's data").
- **Update frequency:** Varies by indicator (vital statistics annual,
  disease surveillance periodic, BRFSS biennial).
- **License/terms:** Public (Florida state government). Some data may
  require account.
- **Friction:** MEDIUM. Interactive portal; some data behind account.
  Florida-specific health data not available elsewhere.
- **Priority:** HIGH
- **Why:** Florida-specific health data — vital statistics, disease
  surveillance, county health profiles — that complements CDC PLACES.
  Volusia County-specific health data. Useful for the resident well-being
  report, health analysis, and maps.
- **Notes:** CHARTS account may be needed for some data. FL DOH also
  publishes community health needs assessments (CHNAs) for hospitals —
  those may have Volusia County health data (hospital CHNAs). CDC PLACES
  + FL DOH CHARTS + hospital CHNAs + County Health Rankings = good health
  data coverage.

### County Health Rankings & Roadmaps (Robert Wood Johnson Foundation)
- **Publisher:** Robert Wood Johnson Foundation / County Health Rankings
  (countyhealthrankings.org)
- **What it provides:** Annual county health rankings — health outcomes
  (mortality, morbidity), health factors (health behaviors, clinical care,
  social and economic factors, physical environment) for nearly all U.S.
  counties. A composite and component rankings with data sources cited.
- **Volusia coverage:** DIRECT — Volusia County ranking and component data.
- **Access method:** County Health Rankings website (download data, reports).
  Public.
- **Update frequency:** Annual.
- **License/terms:** Public (RWJF; data sources cited within are public).
- **Friction:** LOW. Website and downloadable data.
- **Priority:** MEDIUM-HIGH
- **Why:** A convenient composite county health score with components —
  useful for benchmarking Volusia against peer counties and tracking over
  time. Good for the resident well-being report and health overview. Not
  tract-level (county-level), but the components cite underlying data
  sources.
- **Notes:** County Health Rankings is a composite — the underlying data
  comes from public sources (CDC, Census, etc.). Use it for a summary view
  and to identify component areas. It's county-level only (not tract). For
  tract health data, use CDC PLACES.

### Florida Agency for Health Care Administration (AHCA) — Hospital/
Healthcare data
- **Publisher:** Florida AHCA
- **What it provides:** Florida healthcare facility data, hospital data,
  healthcare workforce, some utilization data. Florida-specific.
- **Volusia coverage:** DIRECT — Volusia County healthcare facilities
  (Halifax Health, Florida Hospital DeLand, etc.).
- **Access method:** FL AHCA website, data portals, reports. Public (some
  data may be restricted).
- **Update frequency:** Varies.
- **License/terms:** Public (Florida state government).
- **Friction:** MEDIUM.
- **Priority:** MEDIUM
- **Why:** Healthcare access and facility data for Volusia County — hospital
  locations, capacity, healthcare workforce. Useful for healthcare access
  analysis (resident well-being report) and maps.
- **Notes:** Healthcare utilization data (e.g. hospital discharges) may be
  available via AHCA or AHRQ/HCUP (see below). For healthcare access maps,
  combine AHCA facility data with NCES/OSM data.

### AHRQ / HCUP (Healthcare Cost and Utilization Project) — Hospital
discharges
- **Publisher:** AHRQ (Agency for Healthcare Research and Quality)
- **What it provides:** Hospital inpatient discharge data (SID — State
  Inpatient Databases) — some states participate and publish. Florida may
  participate in HCUP. Hospital discharge data by diagnosis, procedure,
  etc. (state-level; some county detail may be available but often
  suppressed for small areas).
- **Volusia coverage:** MAYBE — if Florida participates and provides county-
  level data. Often HCUP data is state-level; county detail limited.
- **Access method:** AHRQ HCUPnet (online tool), AHRQ data requests,
  some data public. Access may require agreement.
- **Priority:** LOW-MEDIUM (Florida HCUP participation uncertain; county
  detail limited)
- **Notes:** Check if Florida HCUP data has Volusia County detail. If yes,
  useful for healthcare utilization; if no, supplementary. HCUP data use
  agreements may apply.

### U.S. Census Bureau — Educational Attainment (ACS S1501) and NCES
— School District / School data
- **Publisher:** Census Bureau (ACS) and National Center for Education
  Statistics (NCES), U.S. Department of Education
- **What it provides:** 
  - ACS: educational attainment (high school, bachelor's, etc.) by
    geography (tract, county, etc.) — S1501, DP02, etc.
  - NCES: school district demographics, school characteristics (public
    and private), enrollment, staff, finance (National Public Education
    Financial Survey), CCD (Common Core of Data) for public schools,
    Private School Universe Survey (PSS). School district demographics
    (SDM) project.
- **Volusia coverage:** DIRECT — Volusia County (ACS educational attainment),
  Volusia County School District (NCES CCD, SDM). NCES has data for
  Volusia County Schools (the school district).
- **Access method:** Census API/data.census.gov (ACS), NCES website/
  data tools (CCD, PSS, SDM, finance surveys). Public.
- **Update frequency:** ACS annual; NCES CCD annual (with lag), finance
  surveys biennial/annual, PSS periodic.
- **License/terms:** Public domain (U.S. government).
- **Friction:** LOW for ACS; LOW-MEDIUM for NCES (web tools, some data
  downloads).
- **Priority:** HIGH
- **Why:** Education data — educational attainment (ACS) is a core
  demographic/economic indicator. School district data (NCES) provides
  enrollment, staffing, finance for Volusia County Schools. Useful for
  the education section of reports, workforce analysis, and equity.
- **Notes:** ACS educational attainment is tract-level available —
  important for education equity maps. NCES CCD has school-level public
  school data (enrollment, demographics, teachers, finances). Volusia
  County Schools is the district. For school performance (report cards),
  see FL DOE (below).

### Florida Department of Education — School Report Cards / PK-12
data
- **Publisher:** Florida DOE (fldoe.org)
- **What it provides:** Florida school and district report cards (accountability
  data — grades, proficiency, graduation rates, attendance, etc.), school
 -level data, district data. Florida's school accountability data. Volusia
  County Schools report card and data.
- **Volusia coverage:** DIRECT — Volusia County Schools (district report
  card, school-level data).
- **Access method:** FL DOE website (fldoe.org/accountability), school
  report cards (edudata.fldoe.org/ReportCards), data downloads. Public.
- **Update frequency:** Annual (report cards annual, some data annual).
- **License/terms:** Public (Florida state government).
- **Friction:** LOW-MEDIUM. Web portal and data downloads.
- **Priority:** HIGH
- **Why:** School performance data for Volusia County Schools — accountability
  grades, graduation rates, proficiency, etc. Essential for the education
  analysis, resident well-being report, and education maps. School-level
  data enables school-level maps.
- **Notes:** Florida school report cards are public and detailed. The FL DOE
  accountability data is a good source. Combine with NCES for federal
  context and ACS for educational attainment. Note: school report card
  grades are a Florida-specific accountability system.

### Volusia County Schools — local data / district reports
- **Publisher:** Volusia County Schools (vcsedu.org)
- **What it provides:** District-level data, school performance, district
  reports, possibly open data. Volusia County Schools is the 4th largest
  district in Florida.
- **Volusia coverage:** DIRECT.
- **Access method:** VCSEDU.org website, district reports, some data
  portals. Public.
- **Friction:** MEDIUM (varies — some data public, some may require request).
- **Priority:** MEDIUM
- **Why:** Local district data and context. The school district is a major
  Volusia institution. Useful for education analysis and stakeholder input.
- **Notes:** Volusia County Schools may have additional data beyond FL DOE
  report cards (e.g. district-specific reports, student demographics).
  Check vcsedu.org for open data or reports.

### Higher education — Embry-Riddle Aeronautical University, Bethune-
Cookman University, Daytona State College, Stetson University (DeLand)
- **Publisher:** Individual institutions (and NCES/IPEDS for federal data)
- **What it provides:** Enrollment, graduation, demographics, financials,
  program data for the higher ed institutions in Volusia County / the region.
  Embry-Riddle (Daytona Beach — aviation/aerospace), Bethune-Cookman
  (DeLand — HBCU), Daytona State College (Daytona Beach — community
  college), Stetson University (DeLand — private). IPEDS (NCES) has
  institutional data for all of these.
- **Volusia coverage:** DIRECT — Volusia County institutions.
- **Access method:** IPEDS (NCES) — public data tools and downloads for
  all institutions (enrollment, finance, graduation, etc.). Institution
  websites may have additional data. Public.
- **Update frequency:** IPEDS annual (with lag). Institutional publications
  vary.
- **License/terms:** Public (IPEDS/NCES).
- **Friction:** LOW for IPEDS (public data tools). Individual institutional
  data varies.
- **Priority:** HIGH
- **Why:** Higher education institutions are major Volusia employers,
  educational anchors, and workforce pipelines. Embry-Riddle (aviation/
  aerospace workforce), Bethune-Cookman (HBCU, historical significance),
  Daytona State College (workforce/community college), Stetson (private
  university). Their enrollment, programs, and outcomes matter for the
  education analysis, workforce development, and economic development
  (aerospace workforce pipeline). IPEDS gives public institutional data.
- **Notes:** IPEDS is the comprehensive federal source for institutional
  data (enrollment by demographics, graduation rates, finance, programs,
  etc.). Use IPEDS for cross-institution comparison. The institutions may
  publish additional local data. Daytona State College is key for workforce
  development / community college pipeline. Embry-Riddle is key for
  aerospace/aviation workforce. These are Project Volusia stakeholder
  interests (educators bridging to employment).

### Florida Department of Law Enforcement (FDLE) — Uniform Crime Reports
- **Publisher:** Florida Department of Law Enforcement (FDLE)
- **What it provides:** Florida crime data — uniform crime reporting (UCR),
  crime statistics by county and agency, crime rates, clearance rates.
  FDLE publishes Florida crime reports and an online crime data tool
  (Florida Crime Data / FDLE Crime Reports). Some interactive crime data
  tools.
- **Volusia coverage:** DIRECT — Volusia County crime data, Volusia County
  Sheriff's Office data, individual agency data (Daytona Beach PD, etc.).
- **Access method:** FDLE website (fdle.state.fl.us/CR), FDLE crime reports,
  data tools (some interactive). Public. Also some third-party dashboards
  (e.g. data.pnj.com FDLE crime report — Pensacola News Journal has a
  crime dashboard using FDLE data; usable for Florida crime data).
- **Update frequency:** Annual (UCR annual data), with some more frequent
  updates.
- **License/terms:** Public (Florida state government).
- **Friction:** LOW-MEDIUM. Reports and data tools. FDLE's crime data
  tools may have some interactivity; bulk data may be available.
- **Priority:** MEDIUM-HIGH
- **Why:** Crime statistics for Volusia County — violent crime, property
  crime, trends, clearance. Public safety is a resident concern and a
  stakeholder interest. Useful for the resident well-being report, public
  safety analysis, and maps. FDLE is the Florida source; FBI UCR is the
  national source.
- **Notes:** FDLE crime data is Florida's UCR submission. Compare with FBI
  UCR/NIBRS (below). Crime data has limitations (reporting practices,
  classification differences, underreporting). Use carefully. FDLE may
  have more Florida-specific detail than FBI UCR.

### FBI — Uniform Crime Reporting (UCR) / NIBRS
- **Publisher:** FBI
- **What it provides:** National crime statistics — UCR (Summary Reporting
  System, transitioning to NIBRS — National Incident-Based Reporting
  System). Crime data by state, agency, county (aggregate). FBI UCR
  publications, Crime Data Explorer (CDE).
- **Volusia coverage:** VIA AGENCY — Volusia County agencies report to FBI
  UCR/NIBRS; data is available at agency level (Volusia County SO, Daytona
  Beach PD, etc.) and county aggregate through FBI CDE.
- **Access method:** FBI Crime Data Explorer (cde.ucr.fbi.gov) — public,
  API, downloads. FBI UCR data. Public.
- **Update frequency:** Annual (with lag).
- **License/terms:** Public domain (U.S. government).
- **Friction:** LOW-MEDIUM. FBI CDE is usable; NIBRS transition may affect
  data availability/comparability (NIBRS is more detailed; some agencies
  transitioned; data comparability across years may be affected during
  transition).
- **Priority:** MEDIUM
- **Why:** National context and agency-level crime data. Useful as a
  complement to FDLE. FBI CDE provides standardized crime data. Not the
  primary Florida source (FDLE is more Florida-specific) but good for
  national comparison and standardized data.
- **Notes:** NIBRS transition: FBI transitioned from SRS to NIBRS; data
  comparability may be affected. Check current FBI CDE data status for
  Volusia agencies. FDLE may have more timely/detailed Florida crime data.

### Volusia County Sheriff's Office — local crime data / public records
- **Publisher:** Volusia County Sheriff's Office (volusiasheriff.gov)
- **What it provides:** Local crime data, arrest logs, calls for service,
  incident reports, crime mapping (some agencies have public crime maps/
  open data crime feeds). Volusia County SO may have public crime data or
  public records.
- **Volusia coverage:** DIRECT — Volusia County (sheriff's jurisdiction —
  unincorporated areas and some contracted cities).
- **Access method:** Volusia County SO website (public records search, arrest
  logs, etc.), public records requests, possibly open data crime feed (check
  if Volusia County has an open data crime dataset on the Open Data portal).
  Public records.
- **Update frequency:** Real-time/instant for some (arrest logs, calls for
  service); aggregate crime stats periodic.
- **License/terms:** Public record (Florida). Some data may be in public
  records systems.
- **Friction:** MEDIUM. Arrest logs/calls for service may be searchable;
  bulk crime data may require public records request or open data portal.
  Check if Volusia County Open Data portal has crime datasets.
- **Priority:** MEDIUM
- **Why:** Local crime data and public safety context. Useful for public
  safety analysis and maps. More granular than FDLE/FBI (local detail).
- **Notes:** Volusia County SO public records search is available (volusiasheriff.gov/
  resources/public-records-search.stml). Check the Volusia County Open Data
  portal (ArcGIS Hub) for any crime/open data crime feed. If available,
  that's the best programmatic access. Otherwise, public records requests.

### Other public safety data (fire, EMS, emergency management)
- **Publisher:** Volusia County Emergency Management, fire departments,
  Florida DOH (emergency medical services data?), NFIRS (National Fire
  Incident Reporting System — fire data).
- **What it provides:** Fire incident data (NFIRS), emergency management
  data, some fire/EMS data. Volusia County Emergency Management may have
  public data.
- **Volusia coverage:** DIRECT (local).
- **Access method:** NFIRS data (some public via FEMA/USFA), local emergency
  management, public records. Public.
- **Priority:** LOW-MEDIUM.
- **Notes:** NFIRS fire data may have Volusia County fire department data
  (if submitted). Emergency management public data (evacuation zones, etc.)
  is in Domain 5 (environment/climate/disaster). Public safety is partly
  Domain 4 (crime) and Domain 5 (emergency/disaster).

### Other health data (Medicare, Medicaid, BRFSS, etc.)
- **Medicare:** CMS Medicare data (some public — e.g. Care Compare, provider
  data, some county-level health service area data). Public. Useful for
  healthcare access/quality at county level.
- **Medicaid:** Florida Medicaid data — restricted (not public at granular
  level). Some aggregate data may be public.
- **BRFSS:** CDC BRFSS (Behavioral Risk Factor Surveillance System) — state-
  level health survey data; county-level BRFSS is limited (small areas).
  CDC PLACES uses BRFSS for model-based estimates. Direct BRFSS county data
  is sparse.
- **Priority:** Medicare (MEDIUM — public provider/data), BRFSS (LOW for
  county direct — use PLACES), Medicaid (LOW — restricted).
- **Notes:** CDC PLACES is the best public tract-level health source. FL
  DOH CHARTS is the Florida-specific source. Medicare Care Compare is useful
  for provider data.

### Social determinants / community indicators (city data, Opportunity
Atlas, etc.)
- **Opportunity Atlas (Census Bureau / Raj Chetty et al.):** Public data on
  neighborhood-level outcomes (income, incarceration, etc.) based on Census
  data. May have Volusia County tract data. Public. Useful for opportunity/
  economic mobility analysis.
- **City Data / neighborhood data:** Various local sources.
- **Priority:** MEDIUM (Opportunity Atlas if available for Volusia tracts).
- **Notes:** Opportunity Atlas is a public resource for neighborhood-level
  outcomes. Check if Volusia County is covered. Useful for equity and
  opportunity analysis.

---

4.2 TOP PICKS FOR PROJECT VOLUSIA — DEMOGRAPHICS/EDUCATION/HEALTH/PUBLIC SAFETY

1. Census ACS (5-year) — tract-level demographics, education, language,
   disability, vehicle access, household (HIGH — primary demographic detail,
   maps)
2. Census Decennial 2020 + PEP — official population count and annual
   estimates (HIGH — population baseline)
3. Florida EDR population projections — forward-looking county population
   (HIGH — planning, demand)
4. CDC PLACES — tract-level health outcomes/behaviors/risk factors
   (HIGH — best public tract health data)
5. Florida DOH CHARTS — Florida/county vital statistics, disease data,
   health profiles (HIGH — Florida-specific health)
6. FL DOE school report cards — Volusia County Schools performance, school-
   level data (HIGH — education performance)
7. NCES CCD/IPEDS — school district data, higher ed institutional data
   (Embry-Riddle, Bethune-Cookman, Daytona State, Stetson) (HIGH — education
   institutions)
8. County Health Rankings — county health composite + components (MEDIUM-
   HIGH — benchmarking)
9. FBI UCR/NIBRS + FDLE crime data — Volusia crime stats (MEDIUM-HIGH —
   public safety)
10. Volusia County SO public records / open data crime feed (if available)
    (MEDIUM — local crime detail)
11. ACS educational attainment + FL DOE data (MEDIUM-HIGH — education)
12. Opportunity Atlas / social determinants (MEDIUM — if available)

---

4.3 CAVEATS AND FLAGS — DEMOGRAPHICS/EDUCATION/HEALTH/PUBLIC SAFETY

- ACS margins of error matter, especially at tract level. Report with MOEs
  or use appropriate caution. ACS is a survey, not a census.
- ACS does not cover health outcomes (no disease data), crime (no crime
  data), or detailed education performance (no school grades). Those come
  from other sources (CDC PLACES, FL DOH, FL DOE, FBI/FDLE).
- CDC PLACES is model-based (small area estimation from BRFSS). It's an
  estimate, not a direct measurement. Use with awareness; don't treat as
  ground truth. Combine with FL DOH CHARTS for Florida-specific direct
  data where available.
- FL DOH CHARTS may require a CHARTS account for some data. Plan for that
  access step.
- School report card grades are Florida-specific accountability; national
  comparisons use different frameworks. FL DOE data is Florida's.
- Crime data has well-known limitations (underreporting, classification,
  reporting practice changes, NIBRS transition affecting comparability).
  Use multiple sources and note limitations.
- Volusia County SO public records and open data crime feed (if available)
  may provide more granular local data than FDLE/FBI aggregates.
- Health data at tract level is sparse publicly — CDC PLACES is the key
  source filling this gap. Hospital CHNAs may have additional local health
  data (check Halifax Health, Florida Hospital DeLand CHNAs).
- Population: PEP is the Census Bureau's official estimate; Florida EDR
  projections are forecasts. Use PEP for "current" population and EDR for
  "future" population. Different products.
- Higher ed institutions: IPEDS is the comprehensive federal source; use it
  for cross-institution comparison. Individual institutions may publish
  additional local data.

---

5. DOMAIN 5 — TRANSPORTATION, INFRASTRUCTURE, BROADBAND, ENVIRONMENT,
CLIMATE, NATURAL HAZARDS, GEOGRAPHY/GIS

---

5.1 SOURCE LIST

### Florida Department of Transportation (FDOT) — Traffic Data / TRANS
- **Publisher:** Florida DOT (fdot.gov/planning/statistics)
- **What it provides:** Traffic count data — Annual Average Daily Traffic
  (AADT), vehicle classification counts, traffic maps, traffic data by
  road segment (state roads and some local roads). FDOT publishes traffic
  count data and maps. Florida TRANS (Transportation Information System).
- **Volusia coverage:** DIRECT — Volusia County roads (state roads and
  signaled intersections). FDOT traffic counts for Volusia County roads.
- **Access method:** FDOT website (fdot.gov/planning/statistics), traffic
  data downloads, FDOT interactive maps (TranStat? FDOT traffic data
  portal), GIS data. Public.
- **Update frequency:** Annual (AADT updates), with some more frequent
  counts.
- **License/terms:** Public (Florida state government).
- **Friction:** LOW-MEDIUM. FDOT traffic data is available via web portal
  and downloads; GIS data may be available. FDOT data is the authoritative
  Florida traffic source.
- **Priority:** HIGH
- **Why:** Traffic volume data for Volusia County roads — a transportation
  and economic indicator (traffic = movement of people/goods). Useful for
  transportation analysis, maps (traffic heat maps, corridor analysis),
  infrastructure planning, and economic development (access corridors).
- **Notes:** FDOT traffic counts are the Florida source. Compare with
  Volusia County traffic data if available (county may have additional
  traffic data for county roads). FDOT covers state roads primarily; county
  roads may have separate data.

### Volusia County — Traffic / Transportation data (VOTRAN, county roads)
- **Publisher:** Volusia County (Transportation / VOTRAN)
- **What it provides:** VOTRAN (Volusia Oncology? No — Volusia County Public
  Transit / VOTRAN) ridership data, route maps, county traffic data (county
  roads, traffic signals, transportation planning). VOTRAN is the public
  transit system. Volusia County may have traffic data for county roads.
- **Volusia coverage:** DIRECT — Volusia County transit and county roads.
- **Access method:** Volusia County website (volusia.org/services/public-
  transit), VOTRAN reports, ridership data, GIS data (transit routes on
  Open Data portal). Public.
- **Update frequency:** VOTRAN ridership reports periodic (monthly/annual);
  GIS data updated.
- **License/terms:** Public.
- **Friction:** LOW-MEDIUM. VOTRAN ridership data may be in reports; GIS
  data on Open Data portal. County traffic data availability varies.
- **Priority:** MEDIUM-HIGH
- **Why:** Public transit (VOTRAN) ridership and coverage is important for
  transportation equity (who has transit access), resident mobility, and
  transportation maps. County traffic data complements FDOT.
- **Notes:** VOTRAN is Volusia County's public transit system. Ridership
  data is a transit usage indicator. Check VOTRAN for ridership reports
  and the Open Data portal for transit GIS layers (routes, stops).

### FDOT — Annual Traffic Maps / TRIS (Transportation Routing Information
System?) / Florida traffic GIS
- **Publisher:** FDOT
- **What it provides:** FDOT traffic data GIS layers, annual traffic maps,
  traffic count GIS data. FDOT publishes traffic data in GIS format.
- **Volusia coverage:** DIRECT.
- **Access method:** FDOT GIS data, Open Data, FDOT traffic maps. Public.
- **Friction:** LOW-MEDIUM (GIS data availability).
- **Priority:** MEDIUM-HIGH (GIS traffic data for maps)
- **Notes:** FDOT traffic GIS data is valuable for transportation maps.

### U.S. DOT — National Bridge Inventory (NBI)
- **Publisher:** Federal Highway Administration (FHWA), U.S. DOT
- **What it provides:** Bridge inventory — location, condition, type, size,
  traffic, structural attributes for bridges in the U.S. (including Volusia
  County bridges). NBI data is public.
- **Volusia coverage:** DIRECT — Volusia County bridges (all bridges in the
  county reported to NBI).
- **Access method:** FHWA NBI website (fhwa.dot.gov/bridge/nbi), NBI data
  downloads (CSV, flat files), web tools. Public.
- **Update frequency:** Annual (NBI updated annually).
- **License/terms:** Public domain (U.S. government).
- **Friction:** LOW. Data downloads available.
- **Priority:** MEDIUM
- **Why:** Bridge infrastructure data — condition, age, traffic on Volusia
  County bridges. Relevant for infrastructure analysis, transportation
  resilience (bridge condition is infrastructure health), and maps. Not a
  headline indicator but useful infrastructure detail.
- **Notes:** NBI is the standard bridge inventory. Volusia County bridges
  are in it. Useful for infrastructure condition and resilience analysis.

### FCC Broadband Map — Internet access by address
- **Publisher:** FCC (Federal Communications Commission)
- **What it provides:** National Broadband Map — broadband availability by
  address (and geography), provider-level, technology, speeds. Interactive
  map and data. Shows where broadband service is (and isn't) available at
  the address level. Covers fixed and mobile broadband.
- **Volusia coverage:** DIRECT — Volusia County addresses and geography
  (census block level). FCC Broadband Map has block-level broadband
  availability data.
- **Access method:** FCC Broadband Map website (broadbandmap.fcc.gov) —
  interactive map, address lookup, data downloads (bulk data available —
  the FCC publishes the broadband map data for download). Public.
- **Update frequency:** The FCC Broadband Map is updated periodically
  (annual-ish updates; the map went live 2022, updated since). Data
  challenges and updates ongoing.
- **License/terms:** Public (U.S. government). FCC broadband map data is
  public.
- **Friction:** LOW-MEDIUM. Interactive map and address lookup are easy;
  bulk data download is available but may be large/complex. The FCC map
  has known controversies (accuracy concerns — overcount/under-count
  issues; see caveats). Use with awareness.
- **Priority:** HIGH
- **Why:** Broadband access is a named Project Volusia priority (digital
  equity). The FCC Broadband Map is the official federal source for
  broadband availability at address/block level. Essential for the digital
  equity analysis, broadband maps, resident well-being report, and the
  "who lacks internet access" question. SF cratering a county-level view
  from the address-level map.
- **Notes:** The FCC Broadband Map has been criticized for accuracy issues
  (overreporting availability in some cases). It's the best public federal
  source, but treat with appropriate caution. Challenge process exists for
  corrections. Combine with ACS broadband questions (ACS has "do you have
  a computer/internet" questions at tract level) for a triangulated view.
  ACS broadband data is survey-based (household-level self-report) at tract
  resolution; FCC map is provider-reported availability at address/block
  level. Both are useful and have different strengths.

### ACS — Computer and Internet Access (Census)
- **Publisher:** Census Bureau (ACS)
- **What it provides:** Household computer and internet access data — device
  access (computers, smartphones), internet subscription types, broadband
  subscription, by geography (tract, county, etc.). ACS tables on computer
  and internet use (e.g. S2801, B28001-B28010, etc.).
- **Volusia coverage:** DIRECT — Volusia County, tracts.
- **Access method:** Census API, data.census.gov. Public.
- **Update frequency:** 5-year estimates annual; 1-year annual.
- **License/terms:** Public domain.
- **Friction:** LOW.
- **Priority:** HIGH
- **Why:** ACS broadband/computer access data at tract level is the survey-
  based complement to the FCC Broadband Map. ACS tells you who has internet
  (household self-report) by tract; FCC tells you what's available by
  address. Together they give a fuller digital equity picture. Essential for
  the digital equity analysis and maps.
- **Notes:** ACS broadband data is self-reported household access, not
  availability. FCC map is provider-reported availability. Different
  concepts. ACS is survey-based (some MOE at tract level).

### USGS — Water Data (streams, groundwater, water quality) — Volusia
- **Publisher:** U.S. Geological Survey (USGS)
- **What it provides:** Water data — streamflow, groundwater levels, water
  quality, water use, real-time water data. USGS Water Data for Florida
  (waterdata.usgs.gov). Volusia County has USGS stream gauges (e.g. St. Johns
  River, Tomoka River, Halifax River, etc.) and groundwater monitoring.
- **Volusia coverage:** DIRECT — Volusia County water data (stream gauges,
  groundwater wells in Volusia).
- **Access method:** USGS Water Data portal (waterdata.usgs.gov/fl/nwis),
  NWIS (National Water Information System), real-time data, API (USGS Water
  Data Services / NWIS API), data downloads. Public.
- **Update frequency:** Real-time (streamflow, groundwater) and periodic
  (water quality, water use).
- **License/terms:** Public domain (U.S. government).
- **Friction:** LOW-MEDIUM. Real-time data and API are accessible. USGS
  data is extensive and can be complex to query for specific sites.
- **Priority:** MEDIUM-HIGH
- **Why:** Water resources data — streamflow, groundwater, water quality —
  for Volusia County. Important for environment, water resource planning,
  climate/resilience (water is a resilience issue in Florida — flooding,
  sea level rise, groundwater), and environmental maps. Volusia County has
  significant water resources (St. Johns River, Halifax River, Tomoka River,
  lakes, wetlands).
- **Notes:** USGS water data is extensive; identify the specific Volusia
  gauges/wells of interest. Real-time streamflow is readily available.
  Water quality and water use data may require more querying. Florida water
  management districts (see below) also have water data.

### Florida Water Management Districts — Water data
- **Publisher:** Florida's water management districts (St. Johns River Water
  Management District covers Volusia County — SJRWMD; also South Florida
  Water Management District is south; Volusia is in St. Johns River WMD).
- **What it provides:** Water resource data — water levels, flows, water
  quality, water supply, flood protection, environmental data, GIS data.
  St. Johns River Water Management District (SJRWMD) covers Volusia County.
- **Volusia coverage:** DIRECT — Volusia County (SJRWMD jurisdiction).
- **Access method:** SJRWMD website (sjrwmd.gov), data portals, GIS data,
  water data, reports. Public.
- **Update frequency:** Varies (real-time water levels, periodic reports).
- **License/terms:** Public (Florida state government authority).
- **Friction:** LOW-MEDIUM. SJRWMD has data portals and GIS.
- **Priority:** MEDIUM-HIGH
- **Why:** The St. Johns River Water Management District is the water
  authority for Volusia County. Water levels, flows, water supply, flood
  data, environmental water data — important for water resource planning,
  environment, and resilience. Florida's water management district system
  is a key water data source.
- **Notes:** Volusia County is in the St. Johns River Water Management
  District (SJRWMD). Confirm SJRWMD coverage of Volusia (yes — SJRWMD
  covers the St. Johns River basin including Volusia). SJRWMD data is
  Florida water data for Volusia. Also note: Volusia County has many lakes
  and the Halifax River/Intracoastal.

### FEMA — Flood Map Service Center (Flood Insurance Rate Maps — FIRM)
- **Publisher:** FEMA (Federal Emergency Management Agency)
- **What it provides:** Flood hazard maps (Flood Insurance Rate Maps — FIRM),
  flood zones (100-year / SFHA, 500-year, etc.), flood risk data. FEMA
  Flood Map Service Center (msc.fema.gov). Flood maps for Volusia County
  (coastal and inland flooding — Volusia has significant flood risk, both
  coastal and inland/stormwater).
- **Volusia coverage:** DIRECT — Volusia County flood maps (FIRM panels,
  flood zones by parcel/area).
- **Access method:** FEMA Flood Map Service Center (msc.fema.gov) — search
  by address/community, view/download FIRM panels (PDF), flood zone data
  (FEMA provides flood map data in GIS/PDF). FEMA also has flood risk
  data (FEMA Flood Risk Data / National Flood Hazard Layer — NFHL — GIS
  data). Public.
- **Update frequency:** FIRMs updated periodically (new FIRMs, map updates).
  FEMA updates the National Flood Hazard Layer (NFHL) as maps change.
  Volusia County has had FIRM updates (search results mention FEMA updating
  Volusia County FIRM).
- **License/terms:** Public (U.S. government). FEMA flood map data is public.
- **Friction:** LOW-MEDIUM. MSC website for viewing/downloading FIRM panels
  (PDF). NFHL GIS data available for programmatic use. FIRM panels are PDF
  (somewhat unwieldy for programmatic use); NFHL GIS data is better for
  maps/analysis. Flood zone determinations by address are available via
  MSC.
- **Priority:** HIGH
- **Why:** Flood risk is a top Volusia County issue (hurricanes, coastal
  flooding, stormwater, insurance crisis). FEMA flood maps are the baseline
  flood hazard data. Essential for the environment/climate maps (flood
  zones), resilience analysis, resident well-being (flood risk disclosure),
  and the insurance crisis narrative. Every Volusia property is in some
  flood zone context.
- **Notes:** FEMA flood maps have limitations — they reflect current FIRM
  data which may not capture all flood risk (e.g. future sea level rise,
  recent development changes, some local flooding). FEMA maps are the
  regulatory baseline for flood insurance requirements. Volusia County has
  been updating FIRMs (per search results). Use NFHL GIS data for
  programmatic flood zone mapping. Also note: FEMA flood maps are being
  modernized; the FCC Broadband Map has accuracy controversies, and FEMA
  flood maps have similar "as-designed" limitations — treat as regulatory
  baseline, not complete risk picture. See also First Street Foundation /
  Flood Factor (private; some free data but mostly gated) as a supplemental
  flood risk source — note it's private. Florida has its own flood risk
  data too (see Florida climate/flood sources).

### NOAA — Climate data / Weather / Sea Level Rise / Coastal Flood
- **Publisher:** NOAA (National Oceanic and Atmospheric Administration)
- **What it provides:** 
  - Climate data: weather station data (temperature, precipitation, etc.),
    climate normals, extremes, U.S. Climate Resilience Toolkit.
  - Sea level rise: NOAA Sea Level Rise Viewer, sea level rise projections,
    tidal data, coastal flood data.
  - Coastal flood: NOAA coastal flood forecasting, inundation maps.
  - Weather/climate data for Volusia County (weather stations — e.g. Daytona
    Beach Int'l AP weather station, Daytona Beach shores, etc.).
- **Volusia coverage:** DIRECT — Volusia County weather/climate data (NOAA
  stations in Volusia), sea level rise for the Volusia coastline (Atlantic
  coast), coastal flood data. NOAA has sea level rise data for the Florida
  Atlantic coast.
- **Access method:** NOAA Climate Data Online (CDO) — climate data search
  and download (ncdc.noaa.gov / climate.gov), NOAA API (NCEI API), sea
  level rise viewer (coast.noaa.gov/slr), NOAA coastal flood data, NWS
  data. Public.
- **Update frequency:** Real-time (weather), periodic (climate normals,
  sea level rise updates).
- **License/terms:** Public domain (U.S. government).
- **Friction:** LOW-MEDIUM. NOAA CDO and APIs are accessible. Sea level
  rise viewer is interactive. Some data sets are large.
- **Priority:** MEDIUM-HIGH
- **Why:** Climate and weather data — essential for the climate/environment
  analysis, resilience, and the "what's the climate risk" question.
  Volusia County is coastal (Atlantic) and faces hurricanes, sea level rise,
  coastal flooding, extreme heat. NOAA is the primary federal climate/
  weather source. Weather station data for Volusia (e.g. Daytona Beach)
  gives local climate context.
- **Notes:** NOAA has many data products — identify the specific ones for
  Volusia (weather stations, sea level rise for the coast, coastal flood).
  NOAA Sea Level Rise Viewer is a good interactive tool. NOAA's climate
  data online (CDO) has station data. NCEI has climate normals and extremes.
  For sea level rise projections, NOAA has projections (e.g. 2017 NOAA sea
  level rise report, updated projections). NOAA is the go-to federal
  climate source.

### USGS — National Land Cover Database (NLCD)
- **Publisher:** USGS (USGS EROS)
- **What it provides:** National Land Cover Database — land cover classification
  (impervious surface, tree canopy, land cover type — forest, urban,
  agriculture, wetland, water, etc.) for the U.S. at 30m resolution, with
  temporal versions (e.g. 2001, 2006, 2011, 2016, 2021). Land cover change.
  Also USGS has tree canopy cover (from NLCD and USFS).
- **Volusia coverage:** DIRECT — Volusia County land cover (NLCD covers the
  whole U.S. including Volusia).
- **Access method:** MRLC (Multi-Resolution Land Characteristics Consortium)
  website (mrlc.gov), USGS Earth Explorer, USGS data downloads, NLCD data
  (GeoTIFF, etc.). Public.
- **Update frequency:** NLCD releases periodic (e.g. NLCD 2021 released
  recently). Land cover change products.
- **License/terms:** Public domain (U.S. government).
- **Friction:** LOW-MEDIUM. NLCD data is available as GeoTIFF/rasters;
  download and processing required for analysis. MRLC portal is user-
  friendly.
- **Priority:** HIGH
- **Why:** Land cover data — what's forest, urban, agriculture, wetland,
  water in Volusia County, and how it's changing. Essential for environment/
  land use maps, environmental analysis, urban growth analysis, tree canopy
  (urban heat island), and conservation. NLCD is the standard national land
  cover product.
- **Notes:** NLCD is 30m resolution raster — good for county-wide analysis
  but not parcel-level. Use with county parcel/land use data for more detail.
  NLCD's impervious surface and tree canopy layers are particularly useful
  (urban heat, green space). NLCD 2021 is the most recent (as of 2026).

### USFS / NLCD — Tree Canopy Cover
- **Publisher:** U.S. Forest Service (USFS) / NLCD
- **What it provides:** Tree canopy cover percentage by census block group
  (and other geographies) — derived from NLCD and USFS data. Tree canopy is
  part of NLCD (canopy cover layer).
- **Volusia coverage:** DIRECT — Volusia County block group / tract tree
  canopy.
- **Access method:** Same as NLCD (USGS/MRLC). Also USFS Tree Canopy data.
  Public.
- **Priority:** MEDIUM-HIGH
- **Why:** Tree canopy is an environmental quality / urban heat island /
  green space indicator. Useful for environment maps and equity (tree cover
  disparities). Part of NLCD canopy layer.
- **Notes:** Tree canopy layer from NLCD is the primary public source.

### EPA — Air Quality (AirNow, EPA Air Data)
- **Publisher:** U.S. EPA
- **What it provides:** Air quality data — AirNow (real-time air quality
  index, monitor data), EPA Air Data (annual air quality, PM2.5, ozone,
  etc. by county/monitor), EPA environmental justice screening (EJSCREEN —
  includes air quality and other environmental indicators by geography).
- **Volusia coverage:** DIRECT — Volusia County air quality (monitors, county
  air quality). Volusia County may have EPA air quality monitors.
- **Access method:** AirNow (airnow.gov) — real-time and forecast AQI, API.
  EPA Air Data (epa.gov/air-data) — downloads. EJSCREEN (epa.gov/ejscreen) —
  environmental justice screening tool with data downloads. Public.
- **Update frequency:** AirNow real-time; EPA annual air data; EJSCREEN
  periodic.
- **License/terms:** Public domain (U.S. government).
- **Friction:** LOW. AirNow and EPA data are accessible. EJSCREEN is an
  interactive tool with data downloads.
- **Priority:** MEDIUM
- **Why:** Air quality data for Volusia County — environmental health
  indicator. EPA EJSCREEN combines air quality with other environmental
  justice indicators (demographics, etc.) — useful for environmental justice
  analysis. Good for environment maps and resident well-being.
- **Notes:** Volusia County air quality is generally moderate (coastal,
  not major industrial air pollution sources like some urban areas, but does
  have traffic/ozone). EPA air data has monitor-level data; county aggregate
  may be limited if few monitors. EJSCREEN is a good composite environmental
  justice tool.

### EPA — EJSCREEN (Environmental Justice Screening)
- **Publisher:** U.S. EPA
- **What it provides:** EJSCREEN — environmental justice screening and
  mapping tool. Combines environmental indicators (air quality, diesel PM,
  ozone, traffic proximity, lead paint, Superfund, RMP, wastewater, etc.)
  with demographic indicators (low income, minority, etc.) at census block
  group level. Provides EJ indices and report by geography.
- **Volusia coverage:** DIRECT — Volusia County block groups (EJSCREEN covers
  the whole U.S. at block group level).
- **Access method:** EJSCREEN tool (epa.gov/ejscreen) — interactive map,
  report by area, data downloads (EPA provides EJSCREEN data downloads).
  Public.
- **Update frequency:** Periodic (EJSCREEN updates).
- **License/terms:** Public (U.S. government).
- **Friction:** LOW-MEDIUM. Interactive tool; data downloads available.
- **Priority:** MEDIUM-HIGH
- **Why:** Environmental justice data — combines environmental and demographic
  indicators. Useful for equity analysis, environment maps, and identifying
  disparity areas in Volusia County. EJSCREEN is the standard EPA EJ tool.
- **Notes:** EJSCREEN is a screening tool (indicative, not definitive). Use
  for initial EJ analysis. EPA also has EJSCREEN data downloads for
  programmatic use.

### FEMA — Natural Hazards / Disaster / Hurricane data
- **Publisher:** FEMA
- **What it provides:** Disaster declarations, hazard mitigation data,
  flood (above), some disaster data. FEMA disaster declarations for Florida/
  Volusia (e.g. hurricanes Charley, Frances, Ivan, Jeanne 2004; Irma 2017;
  Ian 2022; etc. — Volusia has had multiple disaster declarations).
- **Volusia coverage:** DIRECT — Volusia County disaster declarations.
- **Access method:** FEMA disaster declarations data (FEMA OpenFEMA API —
  disaster declarations, public). Public.
- **Priority:** MEDIUM
- **Notes:** FEMA disaster declarations for Volusia (hurricanes) are a
  resilience record. OpenFEMA API has disaster declarations data.

### First Street Foundation — Flood Factor / Fire Factor / climate risk
- **Publisher:** First Street Foundation (private nonprofit)
- **What it provides:** Flood Factor (property-level flood risk), Fire Factor,
  wind risk, heat risk, sea level rise risk — property-level and community-
  level climate risk data. Some free public data (e.g. Flood Factor ratings
  for individual properties are publicly viewable on floodfactor.com; bulk
  data may have limited free access). First Street's data is widely used.
- **Volusia coverage:** DIRECT — Volusia County properties (Flood Factor
  ratings).
- **Access method:** FloodFactor.com — property lookup (free public view);
  bulk data may be gated/limited free. First Street publishes some data
  openly (e.g. some community-level data) but detailed property-level bulk
  data may require access. Check current First Street data access.
- **Update frequency:** Periodic updates.
- **License/terms:** First Street is a nonprofit; some data is public/free,
  some may be restricted. Flood Factor property ratings are publicly
  viewable. Bulk data access varies.
- **Friction:** MEDIUM — property-level Flood Factor is publicly viewable
  but bulk data may be limited. First Street is a private nonprofit, not
  government; its data is widely used but check terms.
- **Priority:** MEDIUM
- **Why:** Supplemental flood/climate risk data beyond FEMA — First Street's
  Flood Factor is a property-level flood risk metric that goes beyond FEMA
  flood zones (includes future risk, heavy rain, etc.). Useful for the
  flood risk analysis and resilience narrative. Public property lookup is
  free; bulk data access varies.
- **Notes:** First Street is not a government source; it's a nonprofit with
  proprietary methodology. Use as a supplement to FEMA, not a replacement.
  Free public property lookup is available; bulk programmatic access may be
  limited. Note the source type (nonprofit, model-based).

### Florida climate / sea level rise / coastal data (Florida-specific)
- **Publisher:** Florida DEP, Florida Climate Adaptation, Florida Seagrant,
  Florida ocean/coastal data, Florida survey/CMD
- **What it provides:** Florida-specific climate, sea level rise, coastal
  data. Florida has state-level climate adaptation resources. Florida DEP
  coastal data. Florida Sea Grant (UF/FAU/etc.) has coastal data.
- **Volusia coverage:** DIRECT (Florida coastal data includes Volusia).
- **Access method:** Florida DEP, Florida climate resources, Sea Grant.
  Public.
- **Priority:** MEDIUM
- **Notes:** Florida has state-level coastal/sea level rise data that
  complements NOAA. Florida DEP and Sea Grant are options.

### USGS — Elevation / DEM / Topography (Volusia)
- **Publisher:** USGS
- **What it provides:** Elevation data — DEM (Digital Elevation Model),
  LiDAR point clouds, topography. USGS 3DEP (3D Elevation Program) LiDAR
  data for Florida (including Volusia). USGS National Map.
- **Volusia coverage:** DIRECT — Volusia County elevation/LiDAR.
- **Access method:** USGS National Map (nationalmap.gov), USGS Earth Explorer,
  USGS 3DEP LiDAR data, OpenTopography (some LiDAR). Public.
- **Update frequency:** Periodic (LiDAR acquisitions).
- **License/terms:** Public domain (U.S. government).
- **Friction:** MEDIUM — LiDAR data is large; processing required. USGS
  National Map and Earth Explorer are the portals.
- **Priority:** MEDIUM-HIGH
- **Why:** Elevation data — critical for flood modeling, coastal analysis,
  terrain analysis, and maps. Volusia County LiDAR is available via USGS
  3DEP. Essential for detailed flood/terrain analysis and environment maps.
- **Notes:** USGS 3DEP LiDAR for Volusia County — check coverage and
  availability on USGS National Map / Earth Explorer. LiDAR is high-
  resolution elevation; DEM is derived. Useful for detailed analysis.

### Census Bureau — TIGER/Line Shapefiles / GIS boundaries
- **Publisher:** U.S. Census Bureau
- **What it provides:** Geographic boundary files — census tract, county,
  ZIP ZCTA, city/place, school district, county subdivision, etc. TIGER/
  Line shapefiles and GeoJSON. Also Census geocoder. The standard U.S.
  geographic boundaries for mapping and spatial analysis.
- **Volusia coverage:** DIRECT — Volusia County and all 하위 geographies.
- **Access method:** Census Bureau TIGER/Line download page (census.gov/
  geo/tiger), API, GeoJSON/shapefile downloads. Public.
- **Update frequency:** Annual (TIGER/Line updated annually, usually).
- **License/terms:** Public domain (U.S. government).
- **Friction:** LOW. Directly downloadable shapefiles/GeoJSON. The standard
  for U.S. mapping.
- **Priority:** HIGH
- **Why:** The foundational geographic boundaries for all spatial analysis
  and maps in Project Volusia. Tract, county, ZIP, city boundaries — used
  everywhere. Essential for the Map folder and all geospatial work.
- **Notes:** TIGER/Line is the standard. Use the most recent vintage.
  Census also provides the geocoder (geocoding.geo.census.gov) for
  address-to-coordinate conversion. For more current/accurate boundaries
  (e.g. city limits changes), check local GIS (Volusia County Open Data).

### Volusia County — GIS / Open Data portal (ArcGIS Hub)
- **Publisher:** Volusia County (GIS / Geographic Information Services)
- **What it provides:** Volusia County's open GIS data — parcels, zoning,
  land use, flooding, evacuation zones, transportation, transit, public
  safety, parks, schools, administrative boundaries, aerial imagery, and
  more. Volusia County Open Data portal on ArcGIS Hub (opendata-volusiacountyfl
  .hub.arcgis.com). ArcGIS REST services (maps5.vcgov.org/arcgis/rest/services/
  Open_Data/Open_Data_3/FeatureServer). "Geohub" with public GIS applications.
- **Volusia coverage:** DIRECT — Volusia County, comprehensive local GIS
  data.
- **Access method:** ArcGIS Hub open data site (opendata-volusiacountyfl.
  hub.arcgis.com) — browse and download datasets (various formats). ArcGIS
  REST API for feature layers (query, GeoJSON, JSON). Some data also
  available via Equator (equatorstudios.com/florida_volusia) which mirrors
  Volusia County GIS data for download (parcels, LiDAR, contours, building
  footprints, DEMs). Public.
- **Update frequency:** Varies by dataset (parcels updated, zoning updated,
  etc.).
- **License/terms:** Public (Volusia County open data). ArcGIS Online/ Hub
  data is publicly accessible. Volusia County's open data is public.
- **Friction:** LOW-MEDIUM. ArcGIS Hub is user-friendly for browsing/
  downloading. REST API is good for programmatic access (GeoJSON, JSON).
  Some datasets may be large. Equator provides an alternative download
  portal for Volusia GIS data (LiDAR, parcels, contours, building
  footprints, DEMs) — convenient for engineers/developers. Note: Equator
  is a third-party portal aggregating public GIS data; the primary source is
  Volusia County's own Open Data portal.
- **Priority:** HIGH
- **Why:** The single most important local GIS data source for Project
  Volusia. Volusia County's own open data portal has parcels, zoning, flood,
  evacuation zones, transit, public safety locations, parks, schools,
  boundaries, imagery, and more — directly from the county. This is the
  primary source for the Map folder and all local spatial analysis. The
  ArcGIS REST API enables programmatic access.
- **Notes:** Start here for local GIS data. The ArcGIS Hub open data site
  is the main entry. The REST endpoint (maps5.vcgov.org/arcgis/rest/services/
  Open_Data/Open_Data_3/FeatureServer) has multiple layers. Volusia County
  GIS Services (volusia.org/services/financial-and-administrative-services/
  finance-department/information-technology/geographic-information-services)
  is the department. Custom data requests are available from GIS (fee-based
  possibly). Equator (equatorstudios.com/florida_volusia) is a convenient
  third-party mirror for Volusia GIS data (LiDAR, parcels, contours,
  building footprints, DEMs) — useful but the authoritative source is
  Volusia County.

### USGS — National Hydrography Dataset (NHD) / Water bodies
- **Publisher:** USGS
- **What it provides:** National Hydrography Dataset — water features (streams,
  rivers, lakes, wetlands, coastlines) for the U.S. NHD Plus. Volusia County
  water bodies (St. Johns River, Halifax River, Tomoka River, lakes, etc.).
- **Volusia coverage:** DIRECT.
- **Access method:** USGS National Map, NHD downloads, USGS Hydrography.
  Public.
- **Priority:** MEDIUM
- **Notes:** NHD is the standard U.S. hydrography. Useful for water maps.
  Combine with USGS water data for water resources. Florida water management
  district data also has water features.

### USGS / NOAA — Coastal / shoreline data
- **Publisher:** USGS, NOAA
- **What it provides:** Coastal shoreline data, shoreline change, coastal
  elevation (CoNED — Coastal National Elevation Database), bathymetry.
  Volusia County coastline (Atlantic coast, Halifax River/Intracoastal).
- **Volusia coverage:** DIRECT (Volusia coastline).
- **Access method:** USGS, NOAA coastal data portals. Public.
- **Priority:** MEDIUM
- **Notes:** Coastal shoreline and elevation data for the Volusia coast —
  relevant for coastal erosion, sea level rise, coastal flood analysis.

### USDA NRCS — Soil data (SSURGO) / Web Soil Survey
- **Publisher:** USDA Natural Resources Conservation Service (NRCS)
- **What it provides:** Soil survey data — SSURGO (Soil Survey Geographic
  Database) soil maps, soil properties, by county. Web Soil Survey.
- **Volusia coverage:** DIRECT — Volusia County soil data.
- **Access method:** Web Soil Survey (websoilsurvey.sc.egov.usda.gov), NRCS
  soil data downloads (SSURGO GIS data). Public.
- **Priority:** MEDIUM
- **Notes:** Soil data is relevant for land use, agriculture, construction,
  environmental. Volusia County soil data from NRCS. SSURGO is the detailed
  soil survey.

### USDA — Census of Agriculture (Volusia)
- **Publisher:** USDA NASS (National Agricultural Statistics Service)
- **What it provides:** Census of Agriculture — agricultural data (farm
  counts, acreage, production, livestock, values) by county, every 5 years
  (2017, 2022, etc.).
- **Volusia coverage:** DIRECT — Volusia County agriculture census.
- **Access method:** USDA NASS website, Census of Agriculture data, API.
  Public.
- **Priority:** MEDIUM
- **Notes:** Volusia County has agriculture (citrus, vegetables, equine,
  nurseries, etc.). Census of Agriculture gives agricultural data for
  Volusia. Useful for the economic/land use analysis (agriculture is part
  of Volusia's economy and land use).

### 기타 연방/주/로컬 GIS 데이터 (USGS, NOAA, Florida DEP, etc.)
- **See entries above.** USGS (land cover, elevation, water, hydrography),
  NOAA (climate, sea level, coastal), FEMA (flood), EPA (air, EJSCREEN),
  Florida DEP (environment, coastal), water management districts (water),
  FDOT (transportation GIS), Volusia County (open data portal with many
  layers). These are the main geospatial sources.

---

5.2 TOP PICKS FOR PROJECT VOLUSIA — TRANSPORTATION/INFRASTRUCTURE/
BROADBAND/ENVIRONMENT/CLIMATE

1. Volusia County Open Data portal (ArcGIS Hub) — comprehensive local GIS
   data (parcels, zoning, flood, evacuation, transit, public safety, parks,
   schools, imagery, etc.) (HIGH — primary local GIS source)
2. FCC Broadband Map — address-level broadband availability + ACS computer/
   internet access (HIGH — digital equity, named priority)
3. FEMA Flood Map Service Center / NFHL — flood zones, flood risk (HIGH —
   top Volusia issue)
4. Census TIGER/Line — geographic boundaries (tract, county, ZIP, city)
   (HIGH — foundational mapping)
5. FDOT traffic data — AADT, traffic counts, traffic GIS (HIGH — transportation
   data)
6. NOAA climate/weather/sea level rise — local climate, coastal flood, sea
   level rise (HIGH — climate/resilience)
7. USGS NLCD — land cover, impervious surface, tree canopy (HIGH — environment/
   land use maps)
8. USGS 3DEP LiDAR / DEM — elevation data (MEDIUM-HIGH — detailed terrain/
   flood analysis)
9. USGS water data + St. Johns River WMD — water resources (MEDIUM-HIGH —
   water, environment)
10. EPA AirNow / EJSCREEN — air quality + environmental justice (MEDIUM-HIGH —
    environment/equity)
11. U.S. DOT National Bridge Inventory — bridge data (MEDIUM — infrastructure)
12. VOTRAN ridership / Volusia transit (MEDIUM — transit equity)
13. FEMA disaster declarations / OpenFEMA (MEDIUM — resilience record)
14. First Street Flood Factor (public property lookup) (MEDIUM — supplemental
    flood risk)
15. USDA Census of Agriculture (MEDIUM — agriculture land use/economy)
16. Florida DEP / Sea Grant coastal data (MEDIUM — Florida coastal context)
17. USGS NHD hydrography / water bodies (MEDIUM — water maps)
18. USDA NRCS SSURGO soils (MEDIUM — land use/agriculture)

---

5.3 CAVEATS AND FLAGS — TRANSPORTATION/INFRASTRUCTURE/BROADBAND/
ENVIRONMENT/CLIMATE

- Volusia County Open Data portal (ArcGIS Hub) is the go-to local GIS
  source — start there. The ArcGIS REST API enables programmatic access.
  Equator is a convenient third-party mirror but the authoritative source
  is Volusia County's own portal.
- FCC Broadband Map has known accuracy controversies (over/under-reporting).
  It's the best public federal source but treat with caution. Use ACS
  broadband questions (tract-level household self-report) for triangulation.
  The FCC map is provider-reported availability; ACS is household-reported
  access — different concepts.
- FEMA flood maps are the regulatory baseline but have limitations (don't
  capture all risk, future sea level rise, local flooding nuances). FEMA
  maps are being modernized. Use NFHL GIS data for programmatic work. First
  Street Flood Factor is a supplement (private nonprofit, model-based) — use
  as supplement, not replacement.
- NOAA sea level rise and climate data are the federal standard; Florida has
  state-level coastal/climate data that complements. Volusia is coastal
  (Atlantic) — sea level rise and coastal flood are high-priority topics.
- NLCD is 30m raster — good for county analysis but not parcel-level. Use
  with county parcel/land use data for detail. NLCD impervious surface and
  tree canopy are particularly useful layers.
- USGS 3DEP LiDAR is high-resolution elevation — check Volusia County
  coverage and availability on USGS National Map. LiDAR is large data;
  processing required.
- FDOT traffic data is the Florida source for road traffic; Volusia County
  may have additional county road data. FDOT covers state roads primarily.
- VOTRAN ridership data availability — check VOTRAN reports and the Open
  Data portal for transit GIS layers (routes, stops).
- EPA EJSCREEN is a screening tool (indicative); use for initial EJ analysis,
  not definitive EJ determination.
- FEMA disaster declarations (OpenFEMA) give the historical resilience
  record (hurricanes, etc.) for Volusia.
- Florida water management districts: Volusia County is in the St. Johns
  River Water Management District (SJRWMD) — confirm and use SJRWMD data
  for local water resources.
- GIS data formats: Volusia County Open Data uses ArcGIS REST (GeoJSON,
  JSON, PBF), shapefiles, etc. Plan for ArcGIS REST API or download.
  Equator offers convenience downloads (LiDAR, parcels, contours, building
  footprints, DEMs).
- Environmental data overlaps with real estate (flood zones affect property
  values) and government (permitting/environmental permits) — note cross-
  domain use.

---

6. DOMAIN 6 — GOVERNMENT, PUBLIC FINANCE, BUDGETING, TAXES, PERMITTING,
OPEN GOVERNMENT, ELECTIONS, POLITICAL

---

6.1 SOURCE LIST

### Volusia County — Annual Comprehensive Financial Report (ACFR) /
Comprehensive Annual Financial Report (CAFR)
- **Publisher:** Volusia County (volusia.org/services/finance)
- **What it provides:** Volusia County's annual financial report — government
 -wide and fund financial statements, budget, revenues (property tax, sales
  tax, tourist development tax, etc.), expenditures by department/function,
  debt, assets, etc. The primary source for county government finance.
- **Volusia coverage:** DIRECT — Volusia County government finance.
- **Access method:** Volusia County website (volusia.org/services/finance/
  financial-and-administrative-services/finance-department) — ACFR/CAFR
  reports (PDFs). Public.
- **Update frequency:** Annual (after fiscal year end).
- **License/terms:** Public record (Florida).
- **Friction:** LOW-MEDIUM. ACFR is typically a PDF report — readable but
  not machine-readable (may need to parse tables). Some counties publish
  machine-readable financial data; check if Volusia does. The ACFR is the
  authoritative source.
- **Priority:** HIGH
- **Why:** The definitive source for Volusia County government finances —
  revenues, spending, debt, budget. Essential for the government finance
  section of reports, industry mover intelligence (county financial health),
  and the "how does the county spend money" question.
- **Notes:** ACFR is typically PDF. Check if Volusia has machine-readable
  financial data (some counties do via open data portals or CFO initiatives).
  If not, parsing the PDF is the path. Volusia County's ACFR is the primary
  source; the FL DOR and Census gov-finances (below) are complementary
  aggregates.

### Volusia County — Open Data Portal (finance / budget data if available)
- **Publisher:** Volusia County (Open Data portal / ArcGIS Hub)
- **What it provides:** (See Domain 5) — Volusia County Open Data portal may
  have budget/finance datasets in addition to GIS data. Some counties put
  checkbook/transparency data on open data portals.
- **Volusia coverage:** DIRECT (if available).
- **Access method:** Check opendata-volusiacountyfl.hub.arcgis.com for finance/
  budget datasets.
- **Priority:** MEDIUM (depends on what's posted)
- **Notes:** Verify if Volusia County Open Data portal has financial/
  budget/checkbook data. If yes, that's machine-readable and preferred.

### Florida Department of Financial Services (DFS) — Local Government
Finance / Data
- **Publisher:** Florida Department of Financial Services (myfloridacfo.com)
- **What it provides:** Florida local government financial data — some data
  on local government finances, including county-level data. Florida DFS
  division of accounting and financial reporting.
- **Volusia coverage:** DIRECT — Volusia County (as part of Florida local
  government data).
- **Access method:** Florida DFS website (myfloridacfo.com/division/aa).
  Public.
- **Priority:** MEDIUM
- **Notes:** Florida DFS may have local government financial data that
  complements the ACFR. Check what's available.

### U.S. Census Bureau — Annual Survey of State and Local Government
Finances
- **Publisher:** U.S. Census Bureau
- **What it provides:** State and local government finance data — revenues,
  expenditures, debt, employment, by state, county, and local government
  (for governments above a certain size). County-level government finance
  data (revenues by source, expenditures by function, debt, etc.).
- **Volusia coverage:** DIRECT — Volusia County government finance (Census
  gov-finances includes Volusia County).
- **Access method:** Census Bureau API, data.census.gov, Census FTP. Public.
- **Update frequency:** Annual survey (with lag; ~2-3 year lag — e.g. 2022
  data released 2024/2025). Biennial in some years.
- **License/terms:** Public domain.
- **Friction:** LOW. API and web UI.
- **Priority:** MEDIUM
- **Why:** Standardized county government finance data (revenues by source,
  expenditures by function, debt) — useful for comparing Volusia to peer
  counties and tracking government finance trends. Complements the ACFR
  (which is Volusia-specific and more detailed). The Census gov-finances
  gives cross-county comparability.
- **Notes:** Census gov-finances has a lag and covers governments above a
  certain size (Volusia qualifies). Use for cross-county comparison and
  trends. The ACFR is more current and detailed for Volusia specifically.

### Volusia County — Budget (adopted budget)
- **Publisher:** Volusia County (volusia.org/services/finance)
- **What it provides:** Volusia County adopted budget — department budgets,
  revenue estimates, budget documents. Annual.
- **Volusia coverage:** DIRECT.
- **Access method:** Volusia County website (budget documents, PDFs). Public.
- **Friction:** LOW-MEDIUM (PDF budget documents).
- **Priority:** HIGH
- **Why:** The adopted budget is the planned spending/revenue for the county
  — more current than the ACFR (which is actuals after the fact). Useful for
  understanding county priorities and planned spending. The budget document
  is public.
- **Notes:** Budget documents are typically PDFs. Combine with ACFR for
  actuals vs. budget comparison.

### Volusia County — Tourist Development Tax / Convention Development Tax
(already covered in Domain 3; this line notes the government finance aspect)
- **Publisher:** Volusia County Tax Collector / Revenue Services (volusia.org/
  revenue-services/tourist-and-convention-development-tax)
- **What it provides:** Tourist Development Tax (bed tax) administration and
  receipts — a local option tax on short-term accommodations. Receipts by
  taxing district. This is both a tourism indicator (Domain 3) and a
  government revenue line (here).
- **Volusia coverage:** DIRECT — Volusia County taxing districts (Halifax
  District, etc.).
- **Access method:** Volusia County website, Tax Collector, public records.
  Public.
- **Priority:** MEDIUM-HIGH (revenue line + tourism indicator)
- **Notes:** Cross-domain: tourism indicator (Domain 3) and government
  revenue (here). Tourist development tax is a significant Volusia revenue
  source (funded the CVB, etc.). Receipts are a proxy for short-term lodging
  activity.

### Volusia County — Property Tax / Millage Rates / Tax Collector
- **Publisher:** Volusia County Tax Collector (volusia.org/tax-collector)
- **What it provides:** Property tax data — millage rates by taxing authority
  (county, cities, school board, special districts), property tax collections,
  tax roll data. Property tax is a major local revenue source and a resident
  cost.
- **Volusia coverage:** DIRECT — Volusia County and all taxing authorities
  within the county.
- **Access method:** Volusia County Tax Collector website, tax data, public
  records. Public.
- **Update frequency:** Annual (tax year).
- **License/terms:** Public record (Florida).
- **Priority:** MEDIUM-HIGH
- **Why:** Property tax rates and collections are important for residents
  (cost) and for government finance (revenue). Millage rates by jurisdiction
  allow comparison. Useful for the resident well-being report (tax burden)
  and government finance analysis.
- **Notes:** Property tax millage rates and collections are public. The
  Tax Collector administers. For parcel-level assessment detail, VCPA is
  the source (Domain 2). For aggregate tax stats, FL DOR (Domain 2) and
  Tax Collector data are sources.

### Florida Department of Revenue — Taxes / Local Government Tax Data
- **Publisher:** Florida DOR (fldor.org)
- **What it provides:** Florida tax data — sales tax collections by county,
  tourist development tax data, local government tax data, property tax data
  (aggregate). Florida DOR publishes tax collection reports by county.
- **Volusia coverage:** DIRECT — Volusia County tax collections.
- **Access method:** Florida DOR website, reports, data. Public.
- **Priority:** MEDIUM
- **Notes:** Florida DOR tax data is a state-level aggregate source for
  county tax collections. Use for cross-county tax comparison. Covered
  partly in Domain 2 (sales tax as economic indicator) and Domain 3 (tourist
  tax).

### Volusia County — Building Permits / Permit Center / Zoning (already
covered in Domain 2; this line notes government/process aspect)
- **Publisher:** Volusia County Growth and Resource Management / Permit
  Center (volusia.org/services/growth-and-resource-management/building-and-
  zoning/permit-and-zoning-center)
- **What it provides:** Building permits, zoning, land use permitting —
  permitting process and data. Permitting velocity, backlog, process. This
  is both a real estate/development data source (Domain 2) and a government
  process/transparency item (here).
- **Volusia coverage:** DIRECT.
- **Access method:** Permit Center online, public records, some GIS data
  (zoning on Open Data portal). Public.
- **Priority:** HIGH (process/transparency aspect)
- **Why:** Permitting velocity and process are key industry mover concerns
  ("how fast can I get a permit?"). The Permit Center is the government-
  facing side. Permitting data (volume, timelines, backlog) is a government
  performance indicator. Public records and the Permit Center are the access
  points. Zoning/land use GIS on the Open Data portal.
- **Notes:** Permitting data access (bulk) may be limited — the Permit Center
  is interactive. Census BPS is the easy public aggregate for building permit
  counts. County permit data (address-level, status, timelines) may require
  interaction or public records request. This is a key industry mover
  indicator and a government transparency item.

### Volusia County — Procurement / Purchasing / Contracts
- **Publisher:** Volusia County Purchasing / Procurement (volusia.org/services/
  financial-and-administrative-services/purchasing)
- **What it provides:** County procurement/contracting data — vendor contracts,
  purchases, bids,Request for Proposals (RFPs), awarded contracts. "Doing
  Business with Volusia County" information.
- **Volusia coverage:** DIRECT.
- **Access method:** Volusia County Purchasing website, bid/contract listings,
  public records. Public.
- **Update frequency:** Ongoing (bids/RFPs posted, contracts awarded).
- **License/terms:** Public record (Florida).
- **Priority:** MEDIUM-HIGH
- **Why:** Procurement/contracting transparency — who gets county contracts,
  what's being purchased, vendor spend. Useful for transparency, business
  opportunities (vendors), and the industry mover/business angle (county
  contracting opportunities). Public record.
- **Notes:** Volusia County Purchasing website has bid/RFP listings and
  contract info. Bulk contract data (spend by vendor) may or may not be
  easily downloadable — check. Public records requests can get more. "Doing
  Business with Volusia County" page is the vendor entry point.

### Volusia County — Open Government / Transparency / Checkbook
- **Publisher:** Volusia County
- **What it provides:** County open government / transparency data — checkbook
  (if any), open data portal (ArcGIS Hub — GIS data), public records, meeting
  agendas/minutes (County Council meetings), public records request process.
- **Volusia coverage:** DIRECT.
- **Access method:** Volusia County website, Open Data portal, County Council
  agendas/minutes (volusia.org), public records requests. Florida public
  records law (broad public access).
- **Update frequency:** Ongoing (meetings, records).
- **License/terms:** Public record (Florida law — broad public records access).
- **Priority:** MEDIUM
- **Why:** Open government / transparency is part of the charter (open by
  default). Volusia County's open data portal (GIS) is strong; financial
  transparency (checkbook) may be limited. County Council meetings/agendas/
  minutes are public. The public records request process is available for
  non-public data. Useful for the open government analysis.
- **Notes:** Florida has strong public records laws — most county records are
  public. Volusia County's open data portal is GIS-focused (strong). Check if
  there's a financial transparency/checkbook portal (some counties have them;
  if Volusia doesn't, that's a gap/opportunity). County Council meetings,
  agendas, minutes are public (volusia.org). The ACFR and budget are public
  financial documents.

### Volusia County — Supervisor of Elections / Election data
- **Publisher:** Volusia County Supervisor of Elections (volusia.org/elections
  or similar)
- **What it provides:** Election data — voter registration, election results
  (by precinct), voter turnout, elected officials, districts. Volusia County
  election results and voter data.
- **Volusia coverage:** DIRECT — Volusia County elections.
- **Access method:** Volusia County Supervisor of Elections website, election
  results, voter registration data (some public), Florida Division of
  Elections (state-level). Public.
- **Update frequency:** Elections (periodic); voter registration ongoing.
- **License/terms:** Public record (Florida).
- **Priority:** MEDIUM
- **Why:** Election data — voter turnout, election results by precinct,
  elected officials, districts (commission districts, school board, etc.).
  Useful for the civic engagement analysis, political context, and maps
  (commission districts, voting patterns). Florida election data is public.
- **Notes:** Volusia County Supervisor of Elections is the local source.
  Florida Division of Elections (dos.myflorida.com/elections) has state
  data. Precinct-level results are public. Voter registration data has some
  public components (registration by party, etc.) but not all (privacy
  protections). Commission district boundaries are on the GIS portal (see
  Map catalog — commission districts layer).

### Volusia County — Commission Districts / Council Districts (GIS)
- **Publisher:** Volusia County (GIS / redistricting data)
- **What it provides:** Volusia County Council/Commission district boundaries
  (GIS layer on Open Data portal — "Commission Districts" in Map catalog).
  Used for political representation analysis and equity analysis (which
  areas are in which district).
- **Volusia coverage:** DIRECT.
- **Access method:** Volusia County Open Data portal (ArcGIS Hub) — Commission
  Districts layer. Public.
- **Priority:** MEDIUM
- **Notes:** Commission district GIS layer is on the Open Data portal (see
  Map catalog). Useful for political/equity maps.

### Florida Division of Elections / State election data
- **Publisher:** Florida Department of State / Division of Elections
  (dos.myflorida.com/elections)
- **What it provides:** Florida election data — state-level election results,
  voter registration statistics, election administration data.
- **Volusia coverage:** Via state — Florida election data includes Volusia
  County results (statewide data includes county breakdowns).
- **Access method:** Florida Division of Elections website, results, data.
  Public.
- **Priority:** MEDIUM
- **Notes:** Florida Division of Elections has state election data and some
  county breakdowns. Local (Volusia Supervisor of Elections) is more detailed
  for Volusia.

### Florida public records / transparency resources
- **Publisher:** Florida (various — Florida's Government in the Sunshine;
  Florida open government laws)
- **What it provides:** Florida's broad public records laws — most government
  records are public. Florida has a strong public records framework. This
  enables access to Volusia County records (contracts, emails, reports, etc.)
  via public records requests.
- **Volusia coverage:** DIRECT (Florida law applies to Volusia County).
- **Access method:** Public records requests to Volusia County departments.
  Florida Public Records Law.
- **Priority:** MEDIUM (as a mechanism, not a specific dataset)
- **Notes:** Florida's public records laws are a powerful access mechanism.
  If a specific dataset isn't publicly downloadable, a public records request
  may get it (may have fees). This is a tool for accessing Volusia County
  government data beyond published datasets.

### Federal — USAspending / BDM (federal funds to local governments)
- **Publisher:** U.S. Treasury (USAspending.gov) / federal agencies
- **What it provides:** Federal spending data — federal contracts, grants,
  loans, by recipient (including local governments, businesses in Volusia).
  USAspending.gov has federal spending data searchable by location (county).
- **Volusia coverage:** DIRECT — federal spending in Volusia County (federal
  contracts/grants to Volusia County government, businesses, institutions).
- **Access method:** USAspending.gov — searchable by county/location, API.
  Public.
- **Update frequency:** Periodic (data updated).
- **License/terms:** Public (U.S. government).
- **Priority:** MEDIUM
- **Why:** Federal spending in Volusia County — federal grants to the county,
  federal contracts to local businesses, federal funding flows. Useful for
  the industry mover/economic analysis (federal investment in Volusia) and
  government finance (federal grants to county). USAspending is the public
  federal spending database.
- **Notes:** USAspending.gov can be searched by county (Volusia). Useful for
  tracking federal funds to Volusia County government, businesses (e.g.
  Embry-Riddle federal grants?, local contractors), and institutions. Not
  all federal spending is captured perfectly, but it's the public database.

### Volusia County municipalities — city budget/finance/permits/open data
- **Publisher:** Individual cities (Daytona Beach, DeLand, New Smyrna Beach,
  Ormond Beach, Port Orange, Deltona, South Daytona, etc.)
- **What it provides:** City-level budget, finance, permits, open data (where
  available). Each city has its own government finance and permitting.
- **Volusia coverage:** City-specific.
- **Access method:** City websites, city budgets (PDFs), city permit systems,
  city open data (some cities have open data portals; varies). Public.
- **Friction:** MEDIUM (varies by city; some have good data, others less).
- **Priority:** MEDIUM
- **Why:** Cities are important Volusia governments — they have their own
  budgets, taxes, permitting, and services. For a full government picture,
  need city-level data. City budgets, property tax rates, permits, etc.
- **Notes:** Daytona Beach, DeLand, New Smyrna Beach, Ormond Beach, Port
  Orange, Deltona are the major cities. Check each for budget/finance/open
  data availability. City budgets are typically PDFs. City permitting (e.g.
  Daytona Beach permit data) may be interactive. City open data varies.

### Local economic development / business resources (Volusia County Economic
Development, chambers)
- **Publisher:** Volusia County Economic Development (volusiabusinessresources
  .com or volusia.org economic development), Daytona Regional Chamber of
  Commerce, local chambers.
- **What it provides:** Economic development information — business resources,
  incentives, site selection, economic development data, business climate.
  The Daytona Regional Chamber compiles economic development info. Volusia
  County Economic Development provides business support info.
- **Volusia coverage:** DIRECT.
- **Access method:** Website, reports, contacts. Public.
- **Priority:** MEDIUM
- **Notes:** Economic development offices are stakeholder partners (industry
  movers). They have local business/economic development data and context.
  The Chamber may have economic data. These are useful stakeholder contacts
  and sources of local economic development context.

### Public safety / emergency management government data (Volusia County
Emergency Management, fire, etc.) — overlaps Domain 4/5
- **Publisher:** Volusia County Emergency Management, fire rescue, etc.
- **What it provides:** Emergency management data, hurricane evacuation zones
  (see Domain 5 — evacuation zones are in the Map catalog and Domain 5), fire
  rescue data, some public safety government data.
- **Volusia coverage:** DIRECT.
- **Priority:** MEDIUM (overlapping with Domain 4/5)
- **Notes:** Evacuation zones are in Domain 5 (environment/climate/disaster).
  Emergency management public data is part government, part environment/
  safety. Covered in Domain 5 for evacuation zones and flood.

### 기타 local government data (tax collector, property appraiser, clerk of
court, etc.)
- **Tax Collector:** property tax, vehicle registration, etc. (public).
- **Property Appraiser:** property data (Domain 2).
- **Clerk of Court:** court records, official records (public — volusia clerk
  / clerk.org). 
- **These are covered in respective domains.** The Volusia County Clerk of
  Court (clerk.org) has official records, court records (public). Property
  Appraiser (Domain 2). Tax Collector (this domain — property tax, vehicle).

---

6.2 TOP PICKS FOR PROJECT VOLUSIA — GOVERNMENT/FINANCE/PERMITS/OPEN GOV

1. Volusia County ACFR (annual financial report) — county finance, revenues,
   spending, debt (HIGH — definitive county finance source)
2. Volusia County adopted budget — planned spending/revenue (HIGH — current
   county priorities)
3. Volusia County Open Data portal (ArcGIS Hub) — GIS + any finance/budget
   datasets (HIGH — local open data)
4. Volusia County Permit Center / Growth & Resource Management — permitting
   process, zoning, land use (HIGH — permitting velocity, transparency)
5. Volusia County Tourist Development Tax receipts — local revenue + tourism
   indicator (MEDIUM-HIGH — cross-domain)
6. Volusia County property tax / millage rates / Tax Collector — tax burden,
   revenue (MEDIUM-HIGH — resident cost + revenue)
7. Volusia County Purchasing/procurement — contracts, vendors, transparency
   (MEDIUM-HIGH — business opportunities + transparency)
8. U.S. Census gov-finances — standardized county finance for cross-county
   comparison (MEDIUM — comparable county finance)
9. Florida DOR tax data — county tax collections, sales tax, tourist tax
   (MEDIUM — state aggregate tax data)
10. Volusia County Supervisor of Elections — election results, voter data,
    districts (MEDIUM — civic/political)
11. Volusia County Commission Districts GIS (Open Data portal) — political
    representation maps (MEDIUM — political/equity)
12. USAspending.gov — federal spending in Volusia County (MEDIUM — federal
    funds flow)
13. Volusia County County Council meetings/agendas/minutes — open government
    (MEDIUM — transparency)
14. Florida public records requests — access mechanism for non-public county
    data (MEDIUM — access tool)
15. City-level budget/finance/permits (Daytona Beach, DeLand, etc.) — city
    governments (MEDIUM — incremental to county)
16. Volusia County Economic Development / Chamber — local economic development
    context (MEDIUM — stakeholder partners)
17. Florida DFS local government finance data (MEDIUM — state local gov finance)
18. Volusia County Clerk of Court / official records (MEDIUM — public records)

---

6.3 CAVEATS AND FLAGS — GOVERNMENT/FINANCE/PERMITS/OPEN GOV

- Volusia County ACFR is the definitive finance source but is typically a
  PDF — parsing may be needed for machine-readable use. Check if Volusia
  has machine-readable financial data (some counties do; if not, that's a
  gap/opportunity for the open data portal).
- The Volusia County Open Data portal (ArcGIS Hub) is strong on GIS data;
  financial transparency (checkbook) may be limited. Verify what financial/
  budget data is on the portal.
- Permitting data: the Permit Center is interactive; bulk permit data may not
  be trivially downloadable. Census BPS is the easy public aggregate for
  building permit counts. For address-level permit detail, timelines, and
  backlog, may need interaction or public records request. This is a key
  industry mover indicator and a transparency item — investigate early.
- Tourist development tax receipts: public record but may be in reports or
  require request; the CVB may have them (cross-domain with Domain 3).
- Property tax: millage rates and collections are public; for parcel-level
  assessment detail, VCPA is the source (Domain 2). For aggregate, Tax
  Collector and FL DOR.
- Procurement/contracts: the Purchasing website has bid/RFP listings; bulk
  contract spend data may require request. Public records can get more.
- Elections: voter registration data has public components (party, etc.) but
  privacy protections apply (no individual voter lists publicly without
  restrictions). Precinct-level election results are public. Commission
  district boundaries are on the GIS portal.
- Florida public records law is a powerful access mechanism — if a dataset
  isn't publicly downloadable, a public records request may get it (may have
  fees). Plan for this where needed.
- City-level data varies by city — some have good open data, others less.
  Check each major city (Daytona Beach, DeLand, New Smyrna Beach, Ormond
  Beach, Port Orange, Deltona) for budget/permit/open data availability.
- Federal spending (USAspending) is a useful but imperfect view of federal
  funds to Volusia — not all federal spending is captured, and recipient
  location data can be imprecise. Use as indicative.
- Government finance overlaps with economic (tax receipts as economic
  indicators) and real estate (property tax/assessment) — note cross-domain
  use.

---

7. CROSS-DOMAIN NOTES AND OVERLAPS

- Tourism economic impact (Domain 3) uses economic multipliers (Domain 1
  caveats) — published reports are public; models are not.
- STR data (Domain 3) is economic data too (hotel performance is part of the
  economy) — the primary owner is tourism, but economic analysis uses it.
- Property tax / assessment (Domain 2) is also government finance (Domain 6)
  — VCPA is the property source; Tax Collector/FL DOR are the government
  finance sources.
- Building permits (Domain 2 via Census BPS; local via Permit Center) are
  also government process/transparency (Domain 6) — Census BPS is the easy
  public aggregate; the Permit Center is the local process source.
- Broadband (Domain 5) is also a digital equity/resident issue (Domain 4
  resident well-being) — FCC map + ACS broadband data.
- Flood zones (Domain 5) affect real estate values (Domain 2) and insurance
  (economic) — cross-domain.
- Crime data (Domain 4) and public safety locations (Domain 5 Map catalog —
  public safety locations) are related — crime stats (FDLE/FBI/Volusia SO)
  and public safety facility locations (sheriff, fire, EMS) are different
  datasets.
- Evacuation zones (Domain 5) are also emergency management government data
  (Domain 6) — the Map catalog has evacuation zones as a map layer.
- CDC PLACES health data (Domain 4) uses BRFSS (health survey) — BRFSS
  direct county data is sparse; PLACES is the tract-level model-based
  product.

---

8. ACCESS PRIORITY FRAMEWORK FOR Q4 2026

For the baseline data portal and Q4 deliverables, prioritize sources that
are:
  - Public (no subscription)
  - Machine-readable (API, CSV, GIS, downloadable)
  - Cover Volusia County directly at useful geography (county, tract, ZIP)
  - Updated with reasonable frequency
  - Low friction (no complex auth, no manual request required for first cut)

Tier A (start here for baseline portal):
  - BLS LAUS (API/flat files, monthly, county) — unemployment
  - BEA LAPI/GDP (API, annual, county) — income, output
  - Census ACS (API, 5-year, tract/county) — demographic/economic detail
  - Zillow ZHVI/ZORI (free CSVs, monthly, county/ZIP/city) — home values,
    rents
  - Volusia County Open Data portal (GIS, various) — local spatial data
  - CDC PLACES (API/download, tract) — health
  - FDOT traffic data (download/GIS, annual) — transportation
  - FCC Broadband Map (interactive + bulk, address/block) — broadband
  - FEMA NFHL (GIS, flood zones) — flood risk
  - FL DOH CHARTS (portal, county) — Florida health
  - FL DOE school report cards (portal, school) — education

Tier B (add as capacity allows):
  - BLS QCEW (flat files, quarterly, county/industry) — industry structure
  - Census CBP/NES (API, annual, county/ZIP) — business counts
  - Volusia County Property Appraiser (Access DB + GIS, weekly/annual,
    parcel) — parcel data
  - NPS visitor stats (CSV, monthly/annual, Canaveral NS) — recreation
  - BTS TranStats (portal, monthly, airport) — airport passengers
  - CVB reports (PDFs, periodic, Volusia) — tourism market research
  - Volusia County ACFR/budget (PDF, annual) — government finance
  - Census TIGER/Line (shapefile/GeoJSON, annual) — boundaries
  - USGS NLCD (GeoTIFF, periodic, county) — land cover
  - NOAA climate/sea level (various, station/coast) — climate

Tier C (gated/partnership/further effort):
  - STR hotel data (Visit Florida partner route; or CVB reports) — hotel
    performance
  - Inside Airbnb (verify coverage for Volusia; if yes, free public STR data)
  - Commercial STR summaries (AirDNA/AirROI/Airbtics public summaries —
    free top-line, gated detail)
  - Volusia County Permit Center address-level permit data (interactive/
    request)
  - Procurement/contract spend data (portal/listings; bulk may need request)
  - Higher-resolution local data via Florida public records requests

---

9. GAPS AND FOLLOW-UP ACTIONS

- VERIFY Inside Airbnb coverage for Volusia County / Daytona Beach
  (insideairbnb.com/get-the-data) — this is a key STR data gap. If covered,
  it's a high-priority free public STR source. If not, plan for the Visit
  Florida STR partner route or rely on CVB reports + commercial summaries.
- VERIFY Visit Florida Marketing Partner eligibility and process for STR
  report access (visitflorida.org/resources/research/str-reports; contact
  research@visitflorida.org) — if feasible, this unlocks monthly STR data
  for the Daytona Beach market.
- ESTABLISH CONTACT with Volusia County CVB research team (daytonabeach.com/
  about/market-research; research@daytonabeach.com or equivalent) — the CVB
  is the primary local tourism source; early contact may unlock data beyond
  public PDFs.
- VERIFY Volusia County Open Data portal finance/budget/checkbook data
  availability (opendata-volusiacountyfl.hub.arcgis.com) — see if county
  financial data is machine-readable on the portal.
- VERIFY Volusia County Permit Center bulk data access (volusia.org permit
  center; public records) — determine if address-level permit data (timelines,
  backlog) is accessible programmatically or only interactively.
- VERIFY Florida DEO / CareerSource Volusia/Flagler workforce data availability
  — local workforce development board may have job seeker/employer data.
- VERIFY Volusia County Supervisor of Elections data availability (voter
  registration public components, precinct results).
- VERIFY USGS 3DEP LiDAR coverage for Volusia County (USGS National Map/
  Earth Explorer) — for detailed elevation/flood analysis.
- VERIFY city-level open data availability for major Volusia cities (Daytona
  Beach, DeLand, New Smyrna Beach, Ormond Beach, Port Orange, Deltona) —
  city budgets, permits, open data portals.
- VERIFY FL DOH CHARTS account requirement for some data (flhealthcharts.gov
  — "Create your CHARTS account to instantly view your county's data").

---

10. DOCUMENT CONTROL

- This document is the consolidated public data source recon for Project
  Volusia. It should be reviewed and updated as sources are verified,
  accessed, and as new sources are identified.
- Owner: Project Volusia Data Team (per DATA_CATALOG.md)
- Related: DATA_CATALOG.md, TOOLS_CATALOG.md, Q4_2026_EXECUTION_PLAN.md,
  MISSION_STATEMENT.md, OPEN_INTELLIGENCE_DATA_DRIVEN_CHARTER.md
- Next review: 2026-12-02 (aligned with charter review cadence)
- Status: Initial recon complete (2026-09-02). Access verification actions
  in Section 9 are outstanding.

---

End of document.
