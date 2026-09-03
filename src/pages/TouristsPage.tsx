import { indicators } from '../data/sampleData'
import { Card, SectionTitle, Badge, DataSource } from '../components/UI'
import { ResponsiveLine } from '@nivo/line'

export function TouristsPage() {
  const tourismIndicators = indicators.filter((i) => i.category === 'tourism')

  const monthlyVisitors = [
    { month: 'Jan', visitors: 820000 },
    { month: 'Feb', visitors: 910000 },
    { month: 'Mar', visitors: 1180000 },
    { month: 'Apr', visitors: 1050000 },
    { month: 'May', visitors: 980000 },
    { month: 'Jun', visitors: 1120000 },
    { month: 'Jul', visitors: 1280000 },
    { month: 'Aug', visitors: 1150000 },
    { month: 'Sep', visitors: 870000 },
    { month: 'Oct', visitors: 920000 },
    { month: 'Nov', visitors: 850000 },
    { month: 'Dec', visitors: 980000 },
  ]

  const conditions = [
    { label: 'Surf', value: '2-3 ft', status: 'good' },
    { label: 'Water Temp', value: '78°F', status: 'good' },
    { label: 'Weather', value: 'Sunny, 85°F', status: 'good' },
    { label: 'Traffic', value: 'Moderate', status: 'warning' },
    { label: 'Beach Flags', value: 'Green', status: 'good' },
  ]

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
              <div className="text-xs text-gray-200">{c.label}</div>
              <div className="text-lg font-bold mt-1">{c.value}</div>
              <div className={`text-xs mt-1 ${c.status === 'good' ? 'text-green-300' : 'text-yellow-300'}`}>
                {c.status === 'good' ? '● Good' : '● Caution'}
              </div>
            </div>
          ))}
        </div>
        <p className="text-xs text-gray-200 mt-3">Last updated: 2026-09-02 14:30 EDT | Source: NOAA / Volusia County Beach Safety</p>
      </div>

      {/* Visitor Volume Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2">
          <Card>
            <h3 className="text-lg font-semibold text-volusia-navy mb-4">Monthly Visitor Volume (2025)</h3>
            <div className="h-64">
              <ResponsiveLine
                data={[
                  {
                    id: 'visitors',
                    data: monthlyVisitors.map((m) => ({ x: m.month, y: m.visitors / 1000000 })),
                  },
                ]}
                margin={{ top: 20, right: 20, bottom: 50, left: 60 }}
                xScale={{ type: 'point' }}
                yScale={{ type: 'linear', min: 0, max: 1.5 }}
                axisBottom={{ tickRotation: 0 }}
                axisLeft={{ format: (v) => `${v}M`, legend: 'Visitors', legendOffset: -50 }}
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
            <div className="text-3xl font-bold text-volusia-teal">12.4M</div>
            <div className="text-xs text-green-600 mt-1">↑ 4.8% YoY</div>
          </Card>
          <Card>
            <h3 className="text-sm font-semibold text-volusia-navy mb-3">Peak Month</h3>
            <div className="text-3xl font-bold text-volusia-teal">July</div>
            <div className="text-xs text-volusia-slate mt-1">1.28M visitors</div>
          </Card>
          <Card>
            <h3 className="text-sm font-semibold text-volusia-navy mb-3">Hotel Occupancy</h3>
            <div className="text-3xl font-bold text-volusia-teal">72.4%</div>
            <div className="text-xs text-green-600 mt-1">↑ 3.1% YoY</div>
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
    </div>
  )
}
