# CODE & FEATURE CONTRIBUTION

Pathway J — Code & Feature Contributor

Code contributors submit pull requests that improve the Project Volusia source code — frontend components, backend endpoints, gamification engine, data pipeline, and infrastructure.

## Pathway Fields

| Field | Description | Type |
|-------|-------------|------|
| **Branch Name** | Feature branch name | Free text |
| **PR Number** | GitHub PR link/number | URL |
| **Type** | Bug fix, feature, refactor, docs, test | Select |
| **Components** | Which files/components changed | List |
| **Test Results** | Did CI pass? | Boolean |
| **Build Result** | Did npm run build pass? | Boolean |
| **TS Compilation** | Did tsc --noEmit pass? | Boolean |
| **Description** | What does this change? | Free text |
| **Review Status** | Pending, approved, merged | Select |
| **Permission** | Open source — MIT license | Confirm |

## Contribution Types

### Frontend Contributions
- React/Vite/TypeScript/Tailwind component changes
- Page layout improvements, responsive design fixes
- Chart/visualization updates (Nivo, Leaflet)
- Hook improvements (useApi, useDebounce)
- TypeScript type fixes and interface updates
- Accessibility improvements (ARIA, keyboard nav)
- Dark mode, mobile nav, error boundary fixes

### Backend Contributions
- FastAPI endpoint additions/modifications
- Data pipeline improvements (refresh_v2.py, scrapers)
- Gamification engine changes (scoring.py, routes.py)
- SQLite query optimizations, WAL/PRAGMAs
- Authentication/HMAC security improvements
- CORS, rate limiting, middleware additions
- OpenAPI spec updates

### Infrastructure & DevOps
- Docker compose configuration changes
- nginx configuration updates
- cloudflared tunnel configuration
- CI/CD pipeline improvements (GitHub Actions)
- .env.example and environment management
- Makefile targets, dev scripts
- Watchdog and monitoring improvements
- Firewall, port, and networking configuration

### Code Standards
- `npx tsc --noEmit` must pass with zero errors
- `npm run build` must succeed
- `pytest tests/` must pass (7/7)
- Conventional commits (`feat:`, `fix:`, `chore:`, `docs:`)
- All changes must pass CI before merge
- PR reviews required before merge

### XP & Missions
- **Code Commiter** (300 XP): Submit a PR that passes all CI checks
- **Test Contributor** (350 XP): Add tests covering new code
- **CI/CD Contributor** (450 XP): Improve or add CI/CD pipeline
- **Review Contributor** (300 XP): Review 5+ PRs from others
- **Infrastructure Builder** (400 XP): Fix or improve deployment/infrastructure

---

# INFRASTRUCTURE CONTRIBUTION

Pathway K — Infrastructure Contributor

Infrastructure contributors improve the deployment, hosting, monitoring, and operational reliability of Project Volusia — Docker, nginx, cloudflared, CI/CD, and monitoring systems.

## Pathway Fields

| Field | Description | Type |
|-------|-------------|------|
| **Environment** | Docker, nginx, cloudflared, CI, monitoring | Select |
| **Issue** | GitHub issue number or description | URL/Free text |
| **Change Type** | Config fix, service restore, security hardening | Select |
| **Before State** | What was broken? | Free text |
| **After State** | What did you fix? | Free text |
| **Verification** | How did you verify the fix? | Free text |
| **Permissions** | Admin/root access needed? | Boolean |
| **Impact** | How does this affect the system? | Free text |

## Infrastructure Areas

### Docker & Containerization
- Docker Compose configuration fixes
- Container healthcheck configurations
- Port mapping and networking resolution
- Volume and cache management
- WSL2/Windows Docker Desktop fixes

### nginx Configuration
- Security header management (HSTS, CSP, Permissions-Policy)
- SSL/TLS certificate configuration
- Reverse proxy configuration
- Static file serving and caching
- CORS and access control rules

