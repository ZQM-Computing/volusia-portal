export interface Indicator {
  id: string
  name: string
  category: 'economic' | 'tourism' | 'real_estate' | 'demographic' | 'transportation' | 'climate' | 'safety' | 'health' | 'education' | 'finance'
  value: number | string
  unit: string
  change: number | null
  changeLabel: string | null
  vintage: string
  source: string
  sourceUrl: string
  description: string
  trendData?: { x: string; y: number }[]
}

export interface Dataset {
  id: string
  name: string
  category: string
  description: string
  source: string
  sourceUrl: string
  format: string
  vintage: string
  license: string
  status: 'available' | 'gated' | 'missing' | 'in-development'
  lastUpdated: string
  downloads?: number
}

export interface MapLayer {
  id: string
  name: string
  category: 'boundary' | 'economic' | 'infrastructure' | 'environment' | 'demographic' | 'cultural'
  description: string
  source: string
  format: 'geojson' | 'shapefile' | 'raster' | 'point'
  url?: string
}

export interface StakeholderGroup {
  id: 'business' | 'residents' | 'tourists' | 'leaders'
  name: string
  description: string
  icon: string
  highlights: string[]
}

export interface NewsItem {
  id: string
  title: string
  summary: string
  date: string
  category: string
  url?: string
}
