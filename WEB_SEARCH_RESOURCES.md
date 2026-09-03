# Project Volusia — Web Search Tool Resources

> Free and low-cost search/web tools that don't require Firecrawl.
> Tested 2026-09-02 for Hermes Agent integration.

---

## 1. CURRENTLY WORKING (No API Key Required)

### 1.1 DDGS (DuckDuckGo Search) — ✅ ACTIVE
- **Library:** `ddgs` (Python)
- **Install:** `pip install ddgs`
- **Usage:** `from ddgs import DDGS; DDGS().text("query", max_results=5)`
- **Limits:** None (rate-limited by DDG, but generous)
- **Config:** `web.backend: ddgs` in `~/.hermes/config.yaml`
- **Status:** Currently active in Hermes config

### 1.2 Open-Meteo Weather API — ✅ WORKING
- **URL:** `https://api.open-meteo.com/v1/forecast?latitude=29.21&longitude=-81.02&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America%2FNew_York`
- **Limits:** None (free, no key)
- **Data:** Temperature, precipitation, wind, humidity
- **Status:** Verified working for Daytona Beach (29.21°N, 81.02°W)

### 1.3 DuckDuckGo Instant Answer API — ✅ WORKING
- **URL:** `https://api.duckduckgo.com/?q=query&format=json&no_html=1`
- **Limits:** None
- **Data:** Abstract, related topics, definitions
- **Status:** Verified working

### 1.4 NOAA NCEI Weather Data — ✅ WORKING
- **URL:** `https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=TMAX,TMIN,PRCP&stations=USW00012838&startDate=YYYY-MM-DD&endDate=YYYY-MM-DD&format=json`
- **Limits:** None
- **Data:** Historical daily weather
- **Status:** Verified working

### 1.5 Census data.census.gov — ✅ WORKING
- **URL:** `https://data.census.gov/api/access/data/table?g=0500000US12127&tid=ACSDP5Y2023.DP03`
- **Limits:** None
- **Data:** ACS economic, demographic, housing
- **Status:** Verified working

---

## 2. FREE WITH API KEY (Register Once)

### 2.1 Brave Search API
- **URL:** `https://api.search.brave.com/res/v1/web/search`
- **Free tier:** 2,000 queries/month
- **Signup:** https://brave.com/search/api/
- **Header:** `X-Subscription-Token: YOUR_KEY`
- **Status:** Not yet registered

### 2.2 FRED API (St. Louis Fed)
- **URL:** `https://api.stlouisfed.org/fred/series/observations?series_id=FLVOLU7POP&api_key=YOUR_KEY&file_type=json`
- **Free tier:** Unlimited
- **Signup:** https://fred.stlouisfed.org/docs/api/api_key.html
- **Data:** Economic time series (population, unemployment, GDP, etc.)
- **Status:** Not yet registered

### 2.3 Census API
- **URL:** `https://api.census.gov/data/2024/acs/acs5/profile?get=DP03_0062E&for=county:127&in=state:12&key=YOUR_KEY`
- **Free tier:** Unlimited
- **Signup:** https://api.census.gov/data/key_signup.html
- **Data:** All ACS tables programmatically
- **Status:** Not yet registered

### 2.4 BLS API
- **URL:** `https://api.bls.gov/publicAPI/v2/timeseries/data/`
- **Free tier:** 500 queries/day (with key)
- **Signup:** https://data.bls.gov/registrationEngine/
- **Data:** Employment, wages, unemployment
- **Status:** Not yet registered

### 2.5 BEA API
- **URL:** `https://apps.bea.gov/api/data/?UserID=YOUR_KEY&method=GetData&datasetname=Regional&TableName=CAINC1&LineCode=10&GeoFIPS=12127&Year=ALL&ResultFormat=JSON`
- **Free tier:** Unlimited
- **Signup:** https://apps.bea.gov/api/signup/
- **Data:** Personal income, GDP by county
- **Status:** Not yet registered

### 2.6 Google Custom Search
- **URL:** `https://www.googleapis.com/customsearch/v1?key=YOUR_KEY&cx=SEARCH_ENGINE_ID&q=query`
- **Free tier:** 100 queries/day
- **Signup:** https://developers.google.com/custom-search/v1/overview
- **Status:** Not yet registered

---

## 3. SELF-HOSTED OPTIONS

### 3.1 SearXNG
- **Type:** Metasearch engine (aggregates Google, Bing, DuckDuckGo, etc.)
- **Install:** Docker Compose
- **Free:** Yes (self-hosted)
- **Limits:** None
- **Status:** Not yet deployed

**Docker Compose:**
```yaml
version: '3'
services:
  searxng:
    image: searxng/searxng:latest
    ports:
      - "8080:8080"
    environment:
      - INSTANCE_NAME=volusia-search
    volumes:
      - searxng-data:/etc/searxng
    restart: unless-stopped

volumes:
  searxng-data:
```

**Hermes config after setup:**
```yaml
web:
  backend: searxng
  searxng_url: http://localhost:8080
```

### 3.2 Crawl4AI
- **Type:** AI-powered web scraper
- **Install:** `pip install crawl4ai`
- **Free:** Yes (open source)
- **Status:** Not yet installed

---

## 4. PAID OPTIONS (For Reference)

| Service | Free Tier | Paid | Notes |
|---------|-----------|------|-------|
| Firecrawl | Keyless (limited) | $49+/mo | Primary recommendation |
| Serper.dev | 2,500 queries | $49+/mo | Google search API |
| SearchApi.io | 100 searches | $49+/mo | Multi-engine |
| Newsdata.io | 200 req/day | $24+/mo | News-focused |
| Scrape.do | None | $29+/mo | Proxy-based |

---

## 5. RECOMMENDED SETUP FOR PROJECT VOLUSIA

### Immediate (No Cost)
1. ✅ **DDGS** — Already active, no key needed
2. ✅ **Open-Meteo** — Weather data, no key needed
3. ✅ **NOAA NCEI** — Historical weather, no key needed
4. ✅ **Census data.census.gov** — Economic/demographic data

### Register for Free Keys (5 minutes each)
5. **Brave Search API** — 2,000 queries/month
6. **FRED API** — Unlimited economic data
7. **Census API** — Full ACS programmatic access
8. **BLS API** — Employment/wages data
9. **BEA API** — Personal income data

### Self-Hosted (Optional)
10. **SearXNG** — Full metasearch engine on Docker

---

## 6. HERMES CONFIGURATION

Current active config:
```yaml
web:
  backend: ddgs
  use_gateway: false
```

To add SearXNG later:
```yaml
web:
  backend: searxng
  searxng_url: http://localhost:8080
```

To add Brave Search:
```yaml
web:
  backend: brave-free
```

---

Document owner: Project Volusia Leadership
Related: RECON_REPORT_V2.md, DATA_CATALOG.md