### cloudflared Tunnel
- Tunnel service management (NSSM)
- DNS and routing configuration
- Authentication and access control
- Certificate and TLS management
- Service restart and recovery

### CI/CD & GitHub Actions
- GitHub Actions workflow improvements
- Automated testing and deployment pipelines
- GitHub Pages deployment configuration
- Branch protection and merge strategies
- Dependabot and automated security updates

### Monitoring & Watchdog
- Prometheus/Grafana dashboards
- Health check endpoints and alerts
- Log aggregation and analysis
- Cron job management
- Service recovery automation

### Code Standards
- `npx tsc --noEmit` must pass with zero errors
- `npm run build` must succeed
- `pytest tests/` must pass (7/7)
- All changes documented in PROJECT_TRACKING.md
- Infrastructure changes require admin approval

### XP & Missions
- **Infrastructure Builder** (400 XP): Fix or improve deployment/infrastructure
- **CI/CD Contributor** (450 XP): Improve or add CI/CD pipeline
- **Test Contributor** (350 XP): Add tests covering new code

---

# CI/CD & DEVOPS CONTRIBUTION

Pathway L — CI/CD & DevOps Contributor

DevOps contributors improve the continuous integration and deployment pipelines, automation, and operational tooling for Project Volusia.

## Pathway Fields

