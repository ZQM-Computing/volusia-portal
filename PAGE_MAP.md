# Project Volusia — Page Map

## Navigation (from zqmlabs.com)

### Main Navigation
| Page | URL | Description |
|------|-----|-------------|
| Portal Home | `/` | Homepage with search, stats, missions |
| Data Explorer | `/data` | All indicators with search/filter |
| Maps | `/maps` | Interactive map layers |
| Business | `/business` | Business constituency data |
| Residents | `/residents` | Resident demographics & income |
| Tourists | `/tourists` | Tourism & hotel occupancy |
| Leaders | `/leaders` | Leadership & government data |
| Gamification | `/gamification` | Missions, leaderboard, badges |

### Homepage Sections
1. **Hero** — Search bar + CTA buttons (Data Explorer, Maps)
2. **Core Constituencies** — 4 stat cards (Business, Residents, Tourists, Leaders)
3. **"I am a..."** — 10 persona cards
4. **Top Missions** — 5 missions from gamification API
5. **Charts** — Income Trend + Employment & Unemployment
6. **Climate Summary** — Avg Max Temp, Precipitation, Avg Min Temp
7. **Data Domains** — 10 domain cards with search filter
8. **Community Pillars** — 4 expandable umbrellas
9. **Map Preview** — County boundary, beach access, water bodies
10. **Data Sources** — Census, BLS, BEA
11. **Human README** — Getting started + features
12. **AI Agent README** — API endpoints + data schema

### Data Explorer Pages
- **Indicators list** — All 48 indicators, filterable by category
- **Individual indicator** — `/data/indicators/{name}`
- **CSV export** — `/data/indicators.csv`

### Maps Pages
- **Map layers** — Interactive Leaflet maps
- **Layer categories** — Demographics, Economy, Environment, Government

### Constituency Pages
- **Business** — Industry mix, investment, workforce
- **Residents** — Population trends, income, housing
- **Tourists** — Hotel occupancy, ADR, RevPAR
- **Leaders** — Government spending, employees, federal land

### Gamification Pages
- **Missions** — Mission catalog with tiers
- **Leaderboard** — Top contributors
- **State** — Individual contributor stats

### API/Debug Pages
- **Health** — `/health` (backend only)
- **Diagnostics** — `/diagnostics` (auth required)
- **API Status** — `/api/fetch-status`
- **Contributor** — `/api/contributor`
- **Webhooks** — `/api/webhook`

## How to Reach Each Page

### From Homepage (`/`)
1. Click "Data Explorer" → `/data`
2. Click "Maps" → `/maps`
3. Click "Business" card → `/business`
4. Click "Residents" card → `/residents`
5. Click "Tourists" card → `/tourists`
6. Click "Leaders" card → `/leaders`
7. Click "🏆 Gamification" nav link → `/gamification`

### From Data Explorer (`/data`)
- Search indicators by name
- Filter by category (Demographics, Economic, Education, etc.)
- Click indicator → detail view
- Export as CSV

### From Maps (`/maps`)
- Select layer category
- Toggle layer visibility
- Click markers for details

### From Constituency Pages
- Use breadcrumb navigation to go back home
- Use nav links to switch between constituencies

### From Gamification (`/gamification`)
- View mission catalog
- Check leaderboard
- View personal stats

## API Access

### Direct API Calls
```
GET https://zqmlabs.com/health
GET https://zqmlabs.com/indicators
GET https://zqmlabs.com/indicators?category=Demographics
GET https://zqmlabs.com/indicators/{name}
GET https://zqmlabs.com/data/indicators.json
GET https://zqmlabs.com/data/datasets.json
GET https://zqmlabs.com/data/map-layers.json
GET https://zqmlabs.com/categories
GET https://zqmlabs.com/analytics/summary
GET https://zqmlabs.com/pulse.json
GET https://zqmlabs.com/api/contributor
GET https://zqmlabs.com/api/fetch-status
```

### Self-Service API
```
POST https://zqmlabs.com/api/contribute?source=...
POST https://zqmlabs.com/api/webhook?event=...
GET  https://zqmlabs.com/api/indicators/search?q=...
GET  https://zqmlabs.com/api/indicators/bulk?names=...
GET  https://zqmlabs.com/api/indicators/stats
GET  https://zqmlabs.com/api/export/json
GET  https://zqmlabs.com/api/export/csv
GET  https://zqmlabs.com/api/keys
```

### Admin API (auth required)
```
POST https://zqmlabs.com/refresh?secret=<token>
GET  https://zqmlabs.com/diagnostics?secret=<token>
```