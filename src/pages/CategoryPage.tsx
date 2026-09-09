import { useMemo } from 'react'
import { useIndicatorsByCategory, useDownloadCSV } from '../hooks/useApi'
import { Card, SectionTitle, DataSource } from '../components/UI'

const CATEGORY_COPY: Record<string, { title: string; subtitle: string; source: string; url: string }> = {
  housing: { title: 'Housing', subtitle: 'Affordability, inventory, and construction activity for Volusia County', source: 'US Census ACS / Local MLS', url: 'https://www.census.gov/topics/housing.html' },
  education: { title: 'Education', subtitle: 'Enrollment, outcomes, and funding for Volusia County schools and colleges', source: 'FL Dept of Education / NCES', url: 'https://www.fldoe.org/' },
  environment: { title: 'Environment', subtitle: 'Air quality, water quality, and land cover across Volusia County', source: 'EPA / NOAA / FDEP', url: 'https://www.epa.gov/' },
  'public safety': { title: 'Public Safety', subtitle: 'Crime, emergency response, and resiliency metrics for Volusia County', source: 'FBI UCR / FL Dept of Law Enforcement', url: 'https://www.fdle.state.fl.us/' },
  transportation: { title: 'Transportation', subtitle: 'Congestion, commute patterns, and infrastructure for Volusia County', source: 'FDOT / Volusia County MPO', url: 'https://www.fdot.gov/' },
  'government finance': { title: 'Government Finance', subtitle: 'Budget, revenue, and fiscal health for Volusia County', source: 'OpenGov / County Budget Office', url: 'https://www.volusia.org/budget' },
}

export function CategoryPage({ category }: { category: string }) {
  const { data, loading } = useIndicatorsByCategory(category)
  const downloadCSV = useDownloadCSV(category)
  const meta = CATEGORY_COPY[category.toLowerCase()] || { title: category, subtitle: '', source: '', url: '' }
  const indicators = useMemo(() => data?.indicators ?? data ?? [], [data])
  const top = useMemo(() => indicators.slice(0, 6), [indicators])

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <SectionTitle title={meta.title} subtitle={meta.subtitle} />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {loading ? (
          Array.from({ length: 3 }).map((_, i) => <div key={i} className="stat-card animate-pulse bg-gray-100 h-24" />)
        ) : (
          top.map((item: any) => (
            <Card key={item.name}>
              <div className="text-xs text-volusia-slate">{item.name}</div>
              <div className="text-2xl font-bold text-volusia-navy mt-1">{item.value ?? '—'}</div>
              <div className="text-xs text-gray-500 mt-1">{item.source ?? meta.source} · {item.vintage ?? ''}</div>
            </Card>
          ))
        )}
      </div>

      <Card className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-volusia-navy">All Indicators</h3>
          <button className="btn-primary text-sm py-1.5 px-3" onClick={downloadCSV}>Download CSV</button>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-2 px-3 text-volusia-slate">Name</th>
                <th className="text-left py-2 px-3 text-volusia-slate">Value</th>
                <th className="text-left py-2 px-3 text-volusia-slate">Unit</th>
                <th className="text-left py-2 px-3 text-volusia-slate">Source</th>
                <th className="text-left py-2 px-3 text-volusia-slate">Vintage</th>
              </tr>
            </thead>
            <tbody>
              {indicators.map((item: any) => (
                <tr key={item.name} className="border-b border-gray-100">
                  <td className="py-2 px-3 text-volusia-navy">{item.name}</td>
                  <td className="py-2 px-3">{item.value ?? '—'}</td>
                  <td className="py-2 px-3 text-gray-500">{item.unit ?? ''}</td>
                  <td className="py-2 px-3 text-gray-500">{item.source ?? ''}</td>
                  <td className="py-2 px-3 text-gray-500">{item.vintage ?? ''}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <DataSource source={meta.source} url={meta.url} vintage="2026" />
      </Card>
    </div>
  )
}
