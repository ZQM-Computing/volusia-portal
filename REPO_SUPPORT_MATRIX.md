# Project Volusia — GitHub Repo Support Matrix

> How each ZQM-Computing and ZQM-Labs repository can support Project Volusia's mission:
> open intelligence, data-driven decision-making, and technology-driven business growth
> for Volusia County, Florida.

**Date:** 2026-09-02
**Orgs:** ZQM-Computing (16 repos), ZQM-Labs (37 repos)
**Total:** 53 repos

---

## 1. DIRECT USE — Ready for Volusia Integration

These repos provide capabilities Project Volusia needs immediately.

| Repo | Org | How It Supports Volusia |
|------|-----|------------------------|
| **volusia-portal** | Computing | **The public face.** React data portal. Already built. |
| **zqm-ai-master** | Computing | FastAPI gateway + Ollama inference. Powers the API backend for the portal — serves economic indicators, dataset queries, and ML predictions. |
| **ollama-bridge** | Labs | Capability-aware model routing. Lets the portal query local LLMs for natural-language data exploration ("Show me tourism trends"). |
| **zqm-local-tools** | Labs | Self-hosted utilities with no paid API keys. Firecrawl/Crawl4AI for web scraping public data sources (BLS, Census, FDOT). |
| **skill-registry** | Computing | Trigger-able skill registry. Can automate data ingestion pipelines — trigger Census API fetches, BLS scrapes, STR parsing on schedule. |
| **mesh-forensics** | Computing | LAN evidence collection. Adapt for data provenance — track every dataset's source, fetch time, transformations immutably. |
| **zqm-intel-platforms** | Labs | OSINT aggregation. Adapt for public data collection — aggregate economic indicators, tourism stats, real estate data from open sources. |
| **zqm-hermes-skills** | Labs | Hermes agent skills. Use for automated data quality checks, anomaly detection, and report generation. |
| **hermes-agent** | Computing | CLI AI agent. Backend automation — scheduled data refreshes, alert generation, report drafting. |
| **swarm** | Computing | Multi-agent orchestration. Coordinate parallel data collection across sources (BLS, Census, BEA, Zillow, FDOT simultaneously). |
| **ZQM-AI-Council** | Labs | Multi-agent deliberation. Use for data quality review — multiple agents cross-validate findings before publication. |
| **Universal-Map** | Labs | Entity/relationship mapping. Map business ecosystems, supply chains, and industry interdependencies in Volusia County. |
| **eye-in-the-sky-mesh** | Computing | Spatial intelligence on 3D globe. Adapt for Volusia County geospatial visualization — overlay economic data on satellite imagery. |
| **omarchy-eye-in-the-sky-mesh** | Computing | Mission-control widget. Adapt as a real-time operations dashboard for portal health, data freshness, and API status. |

---

## 2. ADAPTABLE — Core Tech Applies, Needs Rework

These have the right architecture but need Volusia-specific adaptation.

| Repo | Org | Adaptation Path |
|------|-----|----------------|
| **herc-framework** | Computing | Ethical reasoning framework. Adapt for data ethics — ensure published intelligence meets fairness, privacy, and non-manipulation standards. |
| **zqm-grail-stack** | Computing | Semantic sieve + ontological frameworks. Build a Volusia-specific knowledge graph linking businesses, demographics, tourism, and infrastructure. |
| **nsgi-ors-pipeline** | Computing | Federal opportunity pipeline. Adapt for local grant/opportunity tracking — surface federal/state grants available to Volusia businesses. |
| **zqm-bounty-hub** | Computing | Bug-bounty orchestration. Adapt for data quality bounty — crowdsource error detection in published datasets. |
| **bounty-tools** | Labs | Target intel + token management. Adapt for API key management across data sources (Census, BLS, BEA, Zillow APIs). |
| **zqm-supply-chain-scanner** | Labs | Vulnerability scanning. Adapt for data pipeline monitoring — detect stale datasets, broken scrapers, API changes. |
| **gemini-desktop** | Labs | AI desktop client. Adapt as a Volusia data explorer desktop app for power users who want offline access. |
| **comfy-custom** | Labs | ComfyUI fork. Adapt for data visualization workflows — generate charts, maps, and infographics programmatically. |
| **comfyui-setup** | Labs | ComfyUI bootstrap. Use as a template for automated portal deployment and environment setup. |

