# Project Volusia — Repository Connection Guide

> How the ZQM-Computing/volusia-portal repository works — frontend and backend in one repo.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    ZQM-Computing/volusia-portal                   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Frontend (React/Vite/TypeScript)                         │  │
│  │  - Static JSON data files in data/*.json                  │  │
│  │  - Built to dist/ via `npm run build`                     │  │
│  │  - Deployed to GitHub Pages → volusia.zqmlabs.com         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Backend (FastAPI/Python 3.11)                            │  │
│  │  - Runs on port 8000 (internal, not exposed to internet)  │  │
│  │  - HTML dashboard: /                                      │  │
│  │  - JSON API: /api/*                                       │  │
│  │  - SQLite database: data/volusia.db                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  nginx (port 80, exposed)                                 │  │
│  │  - Serves frontend static files                           │  │
│  │  - Proxies /api/* to backend port 8000                    │  │
│  │  - 13 security headers (HSTS, CSP, Permissions-Policy)    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Cloudflared Tunnel (optional)                            │  │
│  │  - volusia.zqmlabs.com → localhost:80                     │  │
│  │  - Exposes the portal to the internet                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

### Frontend
- **Language**: TypeScript (React, Vite, Tailwind, Nivo, Leaflet)
- **Source**: `src/` — React components, hooks, pages
- **Build**: `npm run build` → `dist/`
- **Data**: `data/*.json` — static JSON data files served by nginx
- **Deployment**: GitHub Pages → https://volusia.zqmlabs.com

### Backend
- **Language**: Python 3.11 (FastAPI, SQLite)
- **Source**: `backend/` — FastAPI app, routes, gamification
- **Port**: 8000 (internal only, fronted by nginx)
- **Database**: `data/volusia.db` — SQLite, gitignored
- **Data pipeline**: `scripts/refresh_v2.py` — fetches, validates, seeds
- **API**: `/api/indicators`, `/api/health`, `/api/datasets`, etc.

### Infrastructure
- **Docker**: `docker-compose.yml` + `Dockerfile` (frontend) + `backend/Dockerfile.backend`
- **nginx**: `nginx/nginx.conf` — reverse proxy + static files + security headers
- **CI/CD**: `.github/workflows/ci.yml` — 5-job pipeline

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     Data Sources                                 │
│  Census │ BLS │ BEA │ NOAA │ C2ER │ Volusia County CVB         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              scripts/refresh_v2.py                               │
│              (Fetches, validates, seeds SQLite + JSON cache)    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              SQLite Database (data/volusia.db)                   │
│              123 indicators, 14 categories, 6 CVB hotel records       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ├─────────────────────────────────────┐
                              ▼                                     ▼
┌─────────────────────────────────────┐ ┌─────────────────────────────────────┐
│  Backend API (port 8000)            │ │  JSON Export (data/*.json)         │
│  /api/indicators                    │ │  - indicators.json                 │
│  /api/health                        │ │  - economic.json                   │
│  /api/datasets                      │ │  - demographics.json               │
│  /api/diagnostics                   │ │  - climate.json                    │
│  /api/cvb_hotels                    │ │  - cvb-hotels.json                 │
│                                     │ │  - map-layers.json                 │
└─────────────────────────────────────┘ └─────────────────────────────────────┘
                              │                                     │
                              ▼                                     ▼
┌─────────────────────────────────────┐ ┌─────────────────────────────────────┐
│  nginx (port 80)                    │ │  GitHub Pages                       │
│  - Serves frontend static files     │ │  - Built frontend (dist/)          │
│  - Proxies /api/* to :8000          │ │  - Static JSON data files           │
│  - volusia.zqmlabs.com              │ │  - volusia.zqmlabs.com              │
└─────────────────────────────────────┘ └─────────────────────────────────────┘
```

---

## Local Development

### Prerequisites
- Docker and Docker Compose
- Node.js 20+
- Python 3.11+
- Git

### Start the full stack
```bash
cd volusia-portal
docker compose up -d
```

### Verify
```bash
# Backend health
curl http://localhost:8000/health

# Frontend (served by nginx)
curl http://localhost:8080

# APIs (proxied through nginx)
curl http://localhost:8080/api/indicators | head
```

### Frontend-only development
```bash
cd volusia-portal
npm install
npm run dev        # Vite dev server on :5173
```

### Backend-only development
```bash
cd volusia-portal/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### TypeScript compilation check
```bash
npx tsc --noEmit
```

### Run tests
```bash
pytest tests/ -v        # Backend: 7 tests
npx tsc --noEmit        # Frontend: type check
npm run build           # Frontend: build verification
```

---

## Data Refresh

```bash
# Refresh the database and regenerate JSON cache files
cd volusia-portal
python scripts/refresh_v2.py
```

This:
1. Creates/upgrades the SQLite schema
2. Seeds 130 indicators across 14 categories
3. Seeds 6 CVB hotel records
4. Writes 14 JSON cache files for frontend hooks

---

## Deployment

```bash
git checkout gh-pages  # or main, depending on your setup
npm run build
# Deploy dist/ to GitHub Pages
```

Or use the automated GitHub Actions workflow: push to `master` and the CI/CD pipeline builds and deploys.

---

## Environment Variables

| Variable | Purpose | Location |
|----------|---------|----------|
| `VOLUSIA_DB_PATH` | Path to SQLite database | Backend |
| `VOLUSIA_PORT` | Portal port (default: 8000) | Backend |
| `VOLUSIA_HOST` | Portal host (default: 0.0.0.0) | Backend |
| `CENSUS_API_KEY` | Census API key (optional) | Backend |
| `BLS_API_KEY` | BLS API key (optional) | Backend |
| `BEA_API_KEY` | BEA API key (optional) | Backend |
| `NOAA_API_KEY` | NOAA API key (optional) | Backend |
| `C2ER_API_KEY` | C2ER API key (optional) | Backend |

See `.env.example` for the template.

---

## Deployment URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | https://volusia.zqmlabs.com | Static React portal (GitHub Pages) |
| Backend API | https://volusia.zqmlabs.com/api | JSON API (nginx proxy) |
| Backend Portal | http://localhost:8000 | Direct (development only) |
| GitHub Repo | https://github.com/ZQM-Computing/volusia-portal | This repo |

---

## Debug endpoints

| Endpoint | What it returns |
|----------|-----------------|
| `/api/diagnostics` | Full system check: DB counts, file inventory, npm/python versions |
| `/api/health` | Health check + indicator count |
| `/api/indicators.csv` | Download all indicators as CSV |

---

## Troubleshooting

### Frontend shows no data
1. Check if `data/*.json` files exist in the repo
2. Run `python scripts/refresh_v2.py` to regenerate
3. Rebuild and redeploy frontend

### Backend API not responding
1. Check if FastAPI is running: `curl http://localhost:8000/health`
2. Check Docker: `docker compose ps`
3. Check logs: `docker compose logs backend`

### Data not updating
1. Run `python scripts/refresh_v2.py` manually
2. Check `audit_log` table in SQLite
3. Verify API keys are set (if required)

### TypeScript errors
1. Run `npx tsc --noEmit` to see errors
2. Fix type issues in `src/` files
3. Check `src/hooks/useApi.ts` for API URL issues

---

**Last Updated**: 2026-09-09
**Maintainer**: ZQM Computing
