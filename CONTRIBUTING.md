# Contributing to Project Volusia

## Overview

Project Volusia is an open-source public data portal and intelligence platform for Volusia County, Florida. We welcome contributions from the community across **19 pathways** covering data, code, infrastructure, community knowledge, and more.

| Pathway | Name | XP | Purpose |
|---------|------|-----|---------|
| A | Data Source | 400-450 | Add new data fetchers, datasets, indicators |
| B | Analysis | 500 | Research analyses with methodology and results |
| C | Social Media | — | Event/resource sharing via social platforms |
| D | Map Layer | 350 | GeoJSON, Shapefile map layer submissions |
| E | Industry Mover | 400 | Capital flow, infrastructure, policy metrics |
| F | Community Knowledge | 150 | Local observations, community input |
| G | School Project | — | Academic contributions from students |
| H | Tool | 400 | New tools/utilities for the project |
| I | Direct Citizenry | 150 | Simple submission for any contribution |
| J | Code & Feature | 300-450 | Source code improvements (frontend/backend) |
| J* | Youth & Student | 150-300 | Young people's observations and ideas |
| K | Infrastructure | 400 | Docker, nginx, cloudflared, networking |
| K* | Seniors & Aging | 150-300 | Accessibility, health, social connection |
| L | CI/CD & DevOps | 450 | GitHub Actions, automation, pipelines |
| L* | Nonprofit & Community | 350 | Capacity, reach, funding data |
| M | Testing & QA | 350 | Unit, integration, E2E, security tests |
| M* | Healthcare & Public Health | 400 | Access, quality, outcomes data |
| N | Documentation | 250 | README, docs, guides, examples |
| N* | Agriculture, Farming & Maritime | 400 | Production, market, environmental data |
| O | Accessibility & Inclusion | 250 | Digital, physical, policy accessibility |
| P | Crisis & Disaster Response | 350 | Situation reports, resource needs, resilience |
| Q | Environmental Stewardship | 400 | Water, air, wildlife, climate, pollution |
| R | Cultural Heritage & Arts | 350 | Events, heritage sites, arts organizations |
| S | Workforce & Labor | 400 | Hiring, wages, skills, training, disparities |

*Marked pathways are constituency-specific templates within CONSTITUENCY_CONTRIBUTIONS.md

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 20+
- Python 3.11+
- Git

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/ZQM-Computing/volusia-portal.git
cd volusia-portal

# Build and start the project
docker compose up -d

# Verify the backend is healthy
curl http://localhost:8000/health

# Verify the frontend is running
curl http://localhost:8080
```

### TypeScript Compilation

```bash
npx tsc --noEmit
```

## Contribution Types

### 0. Code & Feature Contributions (Pathway J)

Code contributors submit pull requests that improve the Project Volusia source code.

- **Frontend**: React/Vite/TypeScript/Tailwind components, Nivo charts, Leaflet maps, hooks
- **Backend**: FastAPI endpoints, data pipeline (refresh_v2.py), gamification engine (scoring.py), security
- **Infrastructure**: Docker compose, nginx config, cloudflared tunnel, CI/CD workflows
- **Prerequisites**: Node.js 20+, Python 3.11+, Git, Docker

```bash
# Clone and setup
git clone https://github.com/ZQM-Computing/volusia-portal.git
cd volusia-portal
npm install

# Build and test
npx tsc --noEmit        # Must pass with zero errors
npm run build            # Must succeed
npm test                 # 7/7 tests pass
```

- Fork and create a feature branch
- Follow existing code structure and patterns
- `npx tsc --noEmit` must pass with zero errors
- `npm run build` must succeed
- `pytest tests/` must pass (7/7)
- Conventional commits (`feat:`, `fix:`, `chore:`, `docs:`)
- PR reviews required before merge
- **XP**: Code Commiter (300), Test Contributor (350), Review Contributor (300)

### 1. Data Contributions (Pathway A)

- Add new indicators to the `/indicators` endpoint
- Add new datasets to the `/datasets` catalog
- Add new map layers with GeoJSON geometry
- Add new data fetchers to scripts/refresh_v2.py
- Follow existing data format conventions and caching
- **XP**: Data Architect (400), Source Master (450)

### 2. Infrastructure Contributions (Pathway K)

- Docker, nginx, cloudflared configuration fixes
- Security hardening (firewall rules, auth, TLS)
- Service restart and recovery procedures
- Port and networking resolution
- **XP**: Infrastructure Builder (400)

### 3. CI/CD & DevOps Contributions (Pathway L)

- GitHub Actions workflow improvements
- Automated testing and deployment pipelines
- Cron job and watchdog automation
- Dependency updates (Dependabot)
- **XP**: CI/CD Contributor (450)

### 4. Testing & QA Contributions (Pathway M)

- Backend tests (pytest, FastAPI endpoint tests)
- Frontend tests (TypeScript compilation, build verification)
- Infrastructure tests (health checks, security headers)
- Security tests (HMAC auth, CORS, rate limiting)
- **XP**: Test Contributor (350)

### 5. Documentation & Technical Writing Contributions (Pathway N)

- README, CONTRIBUTING.md, API docs improvements
- Architecture and methodology documentation
- Constituency-specific guides (Business, Resident, Tourist, Movers)
- Gamification system documentation
- **XP**: Documentation Contributor (250)

### 6. Analysis Contributions (Pathway B)

- Research questions with methodology, results, limitations
- Reproducibility package required (code, data, environment)
- Conflict of interest disclosure required
- **XP**: Researcher (500)

### 7. Community & Constituency Contributions (Pathways F, J*, K*, L*, M*, N*, O, P, Q, R, S)

- Community knowledge, youth, seniors, nonprofits, healthcare
- Agriculture, maritime, environmental, cultural, workforce
- Accessibility, crisis response, and more
- All templates available in `CONTRIBUTION/templates/CONSTITUENCY_CONTRIBUTIONS.md`
- **XP**: Community Voice (150), Data Architect (400), Source Master (450)

### 8. Issue Reporting

- Use the issue templates (Bug Report, Feature Request)
- Include reproduction steps and environment details
- Search existing issues before creating new ones

### 9. Direct Citizenry Contributions (Pathway I)

- Use this pathway if you aren't sure which pathway to use
- Submit any contribution type with free text description
- **XP**: Community Voice (150)

## Code Standards

- **TypeScript**: Strict mode, no `any` types, `npx tsc --noEmit` must pass
- **Python**: PEP 8, type hints, WAL + busy_timeout + foreign_keys on every DB connection
- **SQL**: Parameterized queries only
- **API**: RESTful conventions, proper HTTP status codes, HMAC auth on `/refresh`
- **Docker**: Multi-stage builds, minimal images, healthchecks
- **Security**: 13 nginx security headers (HSTS, CSP, Permissions-Policy, COOP/COEP/CORP)

## Branch Protection

- All PRs require review before merging
- CI must pass before merge (npx tsc --noEmit + npm run build + pytest tests/)
- Main branch is protected

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Security

Please report security vulnerabilities to security@zqm-computing.io. Do not open public issues for security concerns.

## Contact

- **Email**: zqmcomputing@gmail.com
- **GitHub**: [ZQM-Computing/volusia-portal](https://github.com/ZQM-Computing/volusia-portal)
- **Website**: [volusia.zqmlabs.com](https://volusia.zqmlabs.com)
- **Board**: [GitHub Projects #7](https://github.com/users/ZQM-Computing/projects/7)
- **Templates**: [CONTRIBUTION/templates/](CONTRIBUTION/templates/) — 10 template files, 19 pathways