---

## 3. INFRASTRUCTURE & DEPLOYMENT

Backend, CI/CD, monitoring, and DevOps that keep the portal running.

| Repo | Org | Role |
|------|-----|------|
| **EaglesNest** | Labs | Deployment automation. Deploy and manage the portal on ZQM-MESH nodes. |
| **Daly** | Labs | PowerShell automation. Windows-side automation for data fetchers running on mesh nodes. |
| **Whitefeather** | Labs | PowerShell tooling. Windows service management for portal components. |
| **dotfiles** | Computing | Dev environment. Standardize developer workstations for portal contributors. |
| **dev-setup** | Labs | Developer bootstrap. Onboard new contributors with pre-configured environments. |
| **scripts** | Labs | Shared automation. Reusable PowerShell/Python scripts for data processing and deployment. |
| **data** | Labs | Internal datasets. Store processed Volusia datasets, analytics intermediates, and pipeline outputs. |
| **logs** | Labs | Operational telemetry. Aggregate logs from portal services, data fetchers, and mesh nodes. |
| **zqm-node-01-indexer** | Labs | Service catalog + MCP. Index portal services, datasets, and API endpoints for discovery. |
| **zqm-node-02-indexer** | Labs | Service discovery. Monitor which data sources are live, stale, or broken. |
| **hermes-config** | Computing | Agent configuration. Configure Hermes for Volusia-specific data tasks and scheduled jobs. |
| **.github** (both) | Both | Org governance. Issue templates, PR templates, security policies for the portal repo. |

---

## 4. SECURITY & COMPLIANCE

Ensure the portal meets security, privacy, and compliance standards.

| Repo | Org | Role |
|------|-----|------|
| **zqm-security-policy** | Labs | Enterprise security policies. Define access controls for the portal's API and data layers. |
| **zqm-attestation-toolkit** | Labs | Windows attestation. Verify mesh nodes serving the portal are compliant and untampered. |
| **zqm-attestation-toolkit-clean** | Labs | Clean attestation toolkit. Hardened version for production portal nodes. |
| **zqm-attestation-briefs** | Labs | Compliance documentation. Document the portal's security posture for public transparency. |
| **zqm-shield** | Labs | Endpoint security. Protect portal infrastructure from attacks. |
| **zqm-sword** | Labs | Penetration testing. Regularly test the portal for vulnerabilities. |
| **zqm-public-tools** | Labs | Open-source security tools. Harden the portal's nginx, Docker, and React stack. |
| **awesome-windows-attestation** | Labs | Curated DFIR resources. Reference for incident response if the portal is compromised. |
| **pqc-readiness-toolkit** | Labs | Post-quantum crypto. Future-proof portal encryption and data integrity. |
| **zqm-auth** | Labs | Auth toolkit. Manage API keys, tokens, and access for data sources and portal admins. |
| **zqm-localhost-findings** | Labs | Local security assessment. Audit the portal's runtime environment. |

---

## 5. KNOWLEDGE & REFERENCE

Documentation, methodologies, and research that inform portal content.

| Repo | Org | Role |
|------|-----|------|
| **wiki** | Labs | Knowledge base. Store Volusia research findings, methodology docs, and data dictionaries. |
| **mesh-forensics** | Computing | Forensic methodology. Adapt for data audit trails — prove dataset integrity to stakeholders. |
| **hermes** | Computing | Hermes runtime. Backend agent for automated data processing and report generation. |

---

## 6. STALE / UNCLEAR — Review for Archival

These repos have no description, unclear purpose, or appear abandoned.

