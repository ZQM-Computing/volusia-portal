# Project Volusia — Frontend Documentation

> Documentation for the Project Volusia frontend portal.

---

## Quick Links

| Resource | URL |
|----------|-----|
| **Live Portal** | https://volusia.zqmlabs.com |
|| **Backend Repo** | https://github.com/ZQM-Computing/volusia-portal |
| **API Endpoint** | https://volusia.zqmlabs.com/api |
| **Connection Guide** | [CONNECTION.md](../CONNECTION.md) |

---

## Overview

The frontend is a React/TypeScript application built with Vite, Tailwind CSS, Nivo charts, and Leaflet maps. It displays data from the backend API and static JSON files.

---

## Tech Stack

| Layer | Tech | License |
|-------|------|---------|
| Framework | React 18 + Vite + TypeScript | MIT |
| Charts | Nivo (D3-based) | MIT |
| Maps | Leaflet + react-leaflet | BSD-2 |
| Styling | Tailwind CSS | MIT |

---

## Pages

| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Mission, featured indicators, stakeholder cards |
| Data Explorer | `/data` | Searchable dataset catalog with charts |
| Maps | `/maps` | Interactive Leaflet map with toggleable layers |
| Business | `/business` | Market benchmarks, industry mix |
| Residents | `/residents` | Income, demographics, cost-of-living |
| Tourists | `/tourists` | Conditions, events, visitor volume |
| Leaders | `/leaders` | Capital flows, permitting, workforce |

---

## Data Sources

The frontend uses two data sources:

1. **Static JSON files** (primary) — Fast, works on GitHub Pages
2. **Live API** (fallback) — Real-time data from backend

See [CONNECTION.md](../CONNECTION.md) for details.

---

## Development

```bash
npm install
npm run dev          # http://localhost:5173
npm run build        # outputs to dist/
npm run preview      # http://localhost:4173
```

---

## Deployment

### GitHub Pages (Automatic)

Push to master → GitHub Actions builds and deploys to gh-pages.

### Manual

```bash
npm run build
# Deploy dist/ to GitHub Pages
```

---

## License

MIT © 2026 ZQM Computing
