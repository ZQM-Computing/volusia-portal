# Architecture — Project Volusia

> System architecture and data flow documentation.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Sources (112)                        │
│  Census │ BLS │ BEA │ NOAA │ EPA │ USGS │ FEMA │ HUD │ USDA    │
│  CDC │ FDLE │ FL DEP │ Volusia County │ Universities │ etc.    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Data Pipeline (refresh_v2.py)                │
│  Fetch → Validate → Transform → Store → Quality Check           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SQLite Database (volusia.db)                   │
│  indicators │ time_series │ submissions │ audit_log │ datasets  │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  Portal (:8789)  │ │  API (:8790)     │ │  Proxy (:80)     │
│  FastAPI         │ │  FastAPI         │ │  Python stdlib   │
│  15 endpoints    │ │  4 endpoints     │ │  Static + Proxy  │
│  12 charts       │ │  CRUD            │ │  /api/* → :8789  │
│  HTML pages      │ │  Validation      │ │  /api/v1/* → :8790│
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## Components

### 1. Data Sources

#### Tier 1 — Government (Highest Trust)
- Census Bureau, BLS, BEA, NOAA, EPA, USGS, FEMA, HUD, USDA, CDC
- FDLE, FL DEP, FL DOE, FDOT, Volusia County

#### Tier 2 — Academic/Nonprofit (Verified)
- Universities (.edu), FRED, County Health Rankings, Zillow, Realtor.com

#### Tier 3 — Commercial (Use with Caution)
- SpotCrime, CrimeByCounty, ZipCheckup (cross-reference required)

### 2. Data Pipeline

**File**: `Tools/volusia_data/refresh_v2.py`

```
1. Fetch data from source (API, CSV download, scraping)
2. Validate format and range
3. Transform to standard schema
4. Store in SQLite
5. Run quality checks
6. Log to audit_log
```

### 3. Database Schema

**File**: `Tools/volusia_data/volusia.db`

#### indicators
| Column | Type | Description |
|--------|------|-------------|
| name | TEXT PK | Unique indicator name |
| value | TEXT | Numeric or text value |
| unit | TEXT | Unit of measurement |
| category | TEXT | One of 15 categories |
| source | TEXT | Originating agency |
| source_url | TEXT | Specific URL |
| vintage | TEXT | Year or date range |
| description | TEXT | Human-readable description |
| fetched_at | TEXT | Fetch timestamp |

#### time_series
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| indicator_name | TEXT | Reference to indicator |
| value | REAL | Numeric value |
| unit | TEXT | Unit of measurement |
| source | TEXT | Source agency |
| vintage | TEXT | Year or date range |
| fetched_at | TEXT | Fetch timestamp |

#### submissions
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment |
| submission_id | TEXT | Unique submission ID |
| contribution_type | TEXT | Type of contribution |
| content | TEXT | JSON content |
| status | TEXT | queued/approved/rejected |
| reviewer | TEXT | Assigned reviewer |
| created_at | TEXT | Submission timestamp |
| updated_at | TEXT | Last update timestamp |

### 4. Web Layer

#### Portal (port 8789)
**File**: `Tools/volusia_data/portal_app.py`

- 15 API endpoints
- 12 chart endpoints
- 8 HTML page endpoints
- Coherent data groups

#### Contribution API (port 8790)
**File**: `Tools/volusia_data/contribution_api.py`

- 4 API endpoints
- Contribution routing
- Reviewer assignment
- Status tracking

#### Reverse Proxy (port 80)
**File**: `deploy_portal.py`

- Static file serving
- API request routing
- Port 80 → :8789 or :8790

### 5. Quality System

#### Validation (quality/validate.py)
- Range validation per indicator
- Freshness validation per source
- Cross-source coherence checks
- Automated quality scoring

#### Citation Scoring (quality/citations.py)
- Completeness (40%)
- Attribution quality (30%)
- URL quality (20%)
- Cross-reference (10%)

#### Link Checking (quality/check_links.py)
- HTTP status verification
- Response time measurement
- Broken link detection

---

## Data Flow

### Ingestion Flow
```
Source → Fetcher → Validator → Transformer → SQLite
                                            ↓
                                        Quality Check
                                            ↓
                                        Audit Log
```

### Query Flow
```
Client → Proxy (:80) → Portal (:8789) → SQLite
                    ↓
                    Contribution API (:8790) → SQLite
```

### Contribution Flow
```
Submit → API (:8790) → SQLite (submissions)
              ↓
              Route to Reviewer
              ↓
              Approve/Reject
              ↓
              Update indicators (if approved)
```

---

## Security

### API Keys
- Optional API key enforcement via `VOLUSIA_API_KEYS` env var
- Anonymous submissions allowed for web form

### Input Validation
- JSON schema validation
- URL format validation
- Value range validation
- SQL injection prevention (parameterized queries)

### Access Control
- No authentication required for reads
- Optional API key for writes
- Reviewer assignment for contribution triage

---

## Performance

### Database
- SQLite with WAL mode
- Indexed on name, category, source
- 474 indicators, ~100KB

### API Response Times
- Health check: <10ms
- Indicator list: <50ms
- Chart generation: <500ms
- Search: <100ms

### Caching
- In-memory coherence groups
- Chart image caching (future)
- Database connection pooling (future)

---

## Scalability

### Current
- Single-server deployment
- SQLite database
- Python stdlib HTTP server

### Future
- PostgreSQL for multi-user
- Redis for caching
- CDN for static files
- Kubernetes for orchestration

---

## Monitoring

### Health Checks
- `/api/health` — System status
- `/api/status` — Detailed metrics
- `quality/validate.py` — Data quality

### Audit Trail
- `audit_log` table tracks all pipeline runs
- `submissions` table tracks all contributions
- Console logging for errors

### Alerting
- `alerts/staleness_check.py` — Data freshness
- Webhook integration (future)

---

## Testing

### Unit Tests
```bash
python -m pytest tests/
```

### Integration Tests
```bash
python Tools/volusia_data/quality/validate.py
```

### Manual Testing
```bash
curl http://localhost:80/api/health
curl http://localhost:80/api/indicators
```

---

## Dependencies

### Required
- Python 3.11+
- FastAPI
- Uvicorn
- SQLite 3

### Optional
- matplotlib (charts)
- requests (fetches)
- pandas (processing)

---

*Last updated: 2026-09-06*