| Repo | Org | Last Updated | Recommendation |
|------|-----|-------------|----------------|
| **Quick-Bot-Ledger** | Labs | 2026-08-24 | No description. Investigate or archive. |
| **zqm-workstage2** | Labs | 2026-08-08 | Default branch is `chore/add-pyproject-readme`. Stale. Archive. |

---

## 7. INTEGRATION ARCHITECTURE

```
                    ┌─────────────────────────────────────┐
                    │        volusia-portal (PUBLIC)       │
                    │   React + Vite + Tailwind + Nivo     │
                    │   Leaflet maps, 7 constituency pages  │
                    └──────────────┬──────────────────────┘
                                   │ REST API
                    ┌──────────────▼──────────────────────┐
                    │      zqm-ai-master (PRIVATE)         │
                    │   FastAPI gateway, Ollama inference  │
                    │   Dataset serving, predictions       │
                    └──────────────┬──────────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
┌─────────▼────────┐  ┌───────────▼──────────┐  ┌─────────▼────────┐
│  swarm           │  │  skill-registry      │  │  ollama-bridge   │
│  Multi-agent     │  │  Scheduled data      │  │  LLM routing     │
│  orchestration   │  │  ingestion triggers  │  │  for NL queries  │
└─────────┬────────┘  └───────────┬──────────┘  └──────────────────┘
          │                        │
          └────────────┬───────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
┌───▼───┐  ┌──────────▼──────────┐  ┌───▼──────────────────┐
│ zqm-  │  │  zqm-local-tools    │  │  zqm-intel-platforms │
│ local │  │  Firecrawl/Crawl4AI │  │  OSINT aggregation   │
│ tools │  │  for web scraping   │  │  Public data sources │
└───────┘  └─────────────────────┘  └──────────────────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
    ┌─────▼─────┐ ┌───▼───┐ ┌─────▼─────┐
    │ BLS LAUS  │ │Census │ │ FDOT      │
    │ QCEW      │ │ ACS   │ │ Zillow    │
    │ BEA CAINC │ │ PEP   │ │ STR       │
    └───────────┘ └───────┘ └───────────┘
```

---

## 8. RECOMMENDED INTEGRATION PRIORITY

### Phase 1 — Foundation (Q4 2026)
1. **zqm-ai-master** → API backend for portal
2. **skill-registry** → Scheduled data ingestion
3. **EaglesNest** → Deploy portal on mesh node
4. **zqm-local-tools** → Web scraping for public data sources

### Phase 2 — Access (2027 Q1-Q2)
5. **ollama-bridge** → Natural language data queries
6. **swarm** → Parallel data collection
7. **zqm-intel-platforms** → OSINT aggregation
8. **mesh-forensics** → Data provenance tracking

### Phase 3 — Maturity (2027 Q3-Q4)
9. **ZQM-AI-Council** → Multi-agent data quality review
10. **Universal-Map** → Business ecosystem mapping
11. **eye-in-the-sky-mesh** → Geospatial visualization
12. **herc-framework** → Data ethics enforcement

### Phase 4 — Institutionalization (2028+)
13. **zqm-security-policy** → Security hardening
14. **zqm-attestation-toolkit** → Node attestation
15. **pqc-readiness-toolkit** → Post-quantum readiness
16. **wiki** → Public knowledge base

---

## 9. SUMMARY

| Category | Count | % of Estate |
|----------|-------|-------------|
| Direct Use | 13 | 25% |
| Adaptable | 9 | 17% |
| Infrastructure | 12 | 23% |
| Security & Compliance | 11 | 21% |
| Knowledge & Reference | 3 | 6% |
| Stale/Unclear | 2 | 4% |
| **volusia-portal (the project itself)** | **1** | **2%** |
| **Total** | **52 + portal** | **100%** |

**Bottom line:** 87% of the ZQM GitHub estate (46 of 53 repos) can directly or indirectly support Project Volusia. The remaining 4% (2 repos) are candidates for archival.

---

Document owner: Project Volusia Leadership
Related: MISSION_STATEMENT.md, Q4_2026_EXECUTION_PLAN.md, TIMELINE_AND_ROADMAP.md
