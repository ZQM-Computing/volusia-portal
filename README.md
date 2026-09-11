# ZQM Company Portal — zqmlabs.com

> Advertising ZQM Computing services, connecting to other offerings, and powering the Project Volusia public data portal.

---

## 🌐 Domains Served

| Domain | Repo | Branch | Purpose |
|--------|------|--------|---------|
| **zqmlabs.com** | `ZQM-Computing/zqmlabs-website` | `master` | Primary portal — services, data, gamification |
| **www.zqmlabs.com** | `ZQM-Computing/zqmlabs-website` | `master` | Same as zqmlabs.com (canonical) |
| **data.zqmlabs.com** | `ZQM-Computing/zqmlabs-website` | `master` | Same repo — static data pages |
| **docs.zqmlabs.com** | `ZQM-Computing/zqmlabs-website` | `master` | Same repo — documentation |
| **volusia.zqmlabs.com** | `ZQM-Labs/volusia-zqmlabs` | `main` | Backend data pipeline (separate repo) |
| **api.zqmlabs.com** | `ZQM-Labs/volusia-zqmlabs` | `main` | Backend API (separate repo) |

**Domain-to-repo naming rule**: Each repo name contains its primary domain.
`zqmlabs-website` serves `zqmlabs.com`. `volusia-zqmlabs` serves
`volusia.zqmlabs.com`.

---

## Overview

`zqmlabs-website` is the **React + Vite + TypeScript** frontend that serves
[zqmlabs.com](https://zqmlabs.com). It is the public-facing web application
for ZQM Computing — advertising our services and connecting to other ZQM
offerings including Project Volusia, quantum simulation, and more.

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    zqmlabs.com                           │
│                   Cloudflare CDN                         │
├─────────────────────────────────────────────────────────┤
│              nginx (port 80)                              │
│         ┌───────────┬──────────┐                        │
│         │  Static    │  Proxy   │                        │
│         │  React SPA │  :8000   │                        │
│         └─────┬─────┴────┬─────┘                        │
│               │          │                               │
│               ▼          ▼                               │
│    zqmlabs-website     volusia-zqmlabs                     │
│    (React: src/)    (FastAPI: backend/)                   │
│    repo: ZQM-Computing/  repo: ZQM-Labs/                 │
│           zqmlabs-website         volusia-zqmlabs         │
└─────────────────────────────────────────────────────────┘
```

### Domain → Repo → Branch Mapping

```
zqmlabs.com ──▶ ZQM-Computing/zqmlabs-website ──▶ master branch
                              │
                              ├── React SPA (src/) → static HTML
                              ├── FastAPI backend (backend/) → :8000
                              ├── Gamification (gamification/) → /missions
                              └── Data pages (data/) → /data/{category}

volusia.zqmlabs.com ──▶ ZQM-Labs/volusia-zqmlabs ──▶ main branch
                                    │
                                    └── FastAPI backend → :8000
                                            ├── 50+ indicators
                                            ├── 474 records in volusia.db
                                            └── Gamification engine
```

---

## Quick Links

| Resource | URL | Repo |
|----------|-----|------|
| **Live Portal** | https://zqmlabs.com | `ZQM-Computing/zqmlabs-website` |
| **Backend API** | https://api.zqmlabs.com | `ZQM-Labs/volusia-zqmlabs` |
| **Backend Repo** | https://github.com/ZQM-Labs/volusia-zqmlabs | `volusia-zqmlabs` |
| **Live Data** | https://zqmlabs.com/data | `ZQM-Computing/zqmlabs-website` |
| **Gamification** | https://zqmlabs.com/missions | `ZQM-Computing/zqmlabs-website` |
| **Connection Guide** | [DEPLOY.md](DEPLOY.md) | — |

---

## Key Features

- **50+ Live Indicators** — Economic, demographics, climate, tourism, infrastructure, safety, and more
- **30 Gamification Missions** — 5 tiers, 14 pathways (A–S)
- **Real-Time Data** — Direct from government APIs, refreshed on demand
- **Layered Layout** — Scannable, multi-constituency design
- **Open Source** — MIT License, community contributions welcome

---

## Directory Structure

```
zqmlabs-website/
├── src/                    # React components and pages
├── backend/                # FastAPI backend (serves :8000)
├── data/                   # Static data pages (served by nginx)
├── public/                 # Static assets
├── nginx/                  # nginx configuration
├── scripts/                # Deployment and utility scripts
├── docs/                   # Documentation
├── tests/                  # Test suite
├── package.json            # React dependencies
├── vite.config.ts          # Vite build config
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Docker Compose orchestration
├── deploy.py               # Automated deployment pipeline
└── README.md               # This file
```

---

## Development

### Local Setup
```bash
# Install dependencies
npm install

# Start React dev server
npm run dev

# Start backend
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
```

### Deploy
```bash
python scripts/deploy.py
```

---

## License

MIT — see [LICENSE](LICENSE)

