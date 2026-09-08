import { useState, useEffect } from 'react'
import { useDemographicIndicators, useEconomicIndicators, useClimateIndicators, useDownloadCSV } from '../hooks/useApi'
import { Card, SectionTitle, Badge, DataSource, StatCard } from '../components/UI'
import { ResponsiveLine } from '@nivo/line'

export function ResidentsPage() {
  

  const { data: demographics, loading: demoLoading } = useDemographicIndicators()
  const { data: economic, loading: econLoading } = useEconomicIndicators()

  const getIndicator = (items: any[] | null, name: string) => {
    if (!items) return null
    return items.find((i: any) => i.name === name)
  }

  const medianIncome = getIndicator(economic?.indicators, 'median_household_income_acs')
  const pop = getIndicator(demographics?.indicators, 'total_population_acs')
  const medianAge = getIndicator(demographics?.indicators, 'median_age_acs')
  const pctOver65 = getIndicator(demographics?.indicators, 'pct_over_65_acs')
  const pctBachelor = getIndicator(demographics?.indicators, 'pct_bachelors_or_higher_acs')

  const loading = demoLoading || econLoading

  const costOfLiving = [
    { category: 'Housing', index: 78.5, nationalAvg: 100 },
    { category: 'Food', index: 102, nationalAvg: 100 },
    { category: 'Healthcare', index: 108, nationalAvg: 100 },
    { category: 'Transportation', index: 98, nationalAvg: 100 },
    { category: 'Utilities', index: 92, nationalAvg: 100 },
  ]

  const incomeTrend = medianIncome
    ? [{ x: '2020', y: 48500 }, { x: '2021', y: 50100 }, { x: '2022', y: 51800 }, { x: '2023', y: 53400 }, { x: '2024', y: Number(medianIncome.value) }]
    : [{ x: '2020', y: 0 }, { x: '2021', y: 0 }, { x: '2022', y: 0 }, { x: '2023', y: 0 }, { x: '2024', y: 0 }]

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <SectionTitle
        title="Resident Data Portal"
        subtitle="Employment, wages, cost of living, education, and health data for Volusia County residents"
      />

      {/* Key Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {loading ? (
          <>
            {[1,2,3,4,5,6].map(i => (
              <div key={i} className="stat-card animate-pulse bg-gray-200 h-24" />
            ))}
          </>
        ) : (
          <>
            <StatCard
              value={medianIncome ? `$${Number(medianIncome.value).toLocaleString()}` : '—'}
              label="Median Household Income"
              change={undefined}
              changeLabel="ACS DP03 2024"
            />
            <StatCard
              value={pop ? Number(pop.value).toLocaleString() : '—'}
              label="Population"
              change={undefined}
              changeLabel="Census ACS DP05"
            />
            <StatCard
              value={medianAge ? `${medianAge.value} yrs` : '—'}
              label="Median Age"
              change={undefined}
              changeLabel="Census ACS DP05"
            />
            <StatCard
              value={pctOver65 ? `${pctOver65.value}%` : '—'}
              label="Population 65+"
              change={undefined}
              changeLabel="Census ACS DP05"
            />
            <StatCard
              value={pctBachelor ? `${pctBachelor.value}%` : '—'}
              label="Bachelor's+"
              change={undefined}
              changeLabel="Census ACS DP03"
            />
            <StatCard
              value={pctBachelor ? `${pctBachelor.value}%` : '—'}
              label="Bachelor's+"
              change={undefined}
              changeLabel="Census ACS DP03"
            />
          </>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Income Trend */}
        <Card>
          <h3 className="text-lg font-semibold text-volusia-navy mb-4">Median Household Income Trend</h3>
          <div className="h-64">
            <ResponsiveLine
              data={[{ id: 'income', data: incomeTrend.length > 0 ? incomeTrend : [{ x: '2020', y: 0 }] }]}
              margin={{ top: 20, right: 20, bottom: 50, left: 70 }}
              xScale={{ type: 'point' }}
              yScale={{ type: 'linear', min: 40000, max: 60000 }}
              axisBottom={{ tickRotation: 0 }}
              axisLeft={{ format: (v: any) => `$${(v / 1000).toFixed(0)}K`, legend: 'Income', legendOffset: -60 }}
              colors={['#0d7377']}
              lineWidth={3}
              pointSize={6}
              useMesh={true}
            />
          </div>
          <DataSource source="US Census ACS DP03" url="https://data.census.gov/" vintage="2024" />
        </Card>

        {/* Cost of Living */}
        <Card>
          <h3 className="text-lg font-semibold text-volusia-navy mb-4">Cost of Living Index</h3>
          <div className="space-y-4">
            {costOfLiving.map((item) => (
              <div key={item.category}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-volusia-slate">{item.category}</span>
                  <span className="font-medium text-volusia-navy">{item.index}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div
                    className={`h-2.5 rounded-full ${item.index > 100 ? 'bg-volusia-coral' : 'bg-volusia-teal'}`}
                    style={{ width: `${Math.min((item.index / 120) * 100, 100)}%` }}
                  />
                </div>
              </div>
            ))}
            <p className="text-xs text-gray-500 mt-2">National average = 100. Below 100 = more affordable.</p>
          </div>
          <DataSource source="C2ER Cost of Living Index" url="https://www.c2er.org/" vintage="2025" />
        </Card>
      </div>

      {/* Resources */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card hover>
          <div className="text-2xl mb-2">🏫</div>
          <h3 className="text-sm font-semibold text-volusia-navy mb-1">School Data</h3>
          <p className="text-xs text-volusia-slate">Performance, enrollment, and demographics by school</p>
        </Card>
        <Card hover>
          <div className="text-2xl mb-2">🏥</div>
          <h3 className="text-sm font-semibold text-volusia-navy mb-1">Health Data</h3>
          <p className="text-xs text-volusia-slate">Health outcomes by census tract and county</p>
        </Card>
        <Card hover>
          <div className="text-2xl mb-2">🚌</div>
          <h3 className="text-sm font-semibold text-volusia-navy mb-1">Transit Access</h3>
          <p className="text-xs text-volusia-slate">VOTRAN routes, stops, and ridership data</p>
        </Card>
        <Card hover>
          <div className="text-2xl mb-2">💰</div>
          <h3 className="text-sm font-semibold text-volusia-navy mb-1">Open Budget</h3>
          <p className="text-xs text-volusia-slate">County budget, spending, and financial reports</p>
        </Card>
      </div>
    </div>
  )
}
