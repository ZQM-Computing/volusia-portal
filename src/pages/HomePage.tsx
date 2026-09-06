import { useState, useEffect } from 'react'
import { useEconomicIndicators, useDemographicIndicators, useClimateIndicators, useDatasets, useIndicator, useMapLayers } from '../hooks/useApi'
import { useGamification, useGamificationStats } from '../hooks/useGamification'
import { StatCard, Card, SectionTitle, Badge } from '../components/UI'
import { ResponsiveLine } from '@nivo/line'
import { ResponsiveBar } from '@nivo/bar'

export function HomePage() {
  const { data: economic, loading: econLoading } = useEconomicIndicators()
  const { data: demographics, loading: demoLoading } = useDemographicIndicators()
  const climate = useClimateIndicators()
  const climateIndicators = climate.data?.indicators ?? climate.data ?? null
  const { data: mapLayers } = useMapLayers()
  const { data: datasets } = useDatasets()
  const { visitPage } = useGamification('anonymous')
  const { stats, totalUsers, avgXp, avgLevel } = useGamificationStats('anonymous')
  const [visitedHero, setVisitedHero] = useState(false)

  useEffect(() => { visitPage('home'); }, [])

  const loading = econLoading || demoLoading || climate.loading

  const getIndicator = (items: any[] | null, name: string) => {
    if (!items) return null
    return items.find((i: any) => i.name === name)
  }

  const medianIncome = getIndicator(economic?.indicators, 'median_household_income_acs')
  const unemploymentACS = getIndicator(economic?.indicators, 'unemployment_rate_acs')
  const unemploymentBLS = getIndicator(economic?.indicators, 'unemployment_rate_bls')
  const population = getIndicator(demographics?.indicators, 'total_population_acs')
  const pci = getIndicator(economic?.indicators, 'per_capita_income_bea')
  const employment = getIndicator(economic?.indicators, 'employment_qcew')
  const avgWage = getIndicator(economic?.indicators, 'avg_weekly_wage_qcew')
  const temp = getIndicator(climateIndicators, 'avg_max_temp')

  const fmtNum = (v: any) => {
    if (v == null) return '—'
    const n = Number(v)
    return isNaN(n) ? String(v) : n.toLocaleString()
  }

  const handleVisit = (page: string) => {
    if (!visitedHero) {
      visitPage(page)
      setVisitedHero(true)
    }
  }

  // Income trend chart data from economic indicators
  const incomeTrendData = economic?.indicators
    ?.filter((i: any) => i.name?.includes('median_income') || i.name?.includes('per_capita_income') || i.name?.includes('personal_income'))
    .map((i: any) => ({ x: i.year ?? '2024', y: Number(i.value) ?? 0 })) ?? []

  const employmentTrendData = economic?.indicators
    ?.filter((i: any) => i.name?.includes('employment') || i.name?.includes('unemployment'))
    .map((i: any) => ({ x: i.year ?? '2024', y: Number(i.value) ?? 0 })) ?? []

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
              <a href="/data" onClick={() => handleVisit('/data')} className="btn-primary no-underline bg-volusia-gold text-volusia-navy hover:bg-yellow-400">
                Explore Data
              </a>
              <a href="/maps" onClick={() => handleVisit('/maps')} className="btn-secondary no-underline border-white text-white hover:bg-white hover:text-volusia-navy">
                View Maps
              </a>
            </div>
            {visitedHero && <Badge variant="success" className="mt-4">🎯 +3 XP earned!</Badge>}
          </div>
        </div>
      </section>

      {/* Featured Indicators */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {loading ? (
            <>
              {[1,2,3,4].map(i => <div key={i} className="stat-card animate-pulse bg-gray-200 h-24" />)}
            </>
          ) : (
            <>
              <StatCard
                value={medianIncome ? `$${fmtNum(medianIncome.value)}` : '—'}
                label="Median Household Income"
                change={unemploymentBLS ? parseFloat(unemploymentBLS.value) : undefined}
                changeLabel={unemploymentBLS ? `Unemployment ${unemploymentBLS.value}%` : undefined}
              />
              <StatCard
                value={population ? fmtNum(population.value) : '—'}
                label="Population (2024)"
                change={undefined}
                changeLabel="Census ACS DP05"
              />
              <StatCard
                value={employment ? fmtNum(employment.value) : '—'}
                label="Total Employment"
                change={avgWage && !isNaN(Number(avgWage.value)) ? Number(avgWage.value) : undefined}
                changeLabel={avgWage ? `Avg wkly $${avgWage.value}` : undefined}
              />
              <StatCard
                value={pci ? `$${fmtNum(pci.value)}` : '—'}
                label="Per Capita Income"
                change={temp && !isNaN(Number(temp.value)) ? Number(temp.value) : undefined}
                changeLabel={temp ? "Avg max temp Jan" : undefined}
              />
            </>
          )}
        </div>
      </section>

      {/* Charts */}
      {!loading && economic?.indicators && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <Card>
              <h3 className="font-bold text-volusia-navy mb-4">Income Trend</h3>
              {incomeTrendData.length > 0 ? (
                <ResponsiveLine
                  data={[{ id: 'Income', data: incomeTrendData }]}
                  margin={{ top: 10, right: 30, bottom: 40, left: 60 }}
                  xScale={{ type: 'point' }}
                  yScale={{ type: 'linear' }}
                  axisTop={null}
                  axisRight={null}
                  theme={{}}
                  lineWidth={3}
                />
              ) : (
                <div className="h-48 flex items-center justify-center text-sm text-gray-400">No trend data available</div>
              )}
            </Card>
            <Card>
              <h3 className="font-bold text-volusia-navy mb-4">Employment & Unemployment</h3>
              {employmentTrendData.length > 0 ? (
                <ResponsiveBar
                  data={employmentTrendData.map((d: any) => ({ x: d.x, y: d.y }))}
                  margin={{ top: 10, right: 30, bottom: 40, left: 60 }}
                />
              ) : (
                <div className="h-48 flex items-center justify-center text-sm text-gray-400">No trend data available</div>
              )}
            </Card>
          </div>
        </section>
      )}

{/* Community Activity */}
      {stats && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-volusia-navy text-white rounded-xl p-8">
            <h2 className="text-2xl font-bold mb-6 font-display">Community Activity</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-volusia-gold">{totalUsers}</div>
                <div className="text-sm text-gray-300 mt-1">Active Users</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-volusia-gold">{Math.round(avgLevel)}</div>
                <div className="text-sm text-gray-300 mt-1">Avg Level</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-volusia-gold">{Math.round(avgXp)}</div>
                <div className="text-sm text-gray-300 mt-1">Avg XP</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-volusia-gold">{stats.total_visits}</div>
                <div className="text-sm text-gray-300 mt-1">Total Visits</div>
              </div>
            </div>
          </div>
        </section>
      )}

