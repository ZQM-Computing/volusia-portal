import { useState, useEffect } from 'react'
import { useEconomicIndicators } from '../hooks/useApi'
import { Card, SectionTitle, Badge, DataSource, StatCard, Skeleton, EmptyState, ErrorState } from '../components/UI'
import { ResponsiveBar } from '@nivo/bar'

export function BusinessPage() {
  const { data: economic, loading, error, refetch } = useEconomicIndicators()

  useEffect(() => { document.title = 'Business & Economy — Project Volusia' }, [])

  if (error) return <ErrorState message={error} onRetry={refetch} />
  if (loading) return <Skeleton count={4} />
  if (!economic?.indicators) return <EmptyState title="No economic data" description="The backend may be starting up." />

  const getIndicator = (name: string) => economic.indicators.find((i: any) => i.name === name) ?? null
  const fmtNum = (v: any) => { if (v == null) return '—'; const n = Number(v); return isNaN(n) ? String(v) : n.toLocaleString() }

  const sectorIndicators = economic.indicators.filter((i: any) =>
      i.name?.match(/employment|industry|sector|trade|construction|manufacturing|professional/)
    ) as any[]

    const avgWage = getIndicator('avg_weekly_wage_qcew')
  const personalIncome = getIndicator('personal_income_total')

  return (
    <div>
      <SectionTitle title="Business & Economy" subtitle="Real economic indicators for Volusia County" />
      <Badge variant="info">{economic.indicators.length} live indicators</Badge>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 my-8">
        <StatCard value={personalIncome ? `$${fmtNum(personalIncome.value)}` : '—'} label="Personal Income" change={undefined} changeLabel="BEA" />
        <StatCard value={avgWage ? `$${fmtNum(avgWage.value)}` : '—'} label="Avg Weekly Wage" change={undefined} changeLabel="QCEW" />
        <StatCard value={sectorIndicators.length > 0 ? `${sectorIndicators.length} sectors` : '—'} label="Industry Sectors" change={undefined} changeLabel="" />
        <StatCard value={sectorIndicators.length > 0 ? `${Math.round(sectorIndicators.reduce((s: number, i: any) => s + Number(i.value||0), 0)).toLocaleString()}` : '—'} label="Total Employment" change={undefined} changeLabel="" />
      </div>

      {sectorIndicators.length > 0 && (
        <Card className="mb-8">
          <h3 className="font-bold text-volusia-navy mb-4">Employment by Sector</h3>
          <ResponsiveBar
            data={sectorIndicators.map((i: any) => ({ sector: i.name.replace(/_/g, ' ').replace(/\b\w/g, (c: string) => c.toUpperCase()), jobs: Number(i.value) }))}
            keys={['jobs']}
            indexBy="sector"
            margin={{ top: 10, right: 30, bottom: 60, left: 60 }}
          />
          <DataSource source="BLS QCEW" url="https://www.bls.gov/" vintage="2024" />
        </Card>
      )}

      <Card className="mb-8">
        <h3 className="font-bold text-volusia-navy mb-4">Cost-of-Living Context</h3>
        <p className="text-sm text-volusia-slate mb-4">
          Cost-of-living comparisons are available from C2ER (Council for Community and Economic Research).
          Contact <a href="mailto:info@volusia.org" className="text-volusia-teal underline">Volusia County</a> for the latest index.
        </p>
        <div className="text-sm">
          <div className="flex justify-between py-2 border-b border-gray-100">
            <span className="text-volusia-slate">Housing</span>
            <span className="font-medium text-volusia-navy">{getIndicator('housing_median_value') ? `$${fmtNum(getIndicator('housing_median_value')?.value)}` : '—'}</span>
          </div>
          <div className="flex justify-between py-2 border-b border-gray-100">
            <span className="text-volusia-slate">Median Income</span>
            <span className="font-medium text-volusia-navy">{getIndicator('median_household_income_acs') ? `$${fmtNum(getIndicator('median_household_income_acs')?.value)}` : '—'}</span>
          </div>
          <div className="flex justify-between py-2 border-b border-gray-100">
            <span className="text-volusia-slate">Unemployment</span>
            <span className="font-medium text-volusia-navy">{getIndicator('unemployment_rate_acs') ? `${getIndicator('unemployment_rate_acs')?.value}%` : '—'}</span>
          </div>
        </div>
        <DataSource source="C2ER / ACS" url="https://www.c2er.org/" vintage="2024" />
      </Card>

      <Card>
        <h3 className="font-bold text-volusia-navy mb-4">Business Resources</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <a href="https://www.volusia.org/business" target="_blank" rel="noopener noreferrer" className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
            <h4 className="font-semibold text-volusia-navy">Volusia County Economic Development</h4>
            <p className="text-sm text-volusia-slate">Business permits, incentives, and planning.</p>
          </a>
          <a href="https://www.c2er.org/" target="_blank" rel="noopener noreferrer" className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
            <h4 className="font-semibold text-volusia-navy">C2ER Cost-of-Living Index</h4>
            <p className="text-sm text-volusia-slate">National benchmark for cost comparisons.</p>
          </a>
        </div>
      </Card>
    </div>
  )
}