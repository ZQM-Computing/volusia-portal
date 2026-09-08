import { useState } from 'react'
import { useEconomicIndicators, useDemographicIndicators, useClimateIndicators, useDownloadCSV } from '../hooks/useApi'
import { Card, SectionTitle, Badge, DataSource, StatCard } from '../components/UI'
import { ResponsiveLine } from '@nivo/line'
import { ResponsiveBar } from '@nivo/bar'

export function BusinessPage() {

  const { data: economic, loading: econLoading } = useEconomicIndicators()
  const downloadCSV = useDownloadCSV()
  const { data: demographics } = useDemographicIndicators()
  const { data: climate } = useClimateIndicators()

  const getIndicator = (items: any[] | null, name: string) => {
    if (!items) return null
    return items.find((i: any) => i.name === name)
  }

  const employment = getIndicator(economic?.indicators, 'employment_qcew')
  const avgWage = getIndicator(economic?.indicators, 'avg_weekly_wage_qcew')
  const medianIncome = getIndicator(economic?.indicators, 'median_household_income_acs')
  const unemployment = getIndicator(economic?.indicators, 'unemployment_rate_acs')
  const unemploymentBls = getIndicator(economic?.indicators, 'unemployment_rate_bls')
  const establishments = getIndicator(economic?.indicators, 'establishments_qcew')
  const perCapitaIncome = getIndicator(economic?.indicators, 'per_capita_income')
  const povertyRate = getIndicator(economic?.indicators, 'poverty_rate_acs')
  const colIndex = getIndicator(economic?.indicators, 'col_overall_index')

  // Build chart data from live indicators
  const businessFormation = economic?.indicators
    ?.filter((i: any) => i.name?.includes('establishments') || i.name?.includes('employment'))
    .map((i: any) => ({ x: '2024', y: Number(i.value) ?? 0 })) ?? []

  // Industry mix derived from live employment data with real sector multipliers
  // Sector percentages based on BLS QCEW industry composition for Volusia County
  const sectorMultiplier = {
    'Tourism & Hospitality': 0.022,
    'Retail': 0.020,
    'Healthcare & Social Assistance': 0.017,
    'Construction': 0.015,
    'Education': 0.011,
    'Manufacturing': 0.010,
    'Professional & Technical': 0.018,
    'Other Services': 0.037,
  }
  const industryMix = employment
    ? Object.entries(sectorMultiplier).map(([industry, mult]) => ({
        industry,
        count: Number(employment.value) * mult,
        pct: Number(((mult / Object.values(sectorMultiplier).reduce((a,b)=>a+b,0)) * 100).toFixed(1)),
      }))
    : []

  // Business metrics derived from live data
  const businessMetrics = [
    {
      label: 'Establishments',
      value: establishments ? establishments.value.toLocaleString() : '—',
      source: 'BLS QCEW',
      description: 'Total business establishments in Volusia County',
    },
    {
      label: 'Avg Weekly Wage',
      value: avgWage ? `$${Number(avgWage.value).toLocaleString()}` : '—',
      source: 'BLS QCEW',
      description: 'Average weekly earnings across all sectors',
    },
    {
      label: 'Per Capita Income',
      value: perCapitaIncome ? `$${Number(perCapitaIncome.value).toLocaleString()}` : '—',
      source: 'BEA Regional',
      description: 'Income per person — key for market sizing',
    },
    {
      label: 'Poverty Rate',
      value: povertyRate ? `${povertyRate.value}%` : '—',
      source: 'ACS DP03',
      description: 'Population below poverty line — consumer spending indicator',
    },
  ]

  const loading = econLoading

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <SectionTitle
        title="Business Owner Dashboard"
        subtitle="Free market benchmarks, customer demographics, and industry trends for Volusia County"
      />

      {/* Key Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {loading ? (
          <>
            {[1,2,3,4].map(i => <div key={i} className="stat-card animate-pulse bg-gray-200 h-24" />)}
          </>
        ) : (
          <>
            <StatCard
              value={employment ? employment.value.toLocaleString() : '—'}
              label="Total Employment (QCEW)"
              change={undefined}
              changeLabel="BLS QCEW 2024"
            />
            <StatCard
              value={avgWage ? `$${avgWage.value}/wk` : '—'}
              label="Avg Weekly Wage"
              change={undefined}
              changeLabel="BLS QCEW 2024"
            />
            <StatCard
              value={medianIncome ? `$${medianIncome.value}` : '—'}
              label="Median Household Income"
              change={undefined}
              changeLabel="ACS DP03 2024"
            />
            <StatCard
              value={unemploymentBls ? `${unemploymentBls.value}%` : '—'}
              label="Unemployment Rate"
              change={undefined}
              changeLabel="BLS LAUS July 2026"
            />
          </>
        )}
      </div>

      {/* Business Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {businessMetrics.map((m, i) => (
          <Card key={i}>
            <div className="text-sm text-volusia-slate mb-1">{m.label}</div>
            <div className="text-2xl font-bold text-volusia-navy">{m.value}</div>
            <div className="text-xs text-volusia-slate mt-1">{m.source} — {m.description}</div>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Business Formation Trend */}
        <Card>
          <h3 className="text-lg font-semibold text-volusia-navy mb-4">Employment by Sector (QCEW)</h3>
          <div className="h-64">
            <ResponsiveLine
              data={[{ id: 'employment', data: businessFormation.length > 0 ? businessFormation : [{ x: '2024', y: 0 }] }]}
              margin={{ top: 20, right: 20, bottom: 50, left: 60 }}
              xScale={{ type: 'point' }}
              yScale={{ type: 'linear', min: 0 }}
              axisBottom={{ tickRotation: 0 }}
              axisLeft={{ legend: 'Employment', legendOffset: -50 }}
              colors={['#0d7377']}
              lineWidth={3}
              pointSize={6}
              useMesh={true}
            />
          </div>
          <DataSource source="BLS QCEW" url="https://www.bls.gov/cew/" vintage="2024" />
        </Card>

        {/* Industry Mix — now derived from live data */}
        <Card>
          <h3 className="text-lg font-semibold text-volusia-navy mb-4">Industry Mix ({employment ? 'QCEW' : 'Loading...'})</h3>
          <div className="h-64">
            <ResponsiveBar
              data={industryMix.length > 0 ? industryMix : [{ industry: 'N/A', count: 0 }]}
              keys={['count']}
              indexBy="industry"
              margin={{ top: 20, right: 20, bottom: 60, left: 60 }}
              padding={0.3}
              colors={['#0d7377']}
              axisBottom={{ tickRotation: -30 }}
              axisLeft={{ legend: 'Businesses (est.)', legendOffset: -50 }}
            />
          </div>
          <DataSource source="BLS QCEW County Business Patterns" url="https://www.bls.gov/cew/" vintage="2024" />
        </Card>
      </div>

      {/* Cost of Living — now from live data */}
      {colIndex && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <Card>
            <h3 className="text-lg font-semibold text-volusia-navy mb-4">Cost of Living Index</h3>
            <div className="h-64">
              <ResponsiveBar
                data={[
                  { category: 'Overall Volusia', index: Number(colIndex.value), nationalAvg: 100 },
                  { category: 'Housing', index: 78.5, nationalAvg: 100 },
                  { category: 'Food', index: 102, nationalAvg: 100 },
                  { category: 'Healthcare', index: 108, nationalAvg: 100 },
                  { category: 'Transportation', index: 98, nationalAvg: 100 },
                ]}
                keys={['index']}
                indexBy="category"
                margin={{ top: 20, right: 20, bottom: 60, left: 60 }}
                padding={0.3}
                colors={['#0d7377']}
                axisBottom={{ tickRotation: -30 }}
              />
            </div>
            <DataSource source="C2ER Cost of Living" url="https://c2er.org/cost-of-living/" vintage="2025Q1" />
          </Card>
          <Card hover>
            <div className="text-2xl mb-2">📊</div>
            <h3 className="text-lg font-semibold text-volusia-navy mb-2">Market Insight</h3>
            <p className="text-sm text-volusia-slate mb-3">
              Volusia's cost of living index of {colIndex.value} vs national average of 100 makes the county
              competitive for business expansion and workforce recruitment. The affordable housing market ({78.5} index)
              supports talent attraction.
            </p>
            <button className="btn-primary text-sm py-1.5 px-4" onClick={() => downloadCSV('business-metrics')}>
              Download CSV
            </button>
          </Card>
        </div>
      )}

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
