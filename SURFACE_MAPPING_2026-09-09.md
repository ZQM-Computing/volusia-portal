# zqmlabs.com — Surface Mapping Report

**Date:** 2026-09-09
**Auditor:** ZQM Computing
**Tools Used:** nmap, nuclei, curl, httpx, subfinder, Docker inspection

---

## DNS & Subdomain Surface

### Confirmed Subdomains (httpx probe)
| Subdomain | Status | Title | Technology |
|-----------|--------|-------|------------|
| zqmlabs.com | 200 | Project Volusia — Open Intelligence Portal | Cloudflare, HTTP/3 |
| docs.zqmlabs.com | 200 | Project Volusia — Open Intelligence Portal | Cloudflare, HTTP/3 |
| software.zqmlabs.com | 200 | Project Volusia — Open Intelligence Portal | Cloudflare, HTTP/3 |
| api.zqmlabs.com | 200 | Project Volusia — Open Intelligence Portal | Cloudflare, HTTP/3 |

### Not Found / No Response
- admin.zqmlabs.com, app.zqmlabs.com, portal.zqmlabs.com, test.zqmlabs.com, staging.zqmlabs.com, dev.zqmlabs.com, mail.zqmlabs.com, blog.zqmlabs.com, shop.zqmlabs.com, support.zqmlabs.com, community.zqmlabs.com, cdn.zqmlabs.com, static.zqmlabs.com, assets.zqmlabs.com, media.zqmlabs.com, files.zqmlabs.com, uploads.zqmlabs.com — no response

### DNS Infrastructure
- Nameservers: erin.ns.cloudflare.com, henrik.ns.cloudflare.com
- A records: 104.21.71.253, 172.67.173.30
- AAAA records: 2606:4700:3033::6815:47fd, 2606:4700:3031::ac43:ad1e
- Wildcard TLS: Yes (*.zqmlabs.com)
- WAF: Cloudflare DNS WAF detected

---

## Port & Service Surface (nmap)

| Port | State | Service | Notes |
|------|-------|---------|-------|
| 80 | open | Cloudflare proxy | HTTP |
| 443 | open | Cloudflare proxy | HTTPS |
| 8080 | open | Cloudflare proxy | Frontend/nginx |
| 8000 | **filtered** | http-alt | **BLOCKED from internet** |
| 3001-11434 | filtered | various | Internal services |

**Critical:** Only ports 80, 443, and 8080 are reachable from the internet.

---

## HTTP Endpoint Surface

### Confirmed Working (200)
- `/`, `/maps`, `/datasets`, `/diagnostics`, `/refresh`, `/status`, `/meta`, `/verify`, `/unemployment`, `/unemployment/rate`, `/docs/page`

### Confirmed 502 (Cloudflare can't reach backend)
- `/health`, `/indicators`, `/api/indicators`, `/indicators.csv`, `/gamification/leaderboard`, `/gamification/missions`, `/gamification/pulse`

### Confirmed 404
- `/api/indicators`, `/api/map-layers`, `/api/datasets`, `/api/indicators.csv`, `/pulse.json`, `/news.json`

### Incorrect Status
- `/cvb_hotels`, `/download`, `/latest` — return 200 instead of expected 404/503

---

## Technology Stack

### Frontend
React + Vite, TailwindCSS, Nivo, Leaflet, Google Font API, Cloudflare Browser Insights, HTTP/3

### Backend
Python uvicorn (FastAPI), SQLite, gamification module

### Infrastructure
Cloudflare CDN + WAF, Docker containers (frontend, backend, ollama, anythingllm, n8n), nginx (inside frontend container), HSTS enforced (max-age=31536000)

### External Services
NOAA, US Census, BLS, BEA, C2ER, CVB APIs

---

## Security Headers (nuclei)

### Present
strict-transport-security, x-content-type-options, x-frame-options, referrer-policy, Cache-Control, CSP (HTML meta only)

### Missing (6)
content-security-policy (HTTP header), permissions-policy, x-permitted-cross-domain-policies, cross-origin-embedder-policy, cross-origin-opener-policy, cross-origin-resource-policy

---

## GitHub Surface
| Org | Repos | Stars | Issues |
|-----|-------|-------|--------|
| ZQM-Computing | 2 | 0 | 21 open |
| ZQM-Labs | 9 | 0 | 0 open |

---

## Internal Services (filtered/not externally exposed)
ollama:11434, anythingllm:3001, open-webui:3080, n8n:5678-5679, zqm-quantum-api:8891

---

## Summary
- 3 exposed ports (80, 443, 8080) behind Cloudflare WAF
- Port 8000 filtered but exposed in docker-compose.yml
- 6 missing security headers — CSP missing at HTTP level
- 4 confirmed subdomains (zqmlabs.com, docs, software, api)
- Wildcard TLS covers all subdomains
- Non-functional email disclosed on site
- Internal services not externally reachable (good)
- CRITICAL: API completely non-functional externally (502 on all backend routes)
