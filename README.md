# Project Volusia — Public Data Portal

> Open-source intelligence and data-driven decision-making for Volusia County, Florida.

---

## Quick Links

| Resource | URL |
|----------|-----|
| **Live Portal** | https://volusia.zqmlabs.com |
| **Backend Repo** | https://github.com/ZQM-Labs/project-volusia |
| **API Endpoint** | https://volusia.zqmlabs.com/api |
| **Connection Guide** | [CONNECTION.md](CONNECTION.md) |

---

## Overview

Project Volusia is a comprehensive open data portal for Volusia County, Florida. It aggregates 26+ indicators across 4 categories from authoritative sources including US Census Bureau, BLS, BEA, and NOAA.

### Key Features

- **26+ Indicators** — Demographics, economy, climate, tourism
- **18 Map Layers** — Interactive geographic data
- **Real-Time Data** — Direct from government APIs
- **Open Source** — MIT License, community contributions welcome

---

## Pages

- **Portal Home** (`/`) — Mission, featured indicators, stakeholder cards
- **Data Explorer** (`/data`) — Searchable dataset catalog with Nivo charts
- **Maps** (`/maps`) — Interactive Leaflet map with toggleable layers
- **Business** (`/business`) — Market benchmarks, industry mix, tool access
- **Residents** (`/residents`) — Income, demographics, cost-of-living
- **Tourists** (`/tourists`) — Conditions, events, visitor volume
- **Leaders** (`/leaders`) — Capital flows, permitting, workforce

---

## Stack

| Layer | Tech | License |
|-------|------|---------|
| Framework | React 18 + Vite + TypeScript | MIT |
| Charts | Nivo (D3-based) | MIT |
| Maps | Leaflet + react-leaflet | BSD-2 |
| Styling | Tailwind CSS | MIT |
| Server | nginx (Docker) | BSD-2 |

---

## Run locally

```bash
cd volusia-portal
npm install
npm run dev          # http://localhost:5173
```

## Build

```bash
npm run build        # outputs to dist/
npm run preview      # http://localhost:4173
```

---

## Data Sources

This frontend uses static JSON files exported from the backend.

**Backend Repository**: https://github.com/ZQM-Labs/project-vlusia

### Data Categories

| Category | Count | Examples |
|----------|-------|----------|
| Economic | 13 | unemployment_rate_bls, median_household_income_acs, employment_qcew |
| Demographics | 8 | total_population_pep_2024, median_age_acs, pct_over_65_acs |
| Climate | 6 | avg_max_temp, avg_min_temp, total_precip |
| Tourism | 3 | hotel_occupancy_pct, avg_daily_rate, revpar |

---

## API

The FastAPI backend serves live indicators from SQLite:

| Endpoint | Description |
|----------|-------------|
| `/api/` | Root |
| `/api/health` | Health check + indicator count |
| `/api/indicators` | All indicators (filter: `?category=Economic`) |
| `/api/indicators/{name}` | Single indicator |
| `/api/indicators.csv` | Download all as CSV |
| `/api/datasets` | Latest datasets |
| `/api/refresh` | Trigger a pipeline refresh |

---

## Deployment

### Frontend (GitHub Pages)
```bash
# Automatic via GitHub Actions on push to master
# Or manual:
npm run build
# Deploy dist/ to gh-pages branch
```

### Backend (ZQM-Node-4)
```bash
cd Tools/volusia_data
python portal_app.py
# Portal: http://localhost:8789
# API: http://localhost:8790
```

---

## Connection to Backend

See [CONNECTION.md](CONNECTION.md) for detailed documentation on how this frontend connects to the ZQM-Labs backend.

---

## License

MIT © 2026 ZQM Labs / ZQM Computing
