# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `/api/indicators/search` — full-text search endpoint
- `/api/indicators/stats` — aggregate statistics across all indicators
- `/api/export/csv` — CSV export endpoint
- `/api/fetch-status` — data pipeline fetch status
- `/api/contributor` — contributor registration
- `/api/gamification/*` — full gamification routes (state, leaderboard, missions, badges, visit)
- `scripts/refresh_v2.py` — refactored data pipeline refresh (23 source types)
- `tests/test_backend.py` — 7 backend integration tests
- `pyproject.toml` — ruff, mypy, pytest tool configuration
- `.pre-commit-config.yaml` — ruff + pre-commit hooks

### Changed
- **BREAKING**: All routes moved under `/api/` prefix
- CORS origins restricted to localhost + zqmlabs.com domains
- Frontend `useApi.ts` rewritten as RxJS multi-driver pattern
- New `useGamification.ts` hook extracted from `useApi.ts`
- Database: root-level `data/volusia.db` is primary; `backend/data/volusia.db` is runtime copy

### Fixed
- BusinessPage.tsx: hardcoded data → API fetch
- GameStats.tsx: hardcoded data → API fetch
- NewsPage.tsx: hardcoded news → API fetch
- GamificationPage.tsx + LeadersPage.tsx: TypeScript leaderboard access errors
- gamification.py: POST body parsing, route prefix consistency, signature fix
- test_backend.py: endpoint paths, import paths
- CI: `|| true` loophole removed, ruff/pytest enforced, secrets scan added
- `.env.example`: removed hardcoded refresh token

### Security
- Removed hardcoded refresh token from `.env.example`
- CORS no longer allows wildcard or non-localhost origins
- `.gitignore`: blocks `.env`, `*.log`, `data/api_keys.json`, DB files, pyc files
- `data/api_keys.json` and DB files removed from git tracking

## [3.0.0] — 2026-09-09

### Added
- Full gamification system: XP, levels, badges, leaderboards, missions
- 48 economic indicators across 11 categories
- CVB hotel directory, stakeholder listings
- Interactive map with 18 layers
- Docker Compose + Dockerfile.backend with HEALTHCHECK

### Changed
- Frontend: React 18 + Vite + Tailwind CSS + Nivo + Leaflet
- Backend: FastAPI 0.115 + SQLite

### Fixed
- Data pipeline refresh script (refresh_and_diagnose.sh → refresh_v2.py)
- CORS configuration
- Docker HEALTHCHECK (python urllib)

## [2.0.0] — 2026-09-08

### Added
- Initial full release
- 28 economic indicators
- 8 page routes
- Basic CI (frontend lint + build)

## [1.0.0] — 2026-09-07

### Added
- Project scaffold: FastAPI backend + React frontend
- Core indicator endpoints
- Basic UI pages
