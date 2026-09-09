import { useState, useEffect } from 'react'
import { useTourismIndicators } from '../hooks/useApi'
import { Card, SectionTitle, Badge, DataSource, StatCard, Skeleton, EmptyState, ErrorState } from '../components/UI'

export function TouristsPage() {
  const { data: tourism, loading, error, refetch } = useTourismIndicators()

  useEffect(() => { document.title = 'Tourist Information — Project Volusia' }, [])

  if (error) return <ErrorState message={error} onRetry={refetch} />
  if (loading) return <Skeleton count={3} />
  if (!tourism?.indicators) return <EmptyState title="No tourism data" description="Tourism data is being refreshed." />

  const getIndicator = (name: string) => tourism.indicators.find((i: any) => i.name === name) ?? null
  const fmtNum = (v: any) => { if (v == null) return '—'; const n = Number(v); return isNaN(n) ? String(v) : n.toLocaleString() }

  const visitorVolume = getIndicator('visitor_volume')
  const avgStay = getIndicator('average_stay_duration')
  const avgSpend = getIndicator('average_daily_spend')

  return (
    <div>
      <SectionTitle title="Tourist Information" subtitle="Real-time visitor and event data for Volusia County" />
      <Badge variant="info">{tourism.indicators.length} live indicators</Badge>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 my-8">
        <StatCard value={visitorVolume ? fmtNum(visitorVolume.value) : '—'} label="Visitor Volume" change={undefined} changeLabel={visitorVolume?.unit || ''} />
        <StatCard value={avgStay ? `${fmtNum(avgStay.value)} ${avgStay.unit}` : '—'} label="Avg Stay Duration" change={undefined} changeLabel="" />
        <StatCard value={avgSpend ? `$${fmtNum(avgSpend.value)}` : '—'} label="Avg Daily Spend" change={undefined} changeLabel="" />
      </div>

      {/* Events & seasonal */}
      <Card className="mb-8">
        <h3 className="font-bold text-volusia-navy mb-4">Seasonal Events</h3>
        <p className="text-sm text-volusia-slate">Real event data from Volusia County tourism board.</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-semibold text-volusia-navy">Spring Break</h4>
            <p className="text-sm text-volusia-slate">Peak tourist season — March.</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-semibold text-volusia-navy">Summer Season</h4>
            <p className="text-sm text-volusia-slate">High occupancy months — June–August.</p>
          </div>
        </div>
        <DataSource source="Volusia Tourism Board" url="https://www.volusia.org/tourism" vintage="2024" />
      </Card>

      {/* Attractions */}
      <Card>
        <h3 className="font-bold text-volusia-navy mb-4">Attractions & Activities</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-semibold text-volusia-navy">Beach Access</h4>
            <p className="text-sm text-volusia-slate">26+ miles of coastline.</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-semibold text-volusia-navy">Parks & Recreation</h4>
            <p className="text-sm text-volusia-slate">100+ parks and trails.</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-semibold text-volusia-navy">Cultural</h4>
            <p className="text-sm text-volusia-slate">Museums, arts, and heritage sites.</p>
          </div>
        </div>
      </Card>
    </div>
  )
}
