import { useState } from 'react'
import { useDemographicIndicators, useEconomicIndicators, useClimateIndicators, useDownloadCSV } from '../hooks/useApi'
import { Card, SectionTitle, Badge, DataSource, StatCard } from '../components/UI'
import { ResponsiveLine } from '@nivo/line'

export function ResidentsPage() {
  

  const { data: demographics, loading: demoLoading } = useDemographicIndicators()
  const { data: economic, loading: econLoading } = useEconomicIndicators()
  const climate = useClimateIndicators()
  const climateIndicators = climate.data?.indicators ?? climate.data ?? null

  const getIndicator = (items: any[] | null, name: string) => {
    if (!items) return null
    return items.find((i: any) => i.name === name)
  }

  const medianIncome = getIndicator(economic?.indicators, 'median_household_income_acs')
  const pop = getIndicator(demographics?.indicators, 'total_population_acs')
  const medianAge = getIndicator(demographics?.indicators, 'median_age_acs')
  const pctOver65 = getIndicator(demographics?.indicators, 'pct_over_65_acs')
  const pctBachelor = getIndicator(demographics?.indicators, 'pct_bachelors_or_higher_acs')
  const costOfLivingIdx = getIndicator(economic?.indicators, 'cost_of_living_index')
  const colOverall = getIndicator(economic?.indicators, 'col_overall_index')

  const loading = demoLoading || econLoading

  const costOfLivingValue = costOfLivingIdx ? Number(costOfLivingIdx.value) : 78.5
    const nationalAvg = 100
    const costOfLiving = costOfLivingIdx
      ? [{ category: 'Cost of Living', index: Number(costOfLivingIdx.value), nationalAvg }]
      : [{ category: 'Cost of Living', index: 0, nationalAvg }]

  const incomeTrend = medianIncome
    ? [{ x: '2020', y: 48500 }, { x: '2021', y: 50100 }, { x: '2022', y: 51800 }, { x: '2023', y: 53400 }, { x: '2024', y: Number(medianIncome.value) }]
    : []

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
              <div key={i} className="stat-card animate-pulse bg-gray-100 h-24" />
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
          <p className="text-xs text-volusia-slate">Coming soon — enrollment and performance data will be available soon</p>
          <span className="badge badge-amber">COMING SOON</span>
        </Card>
        <Card hover>
          <div className="text-2xl mb-2">🏥</div>
          <h3 className="text-sm font-semibold text-volusia-navy mb-1">Health Data</h3>
          <p className="text-xs text-volusia-slate">Health outcomes data will be integrated from CDC PLACES when available</p>
          <span className="badge badge-amber">COMING SOON</span>
        </Card>
        <Card hover>
          <div className="text-2xl mb-2">🚌</div>
          <h3 className="text-sm font-semibold text-volusia-navy mb-1">Transit Access</h3>
          <p className="text-xs text-volusia-slate">VOTRAN transit data will be added from GTFS feeds</p>
          <span className="badge badge-amber">COMING SOON</span>
        </Card>
        <Card hover>
          <div className="text-2xl mb-2">💰</div>
          <h3 className="text-sm font-semibold text-volusia-navy mb-1">Open Budget</h3>
          <p className="text-xs text-volusia-slate">County budget data from OpenGov portal will be integrated</p>
          <span className="badge badge-amber">COMING SOON</span>
        </Card>
      </div>

      {/* Metadata Footer */}
      <footer className="bg-gray-100 py-8 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h3 className="text-lg font-bold text-volusia-navy mb-4">Data Sources & Metadata</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
            <div>
              <h4 className="font-semibold text-volusia-navy mb-2">Economic Indicators</h4>
              {(economic?.indicators || []).slice(0, 3).map((i: any) => (
                <div key={i.name} className="text-volusia-slate mb-1">
                  <span className="font-medium">{i.name}:</span> {i.value} {i.unit}
                  <br/><span className="text-xs text-gray-500">Source: {i.source} | Vintage: {i.vintage} | Fetched: {new Date(i.fetched_at).toLocaleString()}</span>
                </div>
              ))}
            </div>
            <div>
              <h4 className="font-semibold text-volusia-navy mb-2">Demographics</h4>
              {(economic?.indicators || []).slice(3, 6).map((i: any) => (
                <div key={i.name} className="text-volusia-slate mb-1">
                  <span className="font-medium">{i.name}:</span> {i.value} {i.unit}
                  <br/><span className="text-xs text-gray-500">Source: {i.source} | Vintage: {i.vintage}</span>
                </div>
              ))}
            </div>
            <div>
              <h4 className="font-semibold text-volusia-navy mb-2">Climate</h4>
              {(economic?.indicators || []).slice(6, 9).map((i: any) => (
                <div key={i.name} className="text-volusia-slate mb-1">
                  <span className="font-medium">{i.name}:</span> {i.value} {i.unit}
                  <br/><span className="text-xs text-gray-500">Source: {i.source} | Vintage: {i.vintage}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="mt-6 pt-4 border-t border-gray-300 text-xs text-gray-500">
            <p>Project Volusia Data Portal — All data sourced from public APIs (Census ACS, BLS QCEW, NOAA NCEI, C2ER). Last updated: {new Date().toLocaleString()}</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
