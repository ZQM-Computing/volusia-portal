# Project Volusia — Maintenance Guide

> Operational runbook for maintaining the Project Volusia portal on ZQM-NODE-4.
> Updated 2026-09-08.

---

## Quick Reference

| Task | Command |
|------|---------|
| Start backend | `taskkill /F /IM python3.exe && cd C:\Users\zqmco\Docker\volusia-portal\backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000` |
| Start frontend | `cd C:\Users\zqmco\Docker\volusia-portal && npm run dev` |
| Build frontend | `cd C:\Users\zqmco\Docker\volusia-portal && npm run build` |
| Verify build | `cd C:\Users\zqmco\Docker\volusia-portal && npx tsc --noEmit && npm run build` |
| Restart backend | `taskkill /F /IM python3.exe && sleep 1 && python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --working-directory C:\Users\zqmco\Docker\volusia-portal\backend` |
| Refresh data | `cd C:\Users\zqmco\Docker\volusia-portal && python scripts/refresh_v2.py` |
| Check backend health | `curl http://localhost:8000/health` |
| Check live site | `curl -sL http://zqmlabs.com/ | grep -c "div id=\"root\""` |
| Verify content | `curl -sL http://zqmlabs.com/ | grep -o "I am a\|Community Pillars\|Top Missions\|Data Domains" \| head -5` |
| Sync dist to nginx | `cp C:\Users\zqmco\Docker\volusia-portal\dist\index.html C:\Users\zqmco\scoop\persist\nginx\html\index.html && cp C:\Users\zqmco\Docker\volusia-portal\dist\assets\*.js C:\Users\zqmco\scoop\persist\nginx\html\assets\ && cp C:\Users\zqmco\Docker\volusia-portal\dist\assets\*.css C:\Users\zqmco\scoop\persist\nginx\html\assets\` |
| Start cloudflared | `nssm start cloudflared` (Admin) |

---

## Directory Structure

|| Path | Purpose |
||------|---------|
|| `C:\Users\zqmco\Docker\volusia-portal\` | Docker app source (React frontend + FastAPI backend) |
|| `C:\Users\zqmco\Docker\volusia-portal\dist\` | Built frontend output (Vite) |
|| `C:\Users\zqmco\Docker\volusia-portal\src\pages\` | React page components |
|| `C:\Users\zqmco\Docker\volusia-portal\src\hooks\` | API hooks (useApi.ts) |
|| `C:\Users\zqmco\Docker\volusia-portal\backend\` | FastAPI backend source |
|| `C:\Users\zqmco\Docker\volusia-portal\backend\gamification\` | Gamification engine (scoring.py, routes.py, gamification.py) |
|| `C:\Users\zqmco\Docker\volusia-portal\scripts\` | Pipeline scripts (refresh_v2.py) |
|| `C:\Users\zqmco\Docker\volusia-portal\data\` | SQLite DB + cache files + audit logs |
|| `C:\Users\zqmco\scoop\persist\nginx\html\` | **Live site root** — served by nginx :80 → zqmlabs.com |
|| `C:\Users\zqmco\Docker\volusia-portal\public\` | Public static files |
|| `C:\Users\zqmco\project-volusia-web\` | Static site generator (NOT the live React app) |
|| `C:\Users\zqmco\Docker\volusia-portal\docker-compose.yml` | Docker Compose config |
|| `C:\Users\zqmco\Docker\volusia-portal\nginx\` | nginx config |

---

## Architecture

```
zqmlabs.com :443 → cloudflared → nginx :80 → index.html + assets/*.js → React SPA
                                              ↓
                                     /api/* → backend:8000 (FastAPI)
                                     /data/* → static assets or backend
```

**Key insight**: The live site serves `index.html` from `C:\Users\zqmco\scoop\persist\nginx\html\`. The React SPA loads from `assets/index-ByC5g7hj.js`. After `npm run build`, both must be synced.

---

## Build & Deploy Workflow

### 1. Make Changes
Edit source files under `C:\Users\zqmco\Docker\volusia-portal\src\` or `backend\`.

### 2. Verify Build
```bash
cd C:\Users\zqmco\Docker\volusia-portal
npx tsc --noEmit          # must pass with 0 errors
npm run build             # outputs to dist/
```

### 3. Sync to Live Site
The nginx volume serves from `C:\Users\zqmco\scoop\persist\nginx\html\`.
```bash
# Sync the built index.html
cp C:\Users\zqmco\Docker\volusia-portal\dist\index.html C:\Users\zqmco\scoop\persist\nginx\html\index.html

# Sync the JS and CSS chunks (new build produces new hashes)
cp C:\Users\zqmco\Docker\volusia-portal\dist\assets\*.js C:\Users\zqmco\scoop\persist\nginx\html\assets\
cp C:\Users\zqmco\Docker\volusia-portal\dist\assets\*.css C:\Users\zqmco\scoop\persist\nginx\html\assets\
```

### 4. Verify Live Site
```bash
# Check div id="root" present (SPA shell)
curl -sL http://zqmlabs.com/ | grep -c "div id=\"root\""

# Check the content is present in the JS chunk
curl -sL http://zqmlabs.com/ | grep -o "I am a\|Community Pillars\|Top Missions\|Data Domains" | head -5

# Check the JS chunk loads
curl -sL http://zqmlabs.com/assets/index-ByC5g7hj.js | grep -o "I am a" | head -1
```

### 5. Restart Backend (if backend code changed)
```bash
taskkill /F /IM python3.exe
sleep 1
cd C:\Users\zqmco\Docker\volusia-portal\backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --working-directory C:\Users\zqmco\Docker\volusia-portal\backend
```

---

## Common Issues

### Stale Frontend on Live Site
**Symptom**: Changes visible locally but not on zqmlabs.com.
**Cause**: nginx volume (`C:\Users\zqmco\scoop\persist\nginx\html\`) is stale.
**Fix**: Run the "Sync to Live Site" commands above. Verify with `curl -sL http://zqmlabs.com/ | grep -o "I am a|Community Pillars|Top Missions|Data Domains"`.

### Stale JS Chunk (Cached Assets)
**Symptom**: `index.html` references `index-OLDHASH.js` but only `index-NEWHASH.js` exists.
**Cause**: Browser caches hashed assets with `immutable` cache-control.
**Fix**: The HTML `src` attribute always matches the current build. After syncing, if a user sees old content, hard-refresh (Ctrl+Shift+R).

### Backend Returns 404 for New Endpoints
**Symptom**: `/api/categories`, `/api/business`, etc. return 404.
**Cause**: Stale uvicorn process running old code.
**Fix**: `taskkill /F /IM python3.exe` then restart uvicorn.

### Stale Frontend on Live Site
**Symptom**: No "I am a", "Community Pillars", "Top Missions", "Data Domains" on zqmlabs.com.
**Cause**: nginx volume not synced with latest `npm run build`.
**Fix**: Sync dist to nginx volume and verify with `curl -sL http://zqmlabs.com/ | grep -o "I am a|Community Pillars|Top Missions|Data Domains"`.

### New API Endpoints Return 404
**Symptom**: `/api/indicators/search`, `/api/indicators/bulk`, `/api/indicators/stats`, `/api/export/json`, `/api/keys`, `/api/datasets/refresh` return 404.
**Cause**: Backend (NSSM service) needs restart to load new code.
**Fix**: `nssm restart VolusiaGamification` (requires Admin).

### Indicators Show Null/None Values
**Symptom**: 17 indicators have null values.
**Cause**: Missing API keys for data sources (BLS/BEA/FBI UCR/FL DOE/FDOT/FWS).
**Fix**: Set API keys as environment variables, run pipeline, restart backend. See issue #67.

### Stale Data Values
**Symptom**: `per_capita_income_acs` shows -888888888, `hotel_occupancy_pct` shows "None".
**Cause**: Placeholder values from API not filtered.
**Fix**: Data validation added to `refresh_v2.py` — run pipeline to clean.

---

## API Endpoints (FastAPI :8000)

### Core Endpoints
| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check + indicator count |
| `GET /indicators` | All indicators (filter by category, limit) |
| `GET /indicators/{name}` | Single indicator |
| `GET /indicators.csv` | Download all as CSV |
| `GET /datasets` | Latest datasets |
| `GET /categories` | All categories |
| `GET /map-layers` | Map layers |

### Analytics
| Endpoint | Description |
|----------|-------------|
| `GET /analytics/summary` | Summary stats by category |
| `GET /analytics/trends/{name}` | Historical trend data |
| `GET /analytics/comparison/{name}` | Cross-category comparison |
| `GET /analytics/dashboard` | Comprehensive dashboard |

### Self-Service
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/contribute` | POST | Submit data contribution |
| `/api/contributor` | GET | Contributor profile/stats |
| `/api/webhook` | POST | Webhook receiver |
| `/api/fetch-status` | GET | Pipeline cache status |

### Search & Export
| Endpoint | Description |
|----------|-------------|
| `GET /api/indicators/search?q=` | Search indicators by name/description |
| `GET /api/indicators/bulk?names=` | Bulk fetch by comma-separated names |
| `GET /api/indicators/stats` | Indicator statistics |
| `GET /api/export/json` | Export as JSON |
| `GET /api/export/csv` | Export as CSV |

### Gamification
| Endpoint | Description |
|----------|-------------|
| `GET /gamification/missions` | Mission catalog |
| `GET /gamification/leaderboard` | Leaderboard |
| `GET /gamification/state/{id}` | Contributor state |
| `GET /pulse` | Indicator pulse |

### Admin
| Endpoint | Description |
|----------|-------------|
| `POST /refresh?secret={token}` | Trigger pipeline refresh |
| `GET /diagnostics?secret={token}` | Full system diagnostics |
| `GET /api/keys` | API key status |
| `GET /api/datasets/refresh?source=` | Dataset refresh |

---

## Gamification System

**Source of truth**: `C:\Users\zqmco\Docker\volusia-portal\backend\gamification\scoring.py`

- **58 missions** across 5 tiers (Entry → Legend)
- **14 pathways** (A-N) including code/infra, civic, environmental, health, research, governance
- **Backend**: `/gamification/missions`, `/gamification/leaderboard`, `/gamification/state/{id}`
- **Frontend hooks**: `useMissions()`, `useGamification()` in `src/hooks/useApi.ts`
- **Mission feed on homepage**: Top 5 available missions shown on HomePage

---

## Homepage Structure (HomePage.tsx)

Current layout (verified 2026-09-08):

| Section | Content |
|---------|---------|
| Hero | Search bar + CTA buttons |
| Core Constituencies | 4 stat cards (Business, Residents, Tourists, Leaders) with live API data |
| "I am a..." | Horizontal scroll of 10 personas |
| Top Missions | 5 missions from `/gamification/missions` API |
| Charts | Income Trend + Employment & Unemployment |
| Climate Summary | Avg Max Temp, Total Precipitation, Avg Min Temp |
| Data Domains | 10 domain cards with search filter |
| Community Pillars | 4 expandable umbrellas |
| Map Preview | County Boundary, Beach Access, Water Bodies |
| Data Sources | Census, BLS, BEA |
| Human README | Getting started + features |
| AI Agent README | API endpoints + data schema |

---

## Maintenance Checklist

### Build & Deploy
- [ ] `npx tsc --noEmit` passes with 0 errors
- [ ] `npm run build` succeeds
- [ ] `npm run preview` returns HTTP 200
- [ ] Dist synced to `C:\Users\zqmco\scoop\persist\nginx\html\`
- [ ] Live site verified: `curl -sL http://zqmlabs.com/ | grep -o "I am a|Community Pillars|Top Missions|Data Domains" | head -5`

### Backend & Data
- [ ] Backend running on :8000 (NSSM service `VolusiaGamification`)
- [ ] Pipeline ran successfully: `python scripts/refresh_v2.py`
- [ ] Cache files current (`data/cache/`)
- [ ] No stale Python processes
- [ ] DB indicators count: 48 (check `curl http://localhost:8000/health`)

### API Endpoints
- [ ] `/health` returns healthy
- [ ] `/indicators` returns 48 indicators
- [ ] `/api/contributor` works
- [ ] `/api/contribute` works
- [ ] `/api/webhook` works
- [ ] `/api/fetch-status` works
- [ ] `/api/indicators/search` works
- [ ] `/api/indicators/bulk` works
- [ ] `/api/indicators/stats` works
- [ ] `/api/export/json` works
- [ ] `/api/export/csv` works
- [ ] `/api/keys` works
- [ ] `/api/datasets/refresh` works

### Infrastructure
- [ ] Cloudflared tunnel running (`nssm start cloudflared`)
- [ ] nginx serving live site (`curl -sL http://zqmlabs.com/ | head -5`)
- [ ] No stale JS/CSS assets in `C:\Users\zqmco\scoop\persist\nginx\html\assets\`

---

## Key Files

| File | Description |
|------|-------------|
| `MAINTENANCE.md` | This file — operational runbook |
| `PROJECT_TRACKING.md` | Project status, milestones, issues, change log |
| `PROJECT_OUTLINE.md` | Maintenance/growth/contribution plan |
| `PROJECT_VOLUSIA_GOV.md` | Governance framework |
| `DEPLOY.md` | Deployment guide (Docker compose + native) |
| `ARCHITECTURE.md` | System architecture and data flow |
| `API.md` | API documentation |
| `README.md` | Project overview |
| `SECURITY.md` | Security hardening notes |

---

*Last updated: 2026-09-08*
*Owner: Alex Zelenski (zqmco)*
*Board: [GitHub Projects #7](https://github.com/users/ZQM-Computing/projects/7)*