{/* Map Preview */}
      {mapLayers && mapLayers.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <SectionTitle title="Live Map Coverage" subtitle={`${mapLayers.length} layers across Volusia County`} />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card hover className="cursor-pointer">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-volusia-teal/20 flex items-center justify-center text-volusia-teal">🗺️</div>
                <div>
                  <div className="font-bold text-volusia-navy">County Boundary</div>
                  <div className="text-xs text-volusia-slate">MultiPolygon — Full coverage</div>
                </div>
              </div>
            </Card>
            <Card hover className="cursor-pointer">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-volusia-blue/20 flex items-center justify-center text-volusia-blue">🏖️</div>
                <div>
                  <div className="font-bold text-volusia-navy">Beach Access Points</div>
                  <div className="text-xs text-volusia-slate">{mapLayers.filter((l: any) => l.category === 'Beach Access Points').length} points</div>
                </div>
              </div>
            </Card>
            <Card hover className="cursor-pointer">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-volusia-purple/20 flex items-center justify-center text-volusia-purple">🌊</div>
                <div>
                  <div className="font-bold text-volusia-navy">Water Bodies</div>
                  <div className="text-xs text-volusia-slate">{mapLayers.filter((l: any) => l.category === 'Water Bodies').length} features</div>
                </div>
              </div>
            </Card>
          </div>
        </section>
      )}

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
          <SectionTitle title="Data Sources" />
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
          <div className="mt-8 flex flex-wrap gap-4">
            <Badge variant="info">📊 {datasets?.length ?? 0} Datasets Available</Badge>
            <Badge variant="success">✅ 28+ Live Indicators</Badge>
            <Badge variant="warning">🔄 Hourly Auto-Refresh</Badge>
          </div>
        </div>
      </section>

      {/* Human README */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-white rounded-xl border border-gray-200 p-8">
          <h2 className="text-3xl font-bold text-volusia-navy mb-4 font-display">📖 Human README</h2>
          <p className="text-volusia-slate leading-relaxed mb-6">
            Welcome to Project Volusia. This portal provides open, free data for everyone.
            Browse indicators, explore maps, and discover Volusia County's economic landscape.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div className="p-4 bg-gray-50 rounded-lg">
              <h3 className="font-bold text-volusia-navy mb-2">Getting Started</h3>
              <p className="text-sm text-volusia-slate">1. Browse <a href="/data" className="text-volusia-teal underline">Data Explorer</a> for indicators</p>
              <p className="text-sm text-volusia-slate">2. Explore <a href="/maps" className="text-volusia-teal underline">Interactive Maps</a> for geography</p>
              <p className="text-sm text-volusia-slate">3. Check <a href="/business" className="text-volusia-teal underline">Business</a> for economic data</p>
              <p className="text-sm text-volusia-slate">4. Visit <a href="/tourists" className="text-volusia-teal underline">Tourists</a> for visitor insights</p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <h3 className="font-bold text-volusia-navy mb-2">Features</h3>
              <p className="text-sm text-volusia-slate">✅ 28+ Live Indicators</p>
              <p className="text-sm text-volusia-slate">✅ 18 Map Layers with GeoJSON</p>
              <p className="text-sm text-volusia-slate">✅ Hourly Auto-Refresh</p>
              <p className="text-sm text-volusia-slate">✅ Gamification with XP Tracking</p>
              <p className="text-sm text-volusia-slate">✅ Real CVB Hotel Data</p>
              <p className="text-sm text-volusia-slate">✅ Open Source (MIT License)</p>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <Badge variant="info">MIT License</Badge>
            <Badge variant="success">Free & Open</Badge>
            <Badge variant="warning">No Paywall</Badge>
            <Badge variant="default">Community Driven</Badge>
          </div>
        </div>
      </section>

      {/* AI Agent README */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-volusia-navy text-white rounded-xl p-8">
          <h2 className="text-3xl font-bold mb-4 font-display">🤖 AI Agent README</h2>
          <p className="text-gray-300 leading-relaxed mb-6">
            This portal provides structured, machine-readable data for AI agents and automated systems.
            All endpoints return JSON. All indicators are normalized with consistent naming.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-4 bg-gray-800 rounded-lg">
              <h3 className="font-bold text-volusia-gold mb-2">API Endpoints</h3>
              <code className="text-xs text-gray-300 block mb-1">GET /api/indicators — All indicators</code>
              <code className="text-xs text-gray-300 block mb-1">GET /api/indicators?category=Economic</code>
              <code className="text-xs text-gray-300 block mb-1">GET /api/indicators/</code><code></code>
              <code className="text-xs text-gray-300 block mb-1">GET /api/datasets — Dataset catalog</code>
              <code className="text-xs text-gray-300 block mb-1">GET /api/map-layers — GeoJSON layers</code>
              <code className="text-xs text-gray-300 block mb-1">GET /api/indicators.csv — Download CSV</code>
            </div>
            <div className="p-4 bg-gray-800 rounded-lg">
              <h3 className="font-bold text-volusia-gold mb-2">Gamification API</h3>
              <code className="text-xs text-gray-300 block mb-1">GET /api/gamification/profile/</code><code></code>
              <code className="text-xs text-gray-300 block mb-1">POST /api/gamification/visit/</code><code></code>
              <code className="text-xs text-gray-300 block mb-1">POST /api/gamification/xp/</code><code></code>
              <code className="text-xs text-gray-300 block mb-1">GET /api/gamification/leaderboard</code>
              <code className="text-xs text-gray-300 block mb-1">GET /api/gamification/stats/</code><code></code>
              <code className="text-xs text-gray-300 block mb-1">GET /api/gamification/achievements/</code><code></code>
            </div>
          </div>
          <div className="mt-6 p-4 bg-gray-800 rounded-lg">
            <h3 className="font-bold text-volusia-gold mb-2">Data Schema</h3>
            <code className="text-xs text-gray-300 block">indicators: [&#123;name, value, unit, category, source, source_url, vintage, description&#125;]</code>
            <code className="text-xs text-gray-300 block">map_layers: [&#123;id, name, category, description, source, format, url, geometry&#125;]</code>
            <code className="text-xs text-gray-300 block">datasets: [&#123;id, source, content, fetched_at&#125;]</code>
            <code className="text-xs text-gray-300 block">gamification: [&#123;user_id, total_xp, level, streak_days, visit_count, last_visit, achievements&#125;]</code>
          </div>
        </div>
      </section>
    </div>
  )
}