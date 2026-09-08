# Project Volusia — Repository Connection Guide

> How ZQM-Labs/project-volusia and ZQM-Computing/volusia-portal work together.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        ZQM-Node-4                                │
│                    (192.168.1.219)                               │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ZQM-Labs/project-volusia (Backend)                       │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  FastAPI Portal (:8789)                             │  │  │
│  │  │  - HTML dashboard                                   │  │  │
│  │  │  - JSON API endpoints                               │  │  │
│  │  │  - SQLite database                                  │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  FastAPI API (:8790)                                │  │  │
│  │  │  - /api/indicators                                  │  │  │
│  │  │  - /api/health                                      │  │  │
│  │  │  - /api/datasets                                    │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Cloudflared Tunnel                                      │  │
│  │  - volusia.zqmlabs.com → localhost:80                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Pages                                 │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ZQM-Computing/volusia-portal (Frontend)                  │  │
│  │  - React/TypeScript portal                                │  │
│  │  - Static JSON data files                                 │  │
│  │  - Deployed to gh-pages branch                            │  │
│  │  - URL: https://volusia.zqmlabs.com                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Repository Roles

### ZQM-Labs/project-volusia (Backend + Data)
- **Purpose**: Data pipeline, backend API, data storage
- **Language**: Python (FastAPI, SQLite)
- **Location**: `\ZQM-GARDEN-03\web\14_Projects\Active\Project-Volusia\`
- **Key Components**:
  - `Tools/volusia_data/portal_app.py` — FastAPI portal (port 8789)
  - `Tools/volusia_data/refresh_v2.py` — Data refresh pipeline
  - `Tools/volusia_data/volusia.db` — SQLite database
  - `Data/` — Data files and cache
- **Deployment**: Runs on ZQM-Node-4 (192.168.1.219)
- **Ports**:
  - 8789: HTML portal
  - 8790: JSON API

### ZQM-Computing/volusia-portal (Frontend)
- **Purpose**: Public-facing web portal
- **Language**: TypeScript (React, Vite, Tailwind)
- **Repository**: https://github.com/ZQM-Computing/volusia-portal
- **Key Components**:
  - `src/` — React frontend source
  - `data/` — Static JSON data exports
  - `backend/` — FastAPI backend (alternative deployment)
  - `dist/` — Built frontend (deployed to GitHub Pages)
- **Deployment**: GitHub Pages → https://volusia.zqmlabs.com
- **CI/CD**: GitHub Actions (`.github/workflows/deploy.yml`)

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
│              ZQM-Labs/project-volusia                            │
│              Tools/volusia_data/refresh_v2.py                    │
│              (Fetches, validates, stores in SQLite)              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              SQLite Database (volusia.db)                         │
│              26+ indicators, 18 map layers, 154 CVB records     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ├─────────────────────────────────────┐
                              ▼                                     ▼
┌─────────────────────────────────────┐ ┌─────────────────────────────────────┐
│  Backend API (:8790)                 │ │  JSON Export (data/*.json)          │
│  /api/indicators                     │ │  - indicators.json                 │
│  /api/health                         │ │  - economic.json                   │
│  /api/datasets                       │ │  - demographics.json               │
│                                      │ │  - climate.json                    │
│                                      │ │  - tourism.json                    │
│                                      │ │  - map-layers.json                 │
└─────────────────────────────────────┘ └─────────────────────────────────────┘
                              │                                     │
                              ▼                                     ▼
┌─────────────────────────────────────┐ ┌─────────────────────────────────────┐
│  Cloudflared Tunnel                  │ │  GitHub Pages                       │
│  volusia.zqmlabs.com → :80           │ │  volusia.zqmlabs.com                │
│  (Backend API access)                │ │  (Static frontend + JSON data)      │
└─────────────────────────────────────┘ └─────────────────────────────────────┘
```

---

## Connection Points

### 1. Data Synchronization
The frontend (`ZQM-Computing/volusia-portal`) uses static JSON files exported from the backend (`ZQM-Labs/project-volusia`).

**Export Process**:
```bash
# In ZQM-Labs/project-volusia
cd Tools/volusia_data
python -c "
import sqlite3, json
conn = sqlite3.connect('volusia.db')
conn.row_factory = sqlite3.Row
cur = conn.execute('SELECT * FROM indicators ORDER BY category, name')
indicators = [dict(r) for r in cur.fetchall()]
with open('../../data/indicators.json', 'w') as f:
    json.dump(indicators, f, indent=2)
"
```

**Import Process**:
The frontend's `vite.config.ts` copies `data/*.json` to `dist/data/` during build.

### 2. API Connection
The frontend can connect to the backend API for live data:

```typescript
// In ZQM-Computing/volusia-portal
const API_BASE = '/data';  // For static JSON files (GitHub Pages)
// OR
const API_BASE = 'https://volusia.zqmlabs.com/api';  // For live backend API
```

### 3. Deployment Connection
- **GitHub Actions** in `ZQM-Computing/volusia-portal` builds and deploys to `gh-pages` branch
- **CNAME** file points `volusia.zqmlabs.com` to GitHub Pages
- **Cloudflared** on ZQM-Node-4 routes traffic to the appropriate service

---

## Environment Variables

| Variable | Purpose | Location |
|----------|---------|----------|
| `VOLUSIA_DB_PATH` | Path to SQLite database | Backend |
| `VOLUSIA_PORT` | Portal port (default: 8789) | Backend |
| `VOLUSIA_HOST` | Portal host (default: 0.0.0.0) | Backend |
| `CENSUS_API_KEY` | Census API key (optional) | Backend |
| `BLS_API_KEY` | BLS API key (optional) | Backend |
| `BEA_API_KEY` | BEA API key (optional) | Backend |

---

## Deployment URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend (GitHub Pages) | https://volusia.zqmlabs.com | Static React portal |
| Backend API (Cloudflared) | https://volusia.zqmlabs.com/api | Live data API |
| Backend Portal (Direct) | http://192.168.1.226:8789 | Local network portal |
| GitHub Repo (Frontend) | https://github.com/ZQM-Computing/volusia-portal | Frontend source |
| GitHub Repo (Backend) | https://github.com/ZQM-Labs/project-volusia | Backend source |

---

## Maintenance Tasks

### Data Refresh
```bash
# On ZQM-Node-4
cd \ZQM-GARDEN-03\web\14_Projects\Active\Project-Volusia\Tools\volusia_data
python refresh_v2.py
```

### Frontend Deployment
```bash
# Automatic via GitHub Actions on push to master
# Or manual:
cd ZQM-Computing/volusia-portal
npm run build
# Deploy dist/ to gh-pages branch
```

### Cloudflared Tunnel
```bash
# On ZQM-Node-4
cloudflared tunnel --config C:\Users\zqmco\.cloudflared\config.yml run
```

---

## Troubleshooting

### Frontend shows no data
1. Check if `data/*.json` files exist in `ZQM-Computing/volusia-portal`
2. Run data export from `ZQM-Labs/project-volusia`
3. Rebuild and redeploy frontend

### Backend API not responding
1. Check if FastAPI is running on ZQM-Node-4: `netstat -ano | findstr :8790`
2. Check cloudflared tunnel status
3. Verify DNS: `nslookup volusia.zqmlabs.com`

### Data not updating
1. Run `refresh_v2.py` manually
2. Check `audit_log` table in SQLite
3. Verify API keys are set (if required)

---

**Last Updated**: 2026-09-07
**Maintainer**: ZQM Labs / ZQM Computing
