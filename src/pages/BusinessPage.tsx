import { indicators } from '../data/sampleData'
import { Card, SectionTitle, Badge, DataSource } from '../components/UI'
import { ResponsiveLine } from '@nivo/line'
import { ResponsiveBar } from '@nivo/bar'

export function BusinessPage() {
  const businessIndicators = indicators.filter((i) =>
    ['economic', 'real_estate'].includes(i.category)
  )

  const industryMix = [
    { industry: 'Tourism', count: 4200, pct: 14.7 },
    { industry: 'Retail', count: 3800, pct: 13.3 },
    { industry: 'Healthcare', count: 3200, pct: 11.2 },
    { industry: 'Construction', count: 2900, pct: 10.2 },
    { industry: 'Education', count: 2100, pct: 7.4 },
    { industry: 'Manufacturing', count: 1800, pct: 6.3 },
    { industry: 'Professional', count: 3400, pct: 11.9 },
    { industry: 'Other', count: 7100, pct: 24.9 },
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <SectionTitle
        title="Business Owner Dashboard"
        subtitle="Free market benchmarks, customer demographics, and industry trends for Volusia County"
      />

      {/* Key Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {businessIndicators.slice(0, 4).map((ind) => (
          <div key={ind.id} className="stat-card">
            <div className="stat-value">{typeof ind.value === 'number' ? ind.value.toLocaleString() : ind.value}</div>
            <div className="stat-label">{ind.name}</div>
            {ind.change && (
              <div className={`text-xs font-medium mt-1 ${ind.change > 0 ? 'text-green-600' : 'text-red-600'}`}>
                {ind.change > 0 ? '↑' : '↓'} {Math.abs(ind.change)} {ind.changeLabel}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Business Formation Trend */}
        <Card>
          <h3 className="text-lg font-semibold text-volusia-navy mb-4">Business Formation Trend</h3>
          <div className="h-64">
            <ResponsiveLine
              data={[
                {
                  id: 'licenses',
                  data: [
                    { x: '2022', y: 24800 },
                    { x: '2023', y: 25900 },
                    { x: '2024', y: 26800 },
                    { x: '2025', y: 27400 },
                    { x: '2026', y: 28456 },
                  ],
                },
              ]}
              margin={{ top: 20, right: 20, bottom: 50, left: 60 }}
              xScale={{ type: 'point' }}
              yScale={{ type: 'linear', min: 20000, max: 32000 }}
              axisBottom={{ tickRotation: 0 }}
              axisLeft={{ legend: 'Active Licenses', legendOffset: -50 }}
              colors={['#0d7377']}
              lineWidth={3}
              pointSize={6}
              useMesh={true}
            />
          </div>
          <DataSource source="FL DBPR / Volusia County" url="https://www.myfloridalicense.com/" vintage="2026" />
        </Card>

        {/* Industry Mix */}
        <Card>
          <h3 className="text-lg font-semibold text-volusia-navy mb-4">Industry Mix</h3>
          <div className="h-64">
            <ResponsiveBar
              data={industryMix}
              keys={['count']}
              indexBy="industry"
              margin={{ top: 20, right: 20, bottom: 60, left: 60 }}
              padding={0.3}
              colors={['#0d7377']}
              axisBottom={{ tickRotation: -30 }}
              axisLeft={{ legend: 'Businesses', legendOffset: -50 }}
            />
          </div>
          <DataSource source="US Census County Business Patterns" url="https://www.census.gov/programs-surveys/cbp.html" vintage="2024" />
        </Card>
      </div>

      {/* Tools & Resources */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card hover>
          <div className="text-2xl mb-2">📋</div>
          <h3 className="text-lg font-semibold text-volusia-navy mb-2">Market Benchmarking</h3>
          <p className="text-sm text-volusia-slate mb-3">
            Compare your business performance against local industry averages. Revenue, margins, and growth rates by sector.
          </p>
          <button className="btn-primary text-sm py-1.5 px-4">Coming Soon</button>
        </Card>
        <Card hover>
          <div className="text-2xl mb-2">🗺️</div>
          <h3 className="text-lg font-semibold text-volusia-navy mb-2">Location Intelligence</h3>
          <p className="text-sm text-volusia-slate mb-3">
            Analyze foot traffic, demographics, and competitor density for any location in Volusia County.
          </p>
          <button className="btn-primary text-sm py-1.5 px-4">Coming Soon</button>
        </Card>
        <Card hover>
          <div className="text-2xl mb-2">📊</div>
          <h3 className="text-lg font-semibold text-volusia-navy mb-2">Quarterly Briefing</h3>
          <p className="text-sm text-volusia-slate mb-3">
            Subscribe to receive the quarterly economic briefing with the latest business indicators.
          </p>
          <button className="btn-primary text-sm py-1.5 px-4">Subscribe</button>
        </Card>
      </div>
    </div>
  )
}