| Field | Description | Type |
|-------|-------------|------|
| **Pipeline** | Which pipeline was modified? | Select |
| **Change Type** | Add, fix, improve, optimize | Select |
| **Workflow File** | .github/workflows/*.yml | File |
| **Test Results** | Did the pipeline pass? | Boolean |
| **Deploy Result** | Did the deploy succeed? | Boolean |
| **Automation Level** | Manual → Semi-auto → Full auto | Select |
| **Documentation** | Updated docs? | Boolean |
| **Permission** | Admin/root access needed? | Boolean |

## CI/CD Areas

### GitHub Actions Workflows
- `ci.yml` — Build, TypeScript compilation, tests
- `deploy.yml` — GitHub Pages deployment
- Automated testing on push/PR to master
- Workflow dispatch triggers for manual runs
- Scheduled jobs (cron, watchdog)

### Automation
- Data pipeline automation (hourly refresh cron)
- Database backup and recovery automation
- Service restart and recovery automation
- Monitoring and alerting automation
- Dependency update automation (Dependabot)

### Deployment
- GitHub Pages deployment (gh-pages branch)
- Static site deployment to zqmlabs.com
- Docker container deployment and orchestration
- Environment management (staging → production)
- Rollback and recovery procedures

### Code Standards
- `npx tsc --noEmit` must pass with zero errors
- `npm run build` must succeed
- `pytest tests/` must pass (7/7)
- All changes documented in PROJECT_TRACKING.md
- CI/CD changes must pass all existing tests

### XP & Missions
- **CI/CD Contributor** (450 XP): Improve or add CI/CD pipeline
- **Code Commiter** (300 XP): Submit a PR that passes CI
- **Test Contributor** (350 XP): Add tests covering new code

---

# TESTING & QA CONTRIBUTION

Pathway M — Testing & QA Contributor

Testing contributors improve the quality and reliability of Project Volusia by writing tests, verifying fixes, and ensuring all code meets quality standards.

## Pathway Fields

| Field | Description | Type |
|-------|-------------|------|
| **Test Type** | Unit, integration, E2E, security | Select |
| **Component** | Which component was tested? | Free text |
| **Coverage** | Lines/branches covered | Number |
| **Test Result** | Pass/fail/skip | Boolean |
| **CI Status** | Did all CI checks pass? | Boolean |
| **TS Compilation** | Did tsc --noEmit pass? | Boolean |
| **Build Status** | Did npm run build pass? | Boolean |
| **Permission** | Admin/root access needed? | Boolean |

## Testing Areas

### Backend Testing
- FastAPI endpoint tests (pytest)
- Data pipeline tests (verify data freshness, accuracy)
- Gamification scoring tests (verify mission awarding)
- Database integrity tests (WAL, PRAGMAs, foreign keys)
- API response validation tests
- Security tests (HMAC auth, CORS, rate limiting)

### Frontend Testing
- TypeScript compilation tests (`npx tsc --noEmit`)
- Build verification tests (`npm run build`)
- Component rendering tests (React/Vite)
- Responsive design verification
- Cross-browser compatibility testing
- Accessibility audits (ARIA, keyboard nav)

### Infrastructure Testing
- Health check endpoint verification
- Service uptime and availability monitoring
- Security header verification (13 headers)
- TLS/certificate expiration monitoring
- Docker container health checks

### Code Standards
- `npx tsc --noEmit` must pass with zero errors
- `npm run build` must succeed
- `pytest tests/` must pass (7/7)
- All test results documented in PROJECT_TRACKING.md
- 100% test pass rate required for merge

### XP & Missions
- **Test Contributor** (350 XP): Add tests covering new code
- **Code Commiter** (300 XP): Submit a PR that passes CI
- **Review Contributor** (300 XP): Review 5+ PRs from others

---

# DOCUMENTATION & TECHNICAL WRITING CONTRIBUTION

Pathway N — Documentation & Technical Writing Contributor

Documentation contributors improve the Project Volusia knowledge base — README, contributing guides, API docs, architecture docs, and user-facing documentation.

## Pathway Fields

| Field | Description | Type |
|-------|-------------|------|
| **Doc Type** | Readme, API, architecture, guide, example | Select |
| **Target Audience** | Developers, residents, business owners, leaders | Select |
| **File Changed** | Which markdown file? | URL/Path |
| **PR Number** | GitHub PR link | URL |
| **Improvement Type** | New section, fix, enhancement, example | Select |
| **CI Status** | Did the docs build pass? | Boolean |
| **Grammar/Style** | Reviewed for clarity? | Boolean |
| **Permission** | Open source — MIT license | Confirm |

## Documentation Areas

### Code Documentation
- README.md updates and improvements
- CONTRIBUTING.md pathway additions
- API documentation (OpenAPI, endpoint descriptions)
- Architecture documentation (system diagrams)
- Deployment and setup guides
- Makefile and script documentation

### User-Facing Documentation
- zqmlabs.com content updates
- Constituency-specific guides (Business, Resident, Tourist, Movers)
- Data source documentation and attribution
- Gamification system documentation
- Contributing templates and pathways

### Technical Writing
- Methodology and quality framework docs
- Governance charter and guiding principles
- Strategic focus and roadmap documents
- Execution plan and delivery status updates
- CHANGELOG.md maintenance

### Code Standards
- `npx tsc --noEmit` must pass with zero errors
- `npm run build` must succeed
- All docs committed to GitHub repo
- All docs linked from CONTRIBUTING.md
- Documentation changes reviewed by team

### XP & Missions
- **Documentation Contributor** (250 XP): Improve docs, guides, or examples
- **Code Commiter** (300 XP): Submit a PR that passes CI
- **Review Contributor** (300 XP): Review 5+ PRs from others

---

# DIRECT CITIZENRY CONTRIBUTION

Pathway I — Direct Citizenry Contributor

(The simplest possible submission form. If you know what you want to contribute but aren't sure which pathway to use, use this one.)

| Field | Description | Type |
|-------|-------------|------|
| **What do you want to contribute?** | Free text — be as specific as you can | Free text |
| **What's your basis for knowing this?** | Free text — personal experience? saw it happen? documentation? | Free text |
| **What decision or report do you think this relates to?** | Free text — optional | Free text |
| **Anything else you'd like to add?** | Free text — optional | Free text |
| **Contact info (optional)** | Name / Email / Phone — you can submit anonymously | Free text |
| **Date** | YYYY-MM-DD | Date |
