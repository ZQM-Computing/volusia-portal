import { Link } from 'react-router-dom'
import { useEconomicIndicators, useDemographicIndicators, useWeatherIndicators } from '../hooks/useApi'
import { StatCard, Card, SectionTitle, Badge } from '../components/UI'

export function HomePage() {
  const { data: economic, loading: econLoading } = useEconomicIndicators()
  const { data: demographics, loading: demoLoading } = useDemographicIndicators()
  const { data: climate, loading: climateLoading } = useWeatherIndicators()

  const loading = econLoading || demoLoading || climateLoading

  const getIndicator = (items: any[] | null, name: string) => {
    if (!items) return null
    return items.find((i: any) => i.name === name)
  }

  const medianIncome = getIndicator(economic?.indicators, 'median_household_income_acs')
  const unemploymentACS = getIndicator(economic?.indicators, 'unemployment_rate_acs')
  const unemploymentBLS = getIndicator(economic?.indicators, 'unemployment_rate_bls')
  const population = getIndicator(demographics?.indicators, 'total_population_pep')
  const pci = getIndicator(economic?.indicators, 'per_capita_income_bea')
  const employment = getIndicator(economic?.indicators, 'employment_qcew')
  const avgWage = getIndicator(economic?.indicators, 'avg_weekly_wage_qcew')
  const temp = getIndicator(climate?.indicators, 'avg_max_temp_jan2024')

  return (
    <div>
      {/* Hero */}
      <section className="bg-gradient-to-br from-volusia-navy via-volusia-blue to-volusia-teal text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <Badge variant="info">v2.0 — Live Data</Badge>
            <h1 className="text-4xl md:text-5xl font-bold mt-4 mb-6 font-display leading-tight">
              Open Intelligence for Volusia County
            </h1>
            <p className="text-xl text-gray-200 mb-8 leading-relaxed">
              Free, open-source data and analytics for business owners, residents, tourists, and industry movers.
              Real numbers. Real sources. No paywalls.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link to="/data" className="btn-primary no-underline bg-volusia-gold text-volusia-navy hover:bg-yellow-400">
                Explore Data
              </Link>
              <Link to="/maps" className="btn-secondary no-underline border-white text-white hover:bg-white hover:text-volusia-navy">
                View Maps
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Indicators */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {loading ? (
            <>
              <div className="stat-card animate-pulse bg-gray-200 h-24" />
              <div className="stat-card animate-pulse bg-gray-200 h-24" />
              <div className="stat-card animate-pulse bg-gray-200 h-24" />
              <div className="stat-card animate-pulse bg-gray-200 h-24" />
            </>
          ) : (
            <>
              <StatCard
                value={medianIncome ? `$${parseInt(medianIncome.value).toLocaleString()}` : '—'}
                label="Median Household Income"
                change={unemploymentBLS ? parseFloat(unemploymentBLS.value) : undefined}
                changeLabel={unemploymentBLS ? `Unemployment ${unemploymentBLS.value}%` : undefined}
              />
              <StatCard
                value={population ? parseInt(population.value).toLocaleString() : '—'}
                label="Population (2024)"
                change={1.1}
                changeLabel="YoY %"
              />
              <StatCard
                value={employment ? parseInt(employment.value).toLocaleString() : '—'}
                label="Total Employment"
                change={avgWage ? `$${avgWage.value}/wk` : undefined}
                changeLabel={avgWage ? "Avg weekly wage" : undefined}
              />
              <StatCard
                value={pci ? `$${parseInt(pci.value).toLocaleString()}` : '—'}
                label="Per Capita Income"
                change={temp ? `${temp.value}°C` : undefined}
                changeLabel={temp ? "Avg max temp Jan" : undefined}
              />
            </>
          )}
        </div>
      </section>

      {/* Mission */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-3xl font-bold text-volusia-navy mb-4 font-display">
              Technology-Driven Business Growth
            </h2>
            <p className="text-volusia-slate leading-relaxed mb-4">
              Project Volusia accelerates business growth by building and integrating open, scalable
              technology systems that improve commerce, democratize data access, and harness big data
              intelligence.
            </p>
            <p className="text-volusia-slate leading-relaxed mb-6">
              We serve four core constituencies: business owners, residents, tourists, and industry movers.
              Every dataset, every chart, every recommendation is judged by one question: does this make
              life better for the people who live, work, visit, and invest in Volusia County?
            </p>
            <div className="flex flex-wrap gap-2">
              <Badge>Open Source</Badge>
              <Badge>Privacy by Design</Badge>
              <Badge>Measurable Impact</Badge>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Card>
              <h3 className="font-bold text-volusia-navy mb-2">Business</h3>
              <p className="text-sm text-volusia-slate">Market benchmarks, industry mix, and growth signals.</p>
            </Card>
            <Card>
              <h3 className="font-bold text-volusia-navy mb-2">Residents</h3>
              <p className="text-sm text-volusia-slate">Income, demographics, and cost-of-living data.</p>
            </Card>
            <Card>
              <h3 className="font-bold text-volusia-navy mb-2">Tourists</h3>
              <p className="text-sm text-volusia-slate">Conditions, events, and visitor volume trends.</p>
            </Card>
            <Card>
              <h3 className="font-bold text-volusia-navy mb-2">Leaders</h3>
              <p className="text-sm text-volusia-slate">Capital flows, permitting, and workforce analytics.</p>
            </Card>
          </div>
        </div>
      </section>

      {/* Data Sources */}
      <section className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionTitle>Data Sources</SectionTitle>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            <Card>
              <h3 className="font-bold text-volusia-navy mb-2">US Census Bureau</h3>
              <p className="text-sm text-volusia-slate">ACS 5-Year DP03/DP05 profiles and Population Estimates Program.</p>
            </Card>
            <Card>
              <h3 className="font-bold text-volusia-navy mb-2">Bureau of Labor Statistics</h3>
              <p className="text-sm text-volusia-slate">Local Area Unemployment Statistics and Quarterly Census of Employment.</p>
            </Card>
            <Card>
              <h3 className="font-bold text-volusia-navy mb-2">Bureau of Economic Analysis</h3>
              <p className="text-sm text-volusia-slate">CAINC1 regional personal income and employment data.</p>
            </Card>
          </div>
        </div>
      </section>
    </div>
  )
}
