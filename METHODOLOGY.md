ANALYSIS METHODOLOGY — PROJECT VOLUSIA
=======================================
Version: 1.0 | Date: 2026-09-03
Owner: Project Volusia Methodologist
Classification: Internal — Public-Facing Standard

---

1. PURPOSE
==========

This document defines the analytical methodology for Project Volusia — the
standards every research product, data analysis, and intelligence brief must
meet before entering a public-facing report.

It ensures that every number we publish, every chart we draw, and every
recommendation we make is:

  - Reproducible (same data + method = same result)
  - Falsifiable (we know what would prove us wrong)
  - Transparent (sources, methods, and limitations are stated)
  - Honest (uncertainty is reported, not hidden)

---

2. EVIDENCE TIER SYSTEM
==========================

2.1 TIERS
----------
Every piece of evidence entering the Project Volusia knowledge base is
assigned a tier. The tier determines how it can be used.

  TIER 1 — CAUSAL
    Randomized controlled trials, natural experiments with strong
    identification, instrumental variables, regression discontinuity.
    Use: Causal claims ("X causes Y"). Material business/policy decisions.

  TIER 2 — REPRESENTATIVE
    Representative panel data, well-designed surveys with documented sampling,
    behavioral logs from administrative sources (BLS QCEW, Census ACS).
    Use: Reliable descriptive claims ("Y% of X is Z"). Trend analysis.

  TIER 3 — DIRECTIONAL
    Expert interviews, structured surveys with known limitations,
    convenience samples with documented methodology.
    Use: Hypothesis generation ("The pattern suggests X"). Strategic context.

  TIER 4 — ILLUSTRATIVE
    Anecdotes, social media signals, case studies, non-representative
    reviews.
    Use: Context and color ("Some residents report X"). NOT for
    quantitative claims.

2.2 RULES
----------
  - Material decisions require Tier 1 or 2 evidence.
  - Tier 3 is directional only — never the sole basis for a KPI.
  - Tier 4 is illustrative only — never used for quantitative claims.
  - When tiers conflict, the higher tier wins. Disagreements are resolved
    by the Methodologist.

---

3. DESCRIPTIVE ANALYSIS
========================

3.1 PURPOSE
------------
Describe what IS happening — no causal claims, no predictions.

3.2 REQUIRED ELEMENTS
----------------------
  - Point estimate with confidence interval or margin of error
  - Time period covered
  - Source citation (including vintage)
  - Sample size / population covered
  - Any transformations applied (inflation adjustment, seasonal adjustment,
    smoothing)

3.3 EXAMPLE (GOOD)
-------------------
  "Volusia County's July 2024 population was 602,772 (Census PEP, vintage
   2024, 95% CI ±1.2%). This is an increase of 4,790 (0.8%) from 2023."

3.4 EXAMPLE (BAD)
------------------
  "Volusia County has ~600K people and is growing." — No source, no vintage,
  no uncertainty.

---

4. CORRELATION ANALYSIS
========================

4.1 PURPOSE
------------
Describe whether two variables move together — still no causal claim.

4.2 REQUIRED ELEMENTS
----------------------
  - Pearson or Spearman correlation coefficient with p-value
  - Sample size
  - Time period
  - Scatterplot OR joint distribution (when possible)
  - Statement: "Correlation does not imply causation."

4.3 RULES
----------
  - N < 30 requires explicit caution.
  - Spurious correlation must be ruled out via theory or triangulation.
  - Lagged effects should be tested (Granger causality as exploratory only).

---

5. TREND ANALYSIS
==================

5.1 PURPOSE
------------
Identify and project patterns over time.

5.2 METHODS
------------
  - Time series decomposition (trend + seasonality + residual)
  - Moving averages (3, 6, or 12 month, stated explicitly)
  - Linear or logistic regression for trend projection (with stated
    assumptions)

5.3 REQUIRED ELEMENTS
----------------------
  - Historical depth (at least 5 years, ideally 10+)
  - Seasonal adjustment method (stated)
  - Trend line with confidence band
  - Explicit statement of assumptions for any projection

5.4 PROJECTION RULES
----------------------
  - Projections beyond 1 year require stated confidence intervals.
  - Projections beyond 3 years are labeled "scenario, not forecast."
  - Scenario analysis (best/base/worst case) is the standard for 3+ year
    projections.

---

6. COMPARATIVE ANALYSIS
========================

6.1 PURPOSE
------------
Benchmark Volusia County against peers (other counties, MSAs, state,
national).

6.2 REQUIRED ELEMENTS
----------------------
  - Peer selection criteria (stated — e.g., population, region, industry mix)
  - Time period matched across all geographies
  - Metrics adjusted for comparability (e.g., per capita, purchasing power)
  - Caveats on data source differences

6.3 PEER COUNTIES (DEFAULT)
----------------------------
Unless otherwise specified, Volusia County comparisons use:

  PRIMARY: Brevard, Flagler, Lake, Orange, Seminole (Central Florida peers)
  SECONDARY: Marion, Polk, St. Johns (Florida MSA peers)
  ASPIRATIONAL: Horry SC, Chatham GA, Boone KY (similar tourism/economy
                mix, similar population)

