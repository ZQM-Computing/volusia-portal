import { useState, useEffect } from 'react'
import { useEconomicIndicators } from '../hooks/useApi'
import { Card, SectionTitle, Badge, DataSource, StatCard, Skeleton, EmptyState, ErrorState } from '../components/UI'
import { ResponsiveBar } from '@nivo/bar'

export function LeadersPage() {
  const { data: economic, loading, error, refetch } = useEconomicIndicators()

  useEffect(() => { document.title = 'Community Leaders — Project Volusia' }, [])

  if (error) return <ErrorState message={error} onRetry={refetch} />
  if (loading) return <Skeleton count={4} />
  if (!economic?.indicators) return <EmptyState title="No indicator data" description="The backend may be starting up." />

  const getIndicator = (name: string) => economic.indicators.find((i: any) => i.name === name) ?? null
  const fmtNum = (v: any) => { if (v == null) return '—'; const n = Number(v); return isNaN(n) ? String(v) : n.toLocaleString() }

  // Employment by sector: use real indicator data
  const employmentData = economic.indicators.filter((i: any) => i.name?.includes('employment')) as any[]
  const capitalData = economic.indicators.filter((i: any) => i.name?.includes('capital') || i.name?.includes('investment')) as any[]
  const avgWage = getIndicator('avg_weekly_wage_qcew')

  return (
    <div>
      <SectionTitle title="Community Leaders" subtitle="Capital flows, employment, and workforce data for decision-making" />
      <Badge variant="info">{economic.indicators.length} live indicators</Badge>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 my-8">
        <StatCard value={employmentData.length > 0 ? `${employmentData.reduce((s: number, i: any) => s + Number(i.value||0), 0).toLocaleString()}` : '—'} label="Total Employment" change={undefined} changeLabel="QCEW" />
        <StatCard value={capitalData.length > 0 ? `${capitalData.length} capital records` : '—'} label="Capital Flow Records" change={undefined} changeLabel="BEA" />
        <StatCard value={avgWage ? `$${fmtNum(avgWage.value)}` : '—'} label="Avg Weekly Wage" change={undefined} changeLabel="QCEW" />
      </div>

      {employmentData.length > 0 && (
        <Card className="mb-8">
          <h3 className="font-bold text-volusia-navy mb-4">Employment by Sector</h3>
          <ResponsiveBar
            data={employmentData.map((i: any) => ({ sector: i.name.replace(/_/g, ' ').replace(/\b\w/g, (c: string) => c.toUpperCase()), jobs: Number(i.value) }))}
            keys={['jobs']}
            indexBy="sector"
            margin={{ top: 10, right: 30, bottom: 60, left: 60 }}
          />
          <DataSource source="BLS QCEW" url="https://www.bls.gov/" vintage="2024" />
        </Card>
      )}

      {capitalData.length > 0 && (
        <Card className="mb-8">
          <h3 className="font-bold text-volusia-navy mb-4">Capital Flows</h3>
          {capitalData.map((i: any) => (
            <div key={i.name} className="flex justify-between py-2 border-b border-gray-100 text-sm">
              <span className="text-volusia-slate">{i.name.replace(/_/g, ' ')}</span>
              <span className="font-medium text-volusia-navy">{fmtNum(i.value)} {i.unit}</span>
            </div>
          ))}
          <DataSource source="BEA" url="https://www.bea.gov/" vintage="2024" />
        </Card>
      )}

      {employmentData.length === 0 && <EmptyState title="No employment data" description="QCEW data is being refreshed. Check back shortly." />}
      {capitalData.length === 0 && <EmptyState title="No capital flow data" description="BEA capital data is being refreshed." />}

      <Card className="mb-8">
        <h3 className="font-bold text-volusia-navy mb-4">Permitting & Zoning</h3>
        <p className="text-sm text-volusia-slate mb-4">Real-time permitting data from Volusia County's ePermitting system.</p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-gray-50 rounded-lg"><div className="text-2xl font-bold text-volusia-teal">—</div><div className="text-xs text-volusia-slate">Pending</div></div>
          <div className="text-center p-4 bg-gray-50 rounded-lg"><div className="text-2xl font-bold text-volusia-teal">—</div><div className="text-xs text-volusia-slate">Approved</div></div>
          <div className="text-center p-4 bg-gray-50 rounded-lg"><div className="text-2xl font-bold text-volusia-teal">—</div><div className="text-xs text-volusia-slate">Inspections</div></div>
          <div className="text-center p-4 bg-gray-50 rounded-lg"><div className="text-2xl font-bold text-volusia-teal">—</div><div className="text-xs text-volusia-slate">Zoning</div></div>
        </div>
      </Card>

      <Card>
        <h3 className="font-bold text-volusia-navy mb-4">Available Indicators</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-volusia-slate border-b">
                <th className="pb-2">Indicator</th>
                <th className="pb-2">Value</th>
                <th className="pb-2">Unit</th>
                <th className="pb-2">Vintage</th>
              </tr>
            </thead>
            <tbody>
              {economic.indicators.map((i: any) => (
                <tr key={i.name} className="border-b border-gray-100">
                  <td className="py-2 text-volusia-navy">{i.name}</td>
                  <td className="py-2">{fmtNum(i.value)}</td>
                  <td className="py-2">{i.unit}</td>
                  <td className="py-2">{i.vintage}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}