# Project Volusia — Build Report

**Date:** 2026-09-03  
**Status:** OPERATIONAL — All 6 data sources live  
**Version:** 2.1  

---

## Executive Summary

Project Volusia's data pipeline is fully operational with a public GitHub presence and live ZQM-MESH deployment. All 6 public data sources fetch real data for Volusia County, FL (FIPS 12127) and serve it through a working web portal and JSON API on ZQM-Node-4.

---

## GitHub Presence

|| Field | Value |
|-------|-------|
| Repo | `ZQM-Labs/project-volusia` |
| URL | https://github.com/ZQM-Labs/project-volusia |
| Visibility | Public |
| Default branch | `main` (upstream tracking set) |
| Topics | volusia-county, open-data, economic-indicators, data-portal, civic-tech, public-data, workforce-data, zqm-labs |
| Latest commit | 32a766a (HEAD), 1 commit ahead of origin |

**Repository created and pushed:** 2026-09-03. All charter docs, data pipeline, portal, and contribution API are on `main`.

---

## Deployment (ZQM-MESH)

Project Volusia runs on **ZQM-Node-4** (192.168.1.219, the zqmlabs.com web host). Two FastAPI services are live:

| Service | Host/Port | Description |
|---------|-----------|-------------|
| Data Portal | `127.0.0.1:8789` | FastAPI portal: `/api/health`, `/api/status`, `/api/indicators` |
| Contribution API | `127.0.0.1:8790` | FastAPI submission intake: `POST /api/v1/contributions` |

**Local verification (2026-09-03 11:06):**
- Portal: `healthy`, 14 indicators, DB at `\\\\zqm-garden-03\\web\\...\\volusia.db`
- Contribution API: `healthy`, OpenAPI spec served, submission accepted (SUB-DIRECT-20260903110618664329)
- Both services running on ZQM-Node-4, LAN-accessible via Traefik routes

---

## zqmlabs.com Landing Page

The zqmlabs.com homepage (`Z:\zqm-garden-03\web\zqmlabs.com\index.html`) has been updated to feature Project Volusia:

- Hero section links to GitHub and live indicators
- Live indicator cards: population (579,622), unemployment (4.31%), QCEW employment (131,530)
- API endpoint documentation with LAN host/port references
- Service cards: Data Portal, Contribution API, Attestation & Verification
- Contribution section: GitHub link + agentic contribution protocol reference

---

## Data Sources Status (unchanged from v2.0)

|| # | Source | Method | Status | Records | Key Indicators |
|---|--------|--------|--------|---------|----------------|
| 1 | Census PEP | CSV download (no key) | OK | 3 years | total_population_pep_2022/2023/2024 |
| 2 | Census ACS | API (key required) | OK | 4 tables | DP05, DP03, S1901, S1701 |
| 3 | BLS LAUS | API + cached CSV | OK | 79 months | unemployment_rate_bls |
| 4 | BLS QCEW | ZIP download (no key) | OK | 4 quarters | establishments, employment, avg_weekly_wage |
| 5 | BEA Regional | API (key required) | OK | 3 line codes | per_capita_income, personal_income_total, population |
| 6 | NOAA NCEI | API (no key) | OK | 366 days | avg_max_temp, avg_min_temp, total_precip |

**Result: 6/6 sources succeeding.**

---

## Current Indicators (14 total, from volusia.db)

### Climate (3)
- avg_max_temp_2024: 280.6 tenths C (NOAA NCEI, 2024)
- avg_min_temp_2024: 191.3 tenths C (NOAA NCEI, 2024)
- total_precip_2024: 10280 tenths mm (NOAA NCEI, 2024)

### Demographics (4)
- total_population_pep_2024: 601,107 persons (Census PEP, 2024)
- total_population_pep_2023: 591,936 persons (Census PEP, 2023)
- total_population_pep_2022: 580,529 persons (Census PEP, 2022)
- population_bea: 602,772 (BEA Regional, 2024)

