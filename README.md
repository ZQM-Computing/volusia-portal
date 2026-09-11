# ZQM Website — zqmlabs.com

> Public portal for ZQM Computing, connecting to other offerings and powering the Project Volusia public data portal.

---

## Domain-to-Repo Mapping

| Domain | Repo | Branch | Purpose |
|--------|------|--------|---------|
| zqmlabs.com | `ZQM-Computing/zqmlabs-frontend` | `master` | React SPA frontend |
| www.zqmlabs.com | `ZQM-Computing/zqmlabs-frontend` | `master` | Same as zqmlabs.com (canonical) |
| data.zqmlabs.com | `ZQM-Computing/zqmlabs-frontend` | `master` | Same repo — static data pages |
| docs.zqmlabs.com | `ZQM-Computing/zqmlabs-frontend` | `master` | Same repo — documentation |
| software.zqmlabs.com | `ZQM-Computing/zqmlabs-frontend` | `master` | React route (/business) |
| leaders.zqmlabs.com | `ZQM-Computing/zqmlabs-frontend` | `master` | React route (/leaders) |
| api.zqmlabs.com | `ZQM-Computing/zqmlabs-backend` | `main` | FastAPI backend |
| volusia.zqmlabs.com | `ZQM-Labs/volusia-zqmlabs` | `main` | Backend data pipeline |

---

## Modular Architecture

The ZQM project is organized into independently deployable modules:

```
zqmlabs-frontend <-> zqmlabs-backend (API calls)
zqmlabs-frontend <-> zqmlabs-gamification (gamification UI)
zqmlabs-backend <-> zqmlabs-gamification (proxy route)
zqmlabs-backend <-> zqmlabs-shared (shared types/utils)
zqmlabs-frontend <-> zqmlabs-shared (shared TypeScript types)
zqmlabs-backend <-> volusia-zqmlabs (data sharing)
```

### Modules

- **zqmlabs-frontend** (master) — React SPA serving zqmlabs.com, software.zqmlabs.com, leaders.zqmlabs.com
- **zqmlabs-backend** (main) — FastAPI serving api.zqmlabs.com and zqmlabs.com API routes
- **zqmlabs-gamification** (main) — Gamification missions, leaderboard, scoring
- **zqmlabs-shared** (main) — Shared types, utilities, configuration
- **volusia-zqmlabs** (main) — Backend data pipeline for volusia.zqmlabs.com (50 indicators)

---

## Overview

This is the **frontend layer** of the ZQM modular architecture. It provides the React SPA that serves [zqmlabs.com](https://zqmlabs.com) and all its subdomains.

## Development

```bash
npm install
npm run build
```

## Repo Map

```
zqmlabs-website (umbrella) = zqmlabs-frontend + documentation
zqmlabs-frontend (code) = React SPA
zqmlabs-backend (code) = FastAPI API server
zqmlabs-gamification (code) = Gamification service
zqmlabs-shared (code) = Shared types and utilities
volusia-zqmlabs (code) = Volusia data pipeline
```
