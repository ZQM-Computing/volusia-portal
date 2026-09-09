import { useState, useEffect, useMemo } from 'react'
import { ErrorBoundary } from '../utils'
import { useDebounce } from '../utils/useDebounce'
import { useDatasets, useIndicator, useMapLayers, useDownloadCSV, useIndicatorList } from '../hooks/useApi'
import { Card, SectionTitle, Badge, DataSource } from '../components/UI'
import { ResponsiveLine } from '@nivo/line'
import { ResponsiveBar } from '@nivo/bar'

export function DataExplorerPage() {

  const [searchTerm, setSearchTerm] = useState('')
  const debouncedSearch = useDebounce(searchTerm, 300)
  const [categoryFilter, setCategoryFilter] = useState<string>('all')

  const { data: datasets, loading: dsLoading } = useDatasets()
  const indicators = useIndicatorList()
  const { data: mapLayers } = useMapLayers()
  const downloadCSV = useDownloadCSV()

  const items = datasets?.datasets ?? datasets ?? []
  const allCategories = ['all', ...new Set(items.map((d: any) => d.category || d.source || '').filter(Boolean))]

  const filtered = items.filter((d: any) => {
    const matchesSearch =
      (d.name ?? '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (d.source ?? '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (d.vintage ?? '').toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = categoryFilter === 'all' || (d.category ?? '').toLowerCase().includes(categoryFilter.toLowerCase())
    return matchesSearch && matchesCategory
  })

  // Build chart data from live indicators
  const unemploymentData = useMemo(() =>
    indicators?.data?.indicators
      ?.filter((i: any) => i.name?.includes('unemployment_rate'))
      .map((i: any) => ({ name: i.name, value: Number(i.value) })) ?? []
  , [indicators])

  const incomeData = useMemo(() =>
    indicators?.data?.indicators
      ?.filter((i: any) => i.name?.includes('median_household_income') || i.name?.includes('per_capita_income') || i.name?.includes('personal_income'))
      .map((i: any) => ({ name: i.name, value: Number(i.value) })) ?? []
  , [indicators])

  const barData = unemploymentData.length > 0
    ? [{ id: 'unemployment', data: unemploymentData.map((d: any) => ({ x: d.name, y: d.value })) }]
    : [{ id: 'unemployment', data: [{ x: 'N/A', y: 0 }] }]

  const barData2 = incomeData.length > 0
    ? [{ id: 'income', data: incomeData.map((d: any) => ({ x: d.name, y: d.value })) }]
    : [{ id: 'income', data: [{ x: 'N/A', y: 0 }] }]

  if (dsLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <SectionTitle title="Data Explorer" subtitle="Search, filter, and download open datasets for Volusia County" />
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {[1, 2].map(i => <div key={i} className="bg-gray-100 rounded-lg h-64 animate-pulse" />)}
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <SectionTitle
        title="Data Explorer"
        subtitle="Search, filter, and download open datasets for Volusia County"
      />

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Card>
          <h3 className="text-lg font-semibold text-volusia-navy mb-4">Unemployment Rate</h3>
          <div className="h-64">
            <ResponsiveLine
              data={barData}
              margin={{ top: 20, right: 20, bottom: 50, left: 50 }}
              xScale={{ type: 'point' }}
              yScale={{ type: 'linear', min: 0 }}
              axisBottom={{ tickRotation: -30 }}
              axisLeft={{ legend: '%', legendOffset: -40 }}
              colors={['#0d7377']}
              lineWidth={3}
              pointSize={6}
              useMesh={true}
            />
          </div>
          <DataSource source="BLS LAUS / Census ACS" url="https://www.bls.gov/lau/" vintage="2026" />
        </Card>

        <Card>
          <h3 className="text-lg font-semibold text-volusia-navy mb-4">Income Indicators</h3>
          <div className="h-64">
            <ResponsiveBar
              data={barData2}
              keys={['value']}
              indexBy="name"
              margin={{ top: 20, right: 20, bottom: 50, left: 50 }}
              padding={0.3}
              colors={['#0d7377', '#c9a84c']}
              axisBottom={{ tickRotation: -30 }}
              axisLeft={{ legend: '$', legendOffset: -40 }}
            />
          </div>
          <DataSource source="US Census ACS / BEA" url="https://data.census.gov/" vintage="2024" />
        </Card>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6 border border-gray-100">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-volusia-slate mb-1">Search</label>
            <input
              type="text"
              placeholder="Search datasets..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-volusia-teal focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-volusia-slate mb-1">Source</label>
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-volusia-teal focus:border-transparent"
            >
              {(allCategories as string[]).map((c) => (
                <option key={c} value={c}>{c === 'all' ? 'All Sources' : c}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Dataset List */}
      <div className="space-y-4">
        {filtered.length === 0 ? (
          <Card><p className="text-volusia-slate text-center py-8">No datasets match your filters.</p></Card>
        ) : (
          filtered.map((dataset: any) => (
            <Card key={dataset.id}>
              <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="text-lg font-semibold text-volusia-navy">{dataset.source || `Dataset #${dataset.id}`}</h3>
                    <Badge variant="success">Available</Badge>
                  </div>
                  <p className="text-sm text-volusia-slate mb-2">
                    {dataset.source} — Vintage: {dataset.vintage ? String(dataset.vintage).slice(0, 10) : 'N/A'}
                  </p>
                  <div className="flex flex-wrap gap-3 text-xs text-gray-500">
                    <span>ID: {dataset.id}</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button className="btn-primary text-sm py-1.5 px-3" onClick={() => downloadCSV()}>
                    Download CSV
                  </button>
                  <button className="btn-secondary text-sm py-1.5 px-3" onClick={() => window.open(`/indicators.csv`, '_blank')}>
                    API
                  </button>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  )
}
