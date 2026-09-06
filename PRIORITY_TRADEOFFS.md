# PRIORITY TRADEOFFS — PROJECT VOLUSIA
# Phase 1 Foundation Deliverable
# Date: 2026-09-03 | Version: 1.0
# Classification: Internal Strategic Document

---

## 1. PURPOSE

This document captures the explicit tradeoffs made during Phase 1 planning —
what we chose to do, what we chose NOT to do, and why. It prevents future
confusion about why certain paths were taken and others deferred.

Every tradeoff here is reversible, but reversing it should be a deliberate
decision, not an accident of forgetting why we chose the way we did.

---

## 2. THE TRADEOFFS

### 2.1 MINIMAL VIABLE PORTAL OVER PERFECT PORTAL

CHOSEN: A baseline portal showing 3-5 real economic indicators, sourced and cited.
NOT CHOSEN: A polished dashboard with charts, maps, time-series, full UX.
WHY: December 2, 2026 review needs real deliverables, not mockups.
      We can build on a working foundation. We cannot build on a plan.
RISK: The MVP is ugly and limited. Stakeholders may judge the project by its
      appearance before they understand its potential.
MITIGATION: Every indicator is real, cited, and refreshable. That credibility
             matters more than visual polish in Phase 1.

### 2.2 OPEN-SOURCE FIRST, PROPRIETARY LATER (IF EVER)

CHOSEN: All tools and data published in open form by default.
NOT CHOSEN: Proprietary gatekeeping of high-value tools or data for revenue.
WHY: The charter commits to open by default. Trust comes from transparency.
      Revenue models (if any) will be built on services, not data lock-in.
RISK: Someone may take our open tools and compete with us. Or take credit.
MITIGATION: Speed and quality of execution. Being first and best matters more
            than being exclusive. Attribution is built into every tool.

### 2.3 BROAD SOURCE AUDIT OVER DEEP SINGLE-SOURCE ANALYSIS

CHOSEN: Audit all 10 DATA_CATALOG.md categories with per-source status.
NOT CHOSEN: Deep-dive into 2-3 categories and ignore the rest.
WHY: Phase 1 is foundation. We need to know what we have and what we're missing
      before we can prioritize build efforts. A partial audit is a biased audit.
RISK: Surface-level understanding of many sources may miss nuances.
MITIGATION: The audit records confidence levels and known gaps. We can go deep
            on specific sources in Phase 2 when we know which ones matter most.

### 2.4 STAKEHOLDER INTERVIEWS (QUALITATIVE) BEFORE DASHBOARDS (QUANTITATIVE)

CHOSEN: Begin stakeholder interviews in Q4 alongside data audit.
NOT CHOSEN: Wait until we have dashboards built, then interview stakeholders
            about what they see.
WHY: Stakeholder input must shape what we build, not just react to what we
      assumed to build. Starting with interviews tests our charter assumptions.
RISR: Interviews without anything to show may feel abstract to stakeholders.
MITIGATION: The interview guide includes concrete prompts ("what would a free
             market dashboard need to contain for you to actually use it?").

### 2.5 HUMAN REVIEW OVER AGENT PUBLICATION

CHOSEN: AI agents produce drafts and monitoring; humans review before publication.
NOT CHOSEN: Fully autonomous AI publishing to the public portal.
WHY: The charter commits to "verifiable, human-reviewed intelligence." AI is an
      amplifier, not an author. Untested AI output is a liability.
RISK: Bottleneck — human review may slow publication if the team is small.
MITIGATION: Structured contribution pathways (see AGENTIC_CONTRIBUTION_STRATEGY.md)
            make review efficient. Routine submissions (data source additions)
            get fast-tracked; material claims get full review.

### 2.6 CACHED DATA OVER MISSING DATA

CHOSEN: When live API fetches fail, fall back to cached CSV/JSON data shipped
      with the codebase.
NOT CHOSEN: Leave indicators blank until live data can be fetched.
WHY: A dashboard with slightly stale but cited data is better than a dashboard
      with gaps. Stakeholders see the structure and can verify the source.
RISK: Cached data may be mistaken for live data if not properly labeled.
MITIGATION: Every cached indicator is labeled "CACHED" in its vintage field.
            The refresh pipeline replaces cached data with live data automatically
            when the API becomes available.

---

## 3. TRADEOFFS DEFERRED TO LATER PHASES

These are NOT made now. They will be revisited in Phase 2 (Access) or Phase 3 (Maturity):

- Regional integration with Orlando, Titusville, Palm Coast, state agencies
- Predictive models and ML forecasting (too early — need more data history first)
- Monetization strategy (Phase 1 is build-foundation; revenue comes after value)
- Proprietary data partnerships (open-first; proprietary only if no public equivalent exists)
- Full-text search on the portal (v2.0 feature after baseline exists)

---

## 4. HOW TO REVERSE A TRADEOFF

Any tradeoff in this document can be revisited at a quarterly review by:

1. Stating the new information or circumstance that justifies reconsideration
2. Proposing the alternative approach
3. Assessing the cost of reversing (what breaks? what is lost?)
4. Decision at the appropriate governance tier (see PROJECT_VOLUSIA_GOV.md)

---

Document owner: Alex Zelenski / Project Volusia Leadership
Related: Q4_2026_EXECUTION_PLAN.md, PROJECT_VOLUSIA_GOV.md, MISSION_STATEMENT.md
Next review: 2026-12-02
