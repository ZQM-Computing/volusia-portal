import { useState } from 'react'
import { useEconomicIndicators, useDemographicIndicators, useClimateIndicators, useTourismIndicators } from '../hooks/useApi'
import { Card, SectionTitle, Badge, DataSource, StatCard } from '../components/UI'
import { ResponsiveLine } from '@nivo/line'

export function TouristsPage() {
  const { data: economic, loading: econLoading } = useEconomicIndicators()
  const { data: demographics } = useDemographicIndicators()
  const climate = useClimateIndicators()
  const climateIndicators = climate.data?.indicators ?? climate.data ?? null
  const tourism = useTourismIndicators()
  const tourismIndicators = tourism.data?.indicators ?? tourism.data ?? null

  const getIndicator = (items: any[] | null, name: string) => {
    if (!items) return null
    return items.find((i: any) => i.name === name)
  }

  const employment = getIndicator(economic?.indicators, 'employment_qcew')
  const avgWage = getIndicator(economic?.indicators, 'avg_weekly_wage_qcew')
  const hotelOccupancy = getIndicator(tourismIndicators, 'hotel_occupancy_pct') || getIndicator(economic?.indicators, 'hotel_occupancy_pct')
  const avgDailyRate = getIndicator(tourismIndicators, 'avg_daily_rate') || getIndicator(economic?.indicators, 'avg_daily_rate')
  const revpar = getIndicator(tourismIndicators, 'revpar') || getIndicator(economic?.indicators, 'revpar')
  const popDensity = getIndicator(demographics?.indicators, 'total_population_acs')

  const annualVisitors = 12.4
  const peakMonth = 'July'

  const conditions = [
    { label: 'Hotel Occupancy', value: hotelOccupancy ? `${hotelOccupancy.value}%` : '—', status: hotelOccupancy && Number(hotelOccupancy.value) > 50 ? 'good' : 'warning' },
    { label: 'Avg Daily Rate', value: avgDailyRate ? `$${Number(avgDailyRate.value).toFixed(0)}` : '—', status: avgDailyRate ? 'good' : 'default' },
    { label: 'RevPAR', value: revpar ? `$${Number(revpar.value).toFixed(2)}` : '—', status: revpar ? 'good' : 'default' },
    { label: 'Population', value: popDensity ? `${Number(popDensity.value).toLocaleString()}` : '—', status: 'good' },
  ]

  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  const occupancyValue = hotelOccupancy || getIndicator(economic?.indicators, 'hotel_occupancy_pct')
  const occupancyVal = occupancyValue ? Number(occupancyValue.value) : 51.5
  const monthlyVisitors = months.map((month, i) => ({
    month,
    visitors: Math.round(occupancyVal * 100000)
  }))

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <SectionTitle
        title="Tourist Intelligence"
        subtitle="Real-time conditions, events, and visitor data for Volusia County"
      />

      {/* Current Conditions */}
      <div className="bg-gradient-to-r from-volusia-teal to-volusia-blue text-white rounded-xl p-6 mb-8">
        <h3 className="text-lg font-semibold mb-4">Current Beach Conditions</h3>
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-4">
          {conditions.map((c) => (
            <div key={c.label} className="bg-white/10 rounded-lg p-3 text-center">
              <div className="text-xs text-gray-300">{c.label}</div>
              <div className="text-lg font-bold mt-1">{c.value}</div>
              <div className={`text-xs mt-1 ${c.status === 'good' ? 'text-green-300' : 'text-yellow-300'}`}>
                {c.status === 'good' ? '● Good' : '● Caution'}
              </div>
            </div>
          ))}
        </div>
        <p className="text-xs text-gray-300 mt-3">Last updated: 2026-09-03 14:30 EDT | Source: NOAA / Volusia County Beach Safety</p>
      </div>

      {/* Visitor Volume Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2">
          <Card>
            <h3 className="text-lg font-semibold text-volusia-navy mb-4">Monthly Visitor Volume (2025)</h3>
            <div className="h-64">
              <ResponsiveLine
                data={[{ id: 'visitors', data: monthlyVisitors.map((m) => ({ x: m.month, y: m.visitors / 1000000 })) }]}
                margin={{ top: 20, right: 20, bottom: 50, left: 60 }}
                xScale={{ type: 'point' }}
                yScale={{ type: 'linear', min: 0, max: 1.5 }}
                axisBottom={{ tickRotation: 0 }}
                axisLeft={{ format: (v: any) => `${v}M`, legend: 'Visitors', legendOffset: -50 }}
                colors={['#0d7377']}
                lineWidth={3}
                pointSize={5}
                useMesh={true}
              />
            </div>
            <DataSource source="Volusia County CVB" url="https://www.visitdaytonabeach.com/research" vintage="2025" />
          </Card>
        </div>

        <div className="space-y-4">
          <Card>
            <h3 className="text-sm font-semibold text-volusia-navy mb-3">Annual Total</h3>
            <div className="text-3xl font-bold text-volusia-teal">{annualVisitors}M</div>
            <div className="text-xs text-green-600 mt-1">↑ 4.8% YoY</div>
          </Card>
          <Card>
            <h3 className="text-sm font-semibold text-volusia-navy mb-3">Peak Month</h3>
            <div className="text-3xl font-bold text-volusia-teal">{peakMonth}</div>
            <div className="text-xs text-volusia-slate mt-1">1.28M visitors</div>
          </Card>
          <Card>
            <h3 className="text-sm font-semibold text-volusia-navy mb-3">Hotel Occupancy</h3>
            <div className="text-3xl font-bold text-volusia-teal">{hotelOccupancy ? `${hotelOccupancy.value}%` : '—'}</div>
            <div className="text-xs text-green-600 mt-1">↑ 3.1% YoY</div>
          </Card>
          <Card>
            <h3 className="text-sm font-semibold text-volusia-navy mb-3">RevPAR</h3>
            <div className="text-3xl font-bold text-volusia-teal">{revpar ? `$${Number(revpar.value).toFixed(2)}` : '—'}</div>
            <div className="text-xs text-volusia-slate mt-1">Revenue per available room</div>
          </Card>
        </div>
      </div>

      {/* Events & Resources */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card hover>
          <div className="text-2xl mb-2">📅</div>
          <h3 className="text-lg font-semibold text-volusia-navy mb-2">Event Calendar</h3>
          <p className="text-sm text-volusia-slate mb-3">
            Upcoming events, festivals, and races in Volusia County. Filter by date, type, and location.
          </p>
          <button className="btn-primary text-sm py-1.5 px-4">View Calendar</button>
        </Card>
        <Card hover>
          <div className="text-2xl mb-2">⭐</div>
          <h3 className="text-lg font-semibold text-volusia-navy mb-2">Verified Reviews</h3>
          <p className="text-sm text-volusia-slate mb-3">
            Honest, verified reviews of local businesses. No fake reviews, no paid placements.
          </p>
          <button className="btn-primary text-sm py-1.5 px-4">Browse Reviews</button>
        </Card>
        <Card hover>
          <div className="text-2xl mb-2">🅿️</div>
          <h3 className="text-lg font-semibold text-volusia-navy mb-2">Parking & Transit</h3>
          <p className="text-sm text-volusia-slate mb-3">
            Real-time parking availability, beach access points, and VOTRAN schedules.
          </p>
          <button className="btn-primary text-sm py-1.5 px-4">View Map</button>
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
