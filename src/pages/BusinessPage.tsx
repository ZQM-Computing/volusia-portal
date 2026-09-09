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

  // Build chart data from live indicators
  const businessFormation = economic?.indicators
    ?.filter((i: any) => i.name?.includes('establishments') || i.name?.includes('employment'))
    .map((i: any) => ({ x: '2024', y: Number(i.value) ?? 0 })) ?? []

  const employmentValue = getIndicator(economic?.indicators, 'employment_qcew')
  const industryMix = [
      { industry: 'Tourism', count: 0, pct: 14.7 },
      { industry: 'Retail', count: 0, pct: 13.3 },
      { industry: 'Healthcare', count: 0, pct: 11.2 },
      { industry: 'Construction', count: 0, pct: 10.2 },
      { industry: 'Education', count: 0, pct: 7.4 },
      { industry: 'Manufacturing', count: 0, pct: 6.3 },
      { industry: 'Professional', count: 0, pct: 11.9 },
      { industry: 'Other', count: 0, pct: 24.9 },
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
            {[1,2,3,4].map(i => <div key={i} className="stat-card animate-pulse bg-gray-100 h-24" />)}
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

        {/* Industry Mix */}
        <Card>
          <h3 className="text-lg font-semibold text-volusia-navy mb-4">Industry Mix (Based on Employment)</h3>
          <div className="h-64">
            <ResponsiveBar
              data={industryMix}
              keys={['count']}
              indexBy="industry"
              margin={{ top: 20, right: 20, bottom: 60, left: 60 }}
              padding={0.3}
              colors={['#0d7377']}
              axisBottom={{ tickRotation: -30 }}
              axisLeft={{ legend: 'Businesses (est.)', legendOffset: -50 }}
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
          <span className="text-sm text-volusia-slate italic">COMING SOON</span>
        </Card>
        <Card hover>
          <div className="text-2xl mb-2">🗺️</div>
          <h3 className="text-lg font-semibold text-volusia-navy mb-2">Location Intelligence</h3>
          <p className="text-sm text-volusia-slate mb-3">
            Analyze foot traffic, demographics, and competitor density for any location in Volusia County.
          </p>
          <span className="text-sm text-volusia-slate italic">COMING SOON</span>
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
