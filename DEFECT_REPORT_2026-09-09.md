# zqmlabs.com / volusia-portal — Defect Assessment Report

**Date:** 2026-09-09  
**Auditor:** ZQM Computing automated audit  
**Scope:** zqmlabs.com live site, ZQM-Computing/volusia-portal repo, ZQM-Labs GitHub orgs, Docker infrastructure

---

## Summary

**21 open issues** on ZQM-Computing/volusia-portal.  
**0 open issues** on all ZQM-Labs repos.

Issues were found through two scans:
- **First scan** identified 5 untracked defects → opened as **#71-#75**
- **Second scan** identified 6 more untracked defects → opened as **#76-#81**
- **Pre-existing** 12 open issues (#57, #65-#70) + 5 Dependabot dependency bumps

---

## All Open Issues on ZQM-Computing/volusia-portal

| Issue # | Title | Severity | Status |
|---------|-------|----------|--------|
| #71 | /api/ route prefix mismatch — all frontend API calls 404 | **P0 CRITICAL** | OPEN |
| #72 | /pulse.json and /news.json return 404 | P1 | OPEN |
| #73 | /gamification/missions and /gamification/pulse return 404 | P2 | OPEN |
| #74 | Indicator count mismatch — API serves 28, site claims 48 | P1 | OPEN |
| #75 | Backend Docker container marked unhealthy | P2 | OPEN |
| #76 | POST /refresh returns returncode:2 but indicators unchanged | P1 | OPEN |
| #77 | All 10 datasets have empty content fields | P1 | OPEN |
| #78 | No /cvb_hotels API endpoint | P2 | OPEN |
| #79 | GET /refresh endpoint mislabeled — says Diagnostics | P2 | OPEN |
| #80 | Docker health check shows unhealthy despite /health OK | P3 | OPEN |
| #81 | POST /refresh with empty body returns 200 — no auth | P2 | OPEN |
| #57 | Backend indicator coverage: 27 of 53, missing tourism/housing/education/safety | P2 | OPEN |
| #65 | API Surface Improvements — Search, Bulk, Export, Stats, Keys | enhancement | OPEN |
| #66 | API Endpoint Tracking — Full Surface Audit | documentation | OPEN |
| #67 | API Keys Required — 17 Indicators Need Data Sources | bug | OPEN |
| #68 | Maintenance Notes — MAINTENANCE.md Improved | documentation | OPEN |
| #69 | Page Map — zqmlabs.com Navigation Guide | documentation | OPEN |
| #70 | Contributor Submission System | feature | OPEN |
| #1-#5 | Dependabot dependency bumps (nivo, postcss, react-dom, tailwindcss) | deps | OPEN |

---

## Newly Filed Issues (#71-#81)

### #71 — P0 CRITICAL: /api/ route prefix mismatch
**Problem:** Frontend JS bundle calls `/api/indicators`, `/api/map-layers`, `/api/datasets`, `/api/indicators.csv` but backend FastAPI routes are mounted at `/indicators`, `/map-layers`, `/datasets`, `/indicators.csv` without the `/api/` prefix. All 4 API calls return 404.

**Evidence:** Docker logs show `GET /api/indicators → 404`, `GET /api/map-layers → 404`, `GET /api/datasets → 404`, `GET /api/indicators.csv → 404`

**Root cause of maps crash:** The `/maps` page JS error `b.filter is not a function` is caused by the API returning 404 → React state receives null → `b` is not an array → `.filter()` fails.

**Fix:** Either add `/api/` prefix to backend routes, or remove `/api/` prefix from frontend fetch calls.

---

### #72 — P1: /pulse.json and /news.json return 404
**Problem:** Frontend references `/pulse.json` and `/news.json` but backend has no corresponding endpoints. Docker logs confirm both return 404.

**Fix:** Add endpoints or remove frontend references.

---

### #73 — P2: /gamification/missions and /gamification/pulse return 404
**Problem:** Gamification system references `/gamification/missions` and `/gamification/pulse` but backend has no endpoints. `/gamification/leaderboard` returns 200 but only 244 bytes.

**Fix:** Add endpoints or remove frontend references.

---

### #74 — P1: Indicator count mismatch — API serves 28, site claims 48
**Problem:** Backend `/health` reports `indicator_count: 28`. `/indicators` returns 28 indicators. But frontend `/data` page references 48 indicator IDs. 20 indicators are missing from the database.

**Impact:** Education, environment, government, housing, and safety categories have null/placeholder data.

**Fix:** Populate remaining 20 indicators or update frontend to reflect actual coverage.

---

### #75 — P2: Backend Docker container marked unhealthy
**Problem:** `docker ps` shows `volusia-portal-backend-1` as `Up 2 days (unhealthy)` despite `/health` returning `{"status":"healthy","db_exists":true,"indicator_count":28}`.

**Fix:** Update Docker HEALTHCHECK to match the actual /health response format.

---

### #76 — P1: POST /refresh returns {status:'triggered', returncode:2} but indicators unchanged
**Problem:** POST /refresh returns `{"status":"triggered","returncode":2}` but the indicator `fetched_at` timestamps do not change after the call. The refresh pipeline is not actually updating any data.

**Evidence:**  
- POST /refresh `{}` → `{"status":"triggered","returncode":2}`  
- After calling POST /refresh, indicator `fetched_at` values remain unchanged
- `refresh_script.py` line 22 calls `subprocess.run([python, "-m", "volusia_data.refresh_v2"])` which returns code 2

**Fix:** Check `refresh_v2.py` for the error causing returncode 2. The refresh pipeline is broken.

---

### #77 — P1: All 10 datasets have empty content fields
**Problem:** GET /datasets returns 10 datasets but every dataset has `content: ""`. Users download datasets but get no actual data.

**Evidence:** `{"count":10,"datasets":[{"id":10,"content":""},...]` — all 10 have empty content.

**Fix:** Populate the content field or update the dataset loading pipeline.

---

### #78 — P2: No /cvb_hotels API endpoint
**Problem:** The `cvb_hotels` table exists in the database (confirmed by diagnostics) but has no API endpoint. CVB hotel data (ADR: $147.35, RevPAR: $124.73) is inaccessible via API.

**Fix:** Add GET /cvb_hotels endpoint to serve hotel data.

---

### #79 — P2: GET /refresh endpoint mislabeled
**Problem:** OpenAPI spec has `GET /refresh` with summary "Diagnostics" (operationId: `diagnostics_refresh_get`). But `GET /diagnostics` already exists and does the same thing. The route naming is confusing. Also, `GET /refresh` is documented as returning "refresh data" but actually returns diagnostics.

**Fix:** Rename GET /refresh to GET /diagnostics or remove it to match the existing endpoint.

---

### #80 — P3: Docker health check shows 'unhealthy' despite /health returning {status:'ok'}
**Problem:** `docker ps` shows `volusia-portal-backend-1` as `Up 2 days (unhealthy)` but `GET /health` returns `{"status":"healthy","db_exists":true,"indicator_count":28}`.

**Root Cause:** The Dockerfile HEALTHCHECK likely expects `{"status":"ok"}` but the endpoint returns `{"status":"healthy"}`.

**Fix:** Update Dockerfile HEALTHCHECK to match the actual /health response format.

---

### #81 — P2: POST /refresh with empty body returns 200 — no auth, no input validation
**Problem:** POST /refresh accepts empty request bodies and returns 200. No authentication, no input validation. The endpoint is exposed on 0.0.0.0:8000 (all interfaces).

**Evidence:** `POST /refresh {}` → 200, `POST /refresh` (empty) → 200.

**Fix:** Add authentication to POST /refresh.

---

## Backend API — Complete Endpoint Inventory

### Working Endpoints (17 documented)
| Method | Path | Returns |
|--------|------|---------|
| GET | / | Service info |
| GET | /health | Health status |
| GET | /indicators | 28 indicators |
| GET | /indicators/{name} | Single indicator |
| GET | /indicators.csv | CSV export |
| GET | /datasets | 10 datasets (all empty content) |
| GET | /map-layers | 18 layers with geometry |
| GET | /diagnostics | Full system diagnostics |
| GET | /refresh | Diagnostics (misnamed) |
| POST | /refresh | Trigger refresh (returncode:2) |
| GET | /status | Source/indicator status |
| GET | /meta | Indicator metadata |
| GET | /verify | Hash verification |
| GET | /unemployment | Unemployment data |
| GET | /unemployment/rate | Rate data |
| GET | /docs/page | Docs HTML |
| GET | /gamification/leaderboard | 244 bytes |
| GET | /gamification/stats/{user_id} | Stats |
| GET | /gamification/achievements/{user_id} | Achievements |
| GET | /gamification/history/{user_id} | History |
| POST | /gamification/visit/{user_id} | Visit |
| POST | /gamification/xp/{user_id} | Add XP |

### 404 Endpoints (frontend references but no backend route)
- `/api/*` (all variants)
- `/pulse.json`
- `/news.json`
- `/gamification/missions`
- `/gamification/pulse`
- `/cvb_hotels`

---

## Infrastructure Status

| Container | Status | Ports | Notes |
|-----------|--------|-------|-------|
| volusia-portal-backend | **unhealthy** | 8000 | Serving but health check fails |
| volusia-portal-frontend | Up | 8080 | Making /api/ calls that 404 |
| ollama | Up | 11434 | |
| anythingllm | Up (healthy) | 3001 | |
| open-webui | Up (healthy) | 3080 | |
| n8n | Up | 5678-5679 | |
| zqm-quantum-api | Up | 8891 | |

---

## GitHub Orgs Summary

### ZQM-Computing (joined 2026-07-05)
- 2 repos: `volusia-portal` (21 open issues), `.github`
- All ZQM-Computing issues are on volusia-portal

### ZQM-Labs (joined 2026-07-12)
- 9 repos: attestation-toolkit, awesome-windows-attestation, pqc-readiness-toolkit, zqm-shield, zqm-security-policy, zqm-public-tools, zqm-attestation-briefs, project-volusia, ZQM-Labs umbrella, .github
- **All repos have 0 open issues** — fully resolved

---

## Critical Path (priority order)

1. **Fix #71** — /api/ route mismatch is the root cause of the maps crash and most data display issues
2. **Fix #76** — Refresh pipeline is broken (returncode 2), data cannot be updated
3. **Fix #74/#77** — 20 missing indicators + 10 empty datasets — data completeness
4. **Fix #72/#73** — Missing endpoints break content and gamification
5. **Fix #78** — cvb_hotels data exists but has no API
6. **Fix #81** — No auth on refresh endpoint — security risk
7. **Fix #75/#80** — Docker health check mismatch
8. **Fix #82** — info@zqmlabs.com email is non-functional; replace with zqmcomputing@gmail.com

---

## Report File
Saved to: `C:\Users\zqmco\AppData\Local\Temp\zqmlabs_defect_report.md`
