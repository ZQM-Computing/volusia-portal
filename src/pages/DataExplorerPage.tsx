import { useState } from 'react'
import { datasets, indicators } from '../data/sampleData'
import { Card, SectionTitle, Badge, DataSource } from '../components/UI'
import { ResponsiveLine } from '@nivo/line'
import { ResponsiveBar } from '@nivo/bar'

export function DataExplorerPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [categoryFilter, setCategoryFilter] = useState<string>('all')
  const [statusFilter, setStatusFilter] = useState<string>('all')

  const categories = ['all', ...new Set(datasets.map((d) => d.category))]
  const statuses = ['all', 'available', 'in-development', 'gated', 'missing']

  const filteredDatasets = datasets.filter((d) => {
    const matchesSearch =
      d.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = categoryFilter === 'all' || d.category === categoryFilter
    const matchesStatus = statusFilter === 'all' || d.status === statusFilter
    return matchesSearch && matchesCategory && matchesStatus
  })

  const unemploymentData = indicators.find((i) => i.id === 'unemployment')
  const incomeData = indicators.find((i) => i.id === 'median-income')

  const barData = [
    { quarter: 'Q1 \'25', unemployment: 4.1, poverty: 14.2 },
    { quarter: 'Q2 \'25', unemployment: 3.8, poverty: 13.9 },
    { quarter: 'Q3 \'25', unemployment: 3.6, poverty: 13.7 },
    { quarter: 'Q4 \'25', unemployment: 3.5, poverty: 13.4 },
    { quarter: 'Q1 \'26', unemployment: 3.6, poverty: 13.1 },
    { quarter: 'Q2 \'26', unemployment: 3.2, poverty: 12.8 },
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <SectionTitle
        title="Data Explorer"
        subtitle="Search, filter, and download open datasets for Volusia County"
      />

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Card>
          <h3 className="text-lg font-semibold text-volusia-navy mb-4">Unemployment Trend</h3>
          <div className="h-64">
            {unemploymentData?.trendData && (
              <ResponsiveLine
                data={[
                  {
                    id: 'unemployment',
                    data: unemploymentData.trendData.map((d) => ({ x: d.x, y: d.y })),
                  },
                ]}
                margin={{ top: 20, right: 20, bottom: 50, left: 50 }}
                xScale={{ type: 'point' }}
                yScale={{ type: 'linear', min: 0, max: 6 }}
                axisBottom={{ tickRotation: -30 }}
                axisLeft={{ legend: '%', legendOffset: -40 }}
                colors={['#0d7377']}
                lineWidth={3}
                pointSize={6}
                useMesh={true}
              />
            )}
          </div>
          <DataSource source={unemploymentData?.source || ''} url={unemploymentData?.sourceUrl || ''} vintage={unemploymentData?.vintage} />
        </Card>

        <Card>
          <h3 className="text-lg font-semibold text-volusia-navy mb-4">Quarterly Comparison</h3>
          <div className="h-64">
            <ResponsiveBar
              data={barData}
              keys={['unemployment', 'poverty']}
              indexBy="quarter"
              margin={{ top: 20, right: 20, bottom: 50, left: 50 }}
              padding={0.3}
              colors={['#0d7377', '#c9a84c']}
              axisBottom={{ tickRotation: -30 }}
              axisLeft={{ legend: '%', legendOffset: -40 }}
              labelSkipWidth={12}
              labelSkipHeight={12}
              legends={[
                { dataFrom: 'keys', anchor: 'bottom-right', direction: 'column', itemWidth: 100, itemHeight: 20 },
              ]}
            />
          </div>
          <DataSource source="BLS LAUS / Census ACS" url="https://www.bls.gov/lau/" vintage="2026-Q2" />
        </Card>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6 border border-gray-100">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
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
            <label className="block text-sm font-medium text-volusia-slate mb-1">Category</label>
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-volusia-teal focus:border-transparent"
            >
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c === 'all' ? 'All Categories' : c.charAt(0).toUpperCase() + c.slice(1)}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-volusia-slate mb-1">Status</label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-volusia-teal focus:border-transparent"
            >
              {statuses.map((s) => (
                <option key={s} value={s}>
                  {s === 'all' ? 'All Statuses' : s.charAt(0).toUpperCase() + s.slice(1)}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Dataset List */}
      <div className="space-y-4">
        {filteredDatasets.length === 0 ? (
          <Card>
            <p className="text-volusia-slate text-center py-8">No datasets match your filters.</p>
          </Card>
        ) : (
          filteredDatasets.map((dataset) => (
            <Card key={dataset.id}>
              <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="text-lg font-semibold text-volusia-navy">{dataset.name}</h3>
                    <Badge
                      variant={
                        dataset.status === 'available'
                          ? 'success'
                          : dataset.status === 'in-development'
                          ? 'warning'
                          : dataset.status === 'gated'
                          ? 'error'
                          : 'default'
                      }
                    >
                      {dataset.status}
                    </Badge>
                  </div>
                  <p className="text-sm text-volusia-slate mb-2">{dataset.description}</p>
                  <div className="flex flex-wrap gap-3 text-xs text-gray-500">
                    <span>Format: {dataset.format}</span>
                    <span>Vintage: {dataset.vintage}</span>
                    <span>License: {dataset.license}</span>
                    {dataset.downloads && <span>Downloads: {dataset.downloads}</span>}
                  </div>
                </div>
                <div className="flex gap-2">
                  {dataset.status === 'available' && (
                    <>
                      <button className="btn-primary text-sm py-1.5 px-3">Download CSV</button>
                      <button className="btn-secondary text-sm py-1.5 px-3">API</button>
                    </>
                  )}
                  {dataset.status === 'in-development' && (
                    <button className="btn-secondary text-sm py-1.5 px-3">Notify Me</button>
                  )}
                  {dataset.status === 'gated' && (
                    <button className="btn-secondary text-sm py-1.5 px-3">Request Access</button>
                  )}
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  )
}