---

7. QUALITATIVE ANALYSIS
========================

7.1 PURPOSE
------------
Understand WHY patterns exist, not just WHAT is happening.

7.2 METHODS
------------
  - Semi-structured interviews (see STAKEHOLDER_INTERVIEW_GUIDE.md)
  - Focus groups (documented sampling, facilitator, protocol)
  - Document analysis (public records, meeting minutes, media)
  - Ethnographic observation (for tourism/tourist behavior studies)

7.3 REQUIRED ELEMENTS
----------------------
  - Sampling method and response rate
  - Interview/focus group protocol (or link to it)
  - Distinction between themes and quotes
  - Differentiation between opinion and fact in notes

7.4 THEME CODING
-----------------
  - Themes are identified from at least 3 independent sources before being
    reported as "pattern."
  - Deviant cases are reported (not just confirming evidence).
  - Theme counts are directional ("majority reported X") — never precise
    percentages from small samples.

---

8. MACHINE LEARNING
=====================

8.1 PURPOSE
------------
Forecast, classify, or detect anomalies in Volusia County data.

8.2 APPROVED METHODS
---------------------
  - Linear/logistic regression
  - Decision trees (interpretable only)
  - Time series forecasting (ARIMA, exponential smoothing)
  - Clustering (for segmentation, with manual labeling)

8.3 REQUIREMENTS
-----------------
  - Training/test split (80/20 minimum)
  - Out-of-sample validation
  - Cross-validation for small datasets
  - Feature importance documented
  - Model limitations stated explicitly
  - Human review before any public claim

8.4 PROHIBITED
---------------
  - Black-box models for material decisions (no deep neural nets without
    interpretation)
  - Training on the entire dataset without held-out validation
  - Using models trained on other geographies without Volusia-specific
    calibration

---

9. DATA QUALITY STANDARDS
===========================

9.1 SOURCE DOCUMENTATION
--------------------------
Every dataset must record:
  - Source name and publisher
  - URL or access method
  - Date accessed
  - Vintage (when the data was published, NOT when accessed)
  - Known limitations

9.2 MISSING DATA
-----------------
  - Missing data is NEVER imputed without documentation.
  - If imputation is used, the method and fraction imputed are stated.
  - Columns with >20% missing are flagged in every report.

9.3 OUTLIER DETECTION
----------------------
  - Values beyond 3 standard deviations are flagged.
  - Outliers are investigated (not silently removed).
  - If an outlier is real, it is reported. If it is a data error, it is
    corrected and the correction is documented.

9.4 INFLATION ADJUSTMENT
-------------------------
  - All dollar amounts over 2 years apart are inflation-adjusted.
  - CPI-U (All Items, U.S. City Average) is the default deflator.
  - Adjustment method is stated (e.g., "2024 dollars, CPI-U deflated").

---

10. REPORTING STANDARDS
=========================

10.1 CITATION FORMAT
---------------------
  Every number cites its source:
    "Volusia County unemployment was 4.6% (BLS LAUS, LAUCN12127000000003,
     July 2026, preliminary)."

10.2 UNCERTAINTY LANGUAGE
--------------------------
  - Point estimates: ± margin of error
  - Projections: "We expect X, with a range of Y-Z under [assumptions]."
  - Correlation: "X and Y are correlated (r=0.7, p<0.01, n=24), but
    this does not establish causation."
  - Small samples: "Based on [N] interviews/stakeholders..."

10.3 VISUAL STANDARDS
----------------------
  - Y-axis starts at 0 for bar charts (unless clearly labeled otherwise)
  - Color-blind accessible palettes (Wong palette or similar)
  - All charts have: title, source, vintage, axis labels
  - Interactive charts include the underlying data as a download link
  - Maps use EPSG:4269 (NAD83) or EPSG:2236 (Florida State Plane East)

10.4 READING LEVEL
-------------------
  Public-facing summaries are written at an 8th-grade reading level.
  Technical appendices are exempt from this standard.

---

11. REPRODUCIBILITY CHECKLIST
==============================

Before any analysis enters a public-facing report, the analyst answers:

  [ ] Data sources are documented and accessible
  [ ] Code is version-controlled and runnable
  [ ] Methodology is stated (which section of this document applies)
  [ ] Uncertainty is reported honestly
  [ ] Limitations are stated explicitly
  [ ] Results are reproducible by an independent analyst
  [ ] Charts meet visual standards
  [ ] Report Lead has signed off

---

12. REVIEW CADENCE
===================

  - Methodology document: Quarterly review (at quarterly formal review)
  - Analysis methods: Before each new analysis project
  - Data sources: At each refresh cycle
  - Report standards: At each quarterly briefing

---

Document owner: Project Volusia Methodologist
Related: COMMERCE_RESEARCH_RELIABILITY.md, AGENTIC_CONTRIBUTION_STRATEGY.md
Next review: 2026-12-02
