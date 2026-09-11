# ZQM Company Portal — zqmlabs.com

> Advertising ZQM Computing services, connecting to other offerings, and powering the Project Volusia public data portal.

---

## Overview

`zqmlabs-website` is the **React + Vite + TypeScript** frontend that serves [zqmlabs.com](https://zqmlabs.com). It is the public-facing web application for ZQM Computing — advertising our services and connecting to other ZQM offerings including Project Volusia, quantum simulation, and more.

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
│    zqmlabs-website     volusia-zqmlabs                          │
│    (React)        (FastAPI)                            │
└─────────────────────────────────────────────────────────┘
```

---

## Quick Links

| Resource | URL |
|----------|-----|
| **Live Portal** | https://zqmlabs.com |
| **Backend API** | https://zqmlabs.com/api |
| **Backend Repo** | https://github.com/ZQM-Labs/volusia-zqmlabs |
| **Live Data** | https://zqmlabs.com/data |
| **Gamification** | https://zqmlabs.com/missions |
| **Connection Guide** | [DEPLOY.md](DEPLOY.md) |

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
├── src/
│   ├── components/     # React components
│   ├── hooks/          # Custom React hooks
│   ├── pages/          # Page components (Hero, Data, Missions, etc.)
│   ├── types/          # TypeScript type definitions
│   ├── utils/          # Utility functions
│   ├── App.tsx         # Main App component
│   └── main.tsx        # Entry point
├── index.html          # HTML entry point
├── package.json        # React + Vite + TypeScript dependencies
├── vite.config.ts      # Vite build configuration
├── tailwind.config.js  # Tailwind CSS configuration
├── tsconfig.json       # TypeScript configuration
├── Dockerfile          # Frontend Docker container
└── docker-compose.yml  # Docker Compose orchestration
```

---

## Development

### Prerequisites

- Node.js 18+
- npm

### Frontend Setup

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Deployment

The `deploy.py` script automates the full pipeline:
1. Backend data refresh
2. Static page generation
3. React frontend build
4. Nginx sync and restart
5. Endpoint verification (21 endpoints)

```bash
# Full deploy
python scripts/deploy.py

# Skip static generation (React-only)
python scripts/deploy.py --skip-generate

# Skip restart
python scripts/deploy.py --skip-restart
```

---

## API Integration

The frontend proxies API requests to the backend via nginx:

| Frontend Path | Backend Endpoint | Description |
|---------------|-----------------|-------------|
| `/data/indicators.json` | `GET /indicators` | All indicators |
| `/data/latest.json` | `GET /latest` | Latest data |
| `/data/{category}/` | `GET /data/{category}` | Category data |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

ZQM-Computing is focused on building the ZQM company portal and connecting ZQM services. Project Volusia is one flagship initiative.

---

## License

MIT License — see [LICENSE](LICENSE).
