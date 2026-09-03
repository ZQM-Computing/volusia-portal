# Project Volusia — Public Data Portal

Open-source intelligence and data-driven decision-making platform for Volusia County, Florida.

## Stack

| Layer       | Tech                        | License     |
|-------------|-----------------------------|-------------|
| Framework   | React 18 + Vite + TypeScript| MIT         |
| Charts      | Nivo (D3-based)             | MIT         |
| Maps        | Leaflet + react-leaflet     | BSD-2       |
| Styling     | Tailwind CSS                | MIT         |
| Server      | nginx (Docker)              | BSD-2       |

All dependencies are free, permissive-license (MIT/Apache/BSD), zero cost.

## Pages

- **Portal Home** (`/`) — Mission, featured indicators, stakeholder cards, updates
- **Data Explorer** (`/data`) — Searchable dataset catalog with Nivo charts
- **Maps** (`/maps`) — Interactive Leaflet map with toggleable layers
- **Business** (`/business`) — Market benchmarks, industry mix, tool access
- **Residents** (`/residents`) — Income, demographics, cost-of-living
- **Tourists** (`/tourists`) — Conditions, events, visitor volume
- **Leaders** (`/leaders`) — Capital flows, permitting, workforce

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

## Docker

```bash
# Build image
docker build -t zqmcomputing/volusia-portal .

# Run on any port
docker run -d -p 8080:80 --name volusia zqmcomputing/volusia-portal

# Stop
docker stop volusia && docker rm volusia
```

Then open http://localhost:8080

## Deploy on ZQM-MESH

```bash
# Build and tag
docker build -t zqmcomputing/volusia-portal:1.0 .
docker save zqmcomputing/volusia-portal:1.0 | ssh root@<node> docker load

# Run on mesh node (e.g., port 8080)
ssh root@<node> "docker run -d -p 8080:80 --name volusia --restart unless-stopped zqmcomputing/volusia-portal:1.0"
```

## Data

`src/data/sampleData.ts` holds the demo datasets and indicators.
Replace with real API calls as sources are wired up per DATA_CATALOG.md.

## License

MIT © 2026 ZQM Labs / ZQM Computing
