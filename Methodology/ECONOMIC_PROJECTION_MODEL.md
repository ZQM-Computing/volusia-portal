# Economic Projection Model: Project Volusia

## Model Overview
This document describes the projection methodology for forecasting Volusia County's economic trends.

---

## Model Assumptions

### Macroeconomic Factors
- Regional GDP growth: Florida average ± 0.5%
- Consumer confidence: Moderate growth trajectory
- Housing market: Stable with seasonal variation
- Tourism: Resilient but weather-dependent

### Sector-Specific Factors
- **Healthcare**: Aging population, medical tech adoption
- **Education**: State funding trends, enrollment changes
- **Government**: Tax base stability, federal funding
- **Aviation**: Training demand, industry expansion
- **Retail**: E-commerce evolution, consumer spending

---

## Projection Methods

### 1. Employer Count Trends
**Method**: Exponential smoothing with sector weighting
**Formula**: E(t) = α·E(obs) + (1-α)·E(t-1)
**Alpha**: 0.3 (balanced responsiveness)
**Baseline**: 43 employers Q4 2026

### 2. Job Posting Velocity
**Method**: Moving average of new postings
**Window**: 90 days
**Baseline**: 2.1 new jobs/week average
**Projection**: Job postings → Employer openings ratio

### 3. Wage Trend Analysis
**Method**: Sector median wage regression
**Factors**: Inflation, cost of living, skill demand
**Baseline**: Sector-specific median wages from data
**Assumption**: Real wage suppression in retail/logistics

### 4. Geographic Expansion
**Method**: New employer probability by city
**Factors**: Commercial vacancy rates, business incentives
**Baseline**: Current employer distribution
**Growth areas**: DeLand corridor, Port Orange commercial zones

---

## Sector Projections (2026-2028)

### High Growth Sectors
1. **Healthcare**
   - Projected employers: +12% annually
   - Job openings: +15% annually
   - Risk: None (essential service)

2. **Aviation**
   - Projected employers: +8% annually
   - Job openings: +10% annually
   - Risk: Industry cycles

3. **Insurance**
   - Projected employers: +5% annually
   - Job openings: +3% annually
   - Risk: Regulatory changes

### Stable Sectors
4. **Education**
   - Projected employers: +2% annually
   - Job openings: +1% annually
   - Risk: Funding cuts

5. **Government**
   - Projected employers: +1% annually
   - Job openings: +0.5% annually
   - Risk: Political cycles

### Declining Sectors
6. **Retail**
   - Projected employers: -3% annually
   - Job openings: -5% annually
   - Risk: E-commerce, saturation

7. **Manufacturing**
   - Projected employers: -2% annually
   - Job openings: -4% annually
   - Risk: Automation, offshoring

---

## Quantitative Projections

### Employer Count Forecast
| Year | Q1 | Q2 | Q3 | Q4 | Trend |
|------|----|----|----|----|-------|
| 2026 | 43 | 45 | 46 | 47 | +9% |
| 2027 | 48 | 49 | 50 | 51 | +8% |
| 2028 | 52 | 53 | 54 | 55 | +7% |

### Job Opening Forecast
| Year | Active | New W/Rate | Risk Adjust |
|------|--------|------------|-------------|
| 2026 | 29 | 2.1/wk | 100% |
| 2027 | 34 | 1.8/wk | 95% |
| 2028 | 38 | 1.5/wk | 90% |

---

## Monte Carlo Sensitivity Analysis

### Key Variables Tested
1. **Employment multiplier**: 0.8-1.2 range
2. **Sector volatility**: ±15% standard deviation
3. **Economic shock**: -10% to +10% impact

### 95% Confidence Intervals
- **Low estimate** (2028): 48 employers, 28 jobs
- **Base estimate** (2028): 55 employers, 38 jobs
- **High estimate** (2028): 62 employers, 52 jobs

---

## Model Limitations

### Known Limitations
1. Small sample size (N=43) limits statistical power
2. Quarterly verification cadence may miss rapid changes
3. External shocks (hurricanes, pandemics) not modeled
4. Inter-employer relationships not captured

### Mitigation Strategies
- Monthly job posting monitoring
- News sentiment integration
- Historical shock cataloging
- Network analysis development

---

## Model Validation Protocol

### Monthly Checks
- [ ] New employer detection
- [ ] Closure verification
- [ ] Wage data refresh
- [ ] Sector classification review

### Quarterly Reviews
- [ ] Projection accuracy assessment
- [ ] Model parameter tuning
- [ ] Methodology documentation
- [ ] Stakeholder feedback integration

---

*Model v1.0 | September 2026*