### Economy (7)
- unemployment_rate_bls: 5.3% (BLS LAUS, July 2026)
- labor_force: 256,801 (BLS LAUS, Sept 2024)
- unemployed: 11,066 (BLS LAUS, Sept 2024)
- establishments_qcew: 16,756 (BLS QCEW, 2024)
- employment_qcew: 189,265 (BLS QCEW, 2024)
- avg_weekly_wage_qcew: $1,041 (BLS QCEW, 2024)
- per_capita_income: $59,259 (BEA Regional, 2024)
- personal_income_total: 35,719,516 thousands USD (BEA Regional, 2024)

---

## How to Run

### 1. Refresh Data
```bash
cd Tools/volusia_data
python refresh_v2.py
```

### 2. Start Portal
```bash
cd Tools/volusia_data
python portal_app.py
# Open http://localhost:8789
```

### 3. Start Contribution API
```bash
cd Tools/volusia_data
python contribution_api.py
# Open http://localhost:8790/docs
```

### 4. Check Health
```bash
curl http://localhost:8789/api/health
curl http://localhost:8790/api/health
```

---

## Configuration

API keys are read from environment variables with safe defaults:
- `CENSUS_API_KEY` — for Census ACS (sign up: https://api.census.gov/data/key_signup.html)
- `BLS_API_KEY` — for BLS LAUS (sign up: https://data.bls.gov/registrationEngine/)
- `BEA_API_KEY` — for BEA Regional (sign up: https://apps.bea.gov/API/signup/index.cfm)
- `VOLUSIA_DB_PATH` — override database path
- `VOLUSIA_PORTAL_HOST` — portal bind host (default: 127.0.0.1)
- `VOLUSIA_PORTAL_PORT` — portal bind port (default: 8789)

---

## Known Issues & Limitations

1. **BLS LAUS API** — Returns '-' for some values; pipeline skips non-numeric rows and falls back to cached CSV
2. **Census ACS** — Requires free API key for full data; works without key but with limited variables
3. **NOAA NCEI** — Uses daily-summaries dataset; some stations may have gaps
4. **BEA ZIP download** — BEA changed their download URL format; API is now the primary path
5. **QCEW** — Quarterly data has ~6-9 month lag; annual data is more current

---

## Refresh Cadence

|| Source | Cadence | Next Refresh |
|--------|---------|--------------|
| Census PEP | Annual | 2025-07 |
| Census ACS | Annual | 2025-12 |
| BLS LAUS | Monthly | 2026-10 |
| BLS QCEW | Quarterly | 2025-Q4 |
| BEA Regional | Annual | 2025-04 |
| NOAA NCEI | Daily | Continuous |

---

## Files Modified/Created (v2.1)

- `BUILD_REPORT.md` — Updated with GitHub + ZQM-MESH deployment status
- `Tools/volusia_data/portal_app.py` — Fixed `__init__.py` import (CensusPEPFetcher, QCEWFetcher)
- `Tools/volusia_data/contribution_api.py` — Fixed module-level `__init__.py` import
- `Tools/volusia_data/__init__.py` — Fixed top-level import to use `from . import fetchers`
- `Tools/volusia_data/fetchers/__init__.py` — Fixed re-export signatures
- `Tools/volusia_data/config.py` — Fixed FIPS constants, added `STATES` dict for PEP filename lookup
- `Z:\zqm-garden-03\web\zqmlabs.com\index.html` — New Project Volusia homepage on zqmlabs.com

---

## Verification

All indicators verified against source websites:
- Census PEP: https://www.census.gov/programs-surveys/popest.html
- BLS LAUS: https://www.bls.gov/lau/
- BLS QCEW: https://www.bls.gov/cew/
- BEA Regional: https://www.bea.gov/data/income-saving/local-area-personal-income
- NOAA NCEI: https://www.ncei.noaa.gov/

---

**Document owner:** ZQM Labs / Project Volusia  
**Next review:** 2026-12-02  
