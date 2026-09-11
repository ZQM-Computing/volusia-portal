import { useState, useEffect, useCallback } from 'react'

const API_BASE = ''

function useApiData<T>(endpoint: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const fetchData = useCallback(() => {
    setLoading(true)
    setError(null)
    fetch(`${API_BASE}${endpoint}`)
      .then((res) => { if (!res.ok) throw new Error(`HTTP ${res.status}`); return res.json() })
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [endpoint])
  useEffect(() => { fetchData() }, [fetchData])
  return { data, loading, error, refetch: fetchData }
}

// Category → cache file name mapping (cache files use kebab-case,
// but category names use spaces — map so routes resolve)
function categoryToCacheFile(category: string): string {
  return category.toLowerCase().replace(/\s+/g, '-')
}

export function useAllIndicators() { return useApiData<any>('/data/indicators.json') }
export function useEconomicIndicators() { return useApiData<any>('/data/economic.json') }
export function useDemographicIndicators() { return useApiData<any>('/data/demographics.json') }
export function useClimateIndicators() { return useApiData<any>('/data/climate.json') }
export function useTourismIndicators() { return useApiData<any>('/data/tourism.json') }
export function useDatasets() { return useApiData<any>('/data/datasets.json') }
export function useMapLayers() { return useApiData<any>('/data/map-layers.json') }
export function useNews() { return useApiData<any>('/data/news.json') }
export function useHealth() { return useApiData<any>('/data/health.json') }
export function useStakeholderGroups() { return useApiData<any>('/data/stakeholders.json') }
export function useIndicatorsByCategory(category: string) {
  const key = categoryToCacheFile(category)
  return useApiData<any>(`/data/${encodeURIComponent(key)}.json`)
}
export function useIndicator(name: string) { return useApiData<any>(`/indicators/${encodeURIComponent(name)}`) }
export function useIndicatorList() { return useApiData<any>('/data/indicators.json') }
export function useDownloadCSV(category?: string) {
  const url = category ? `/api/indicators.csv?category=${encodeURIComponent(category)}` : '/api/indicators.csv'
  return () => { if (typeof window !== 'undefined') window.open(url, '_blank') }
}

export function useGamification(userId: string = 'anonymous') {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [pulse, setPulse] = useState<any[]>([])
  const visitPage = useCallback(() => {
    fetch(`/api/gamification/visit/${encodeURIComponent(userId)}`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({page: typeof window !== 'undefined' ? window.location.pathname : '/'}) })
      .then((res) => res.json())
      .then(setData)
      .catch(() => {})
  }, [userId])
  useEffect(() => {
    fetch('/api/pulse.json')
      .then((res) => res.json())
      .then(setPulse)
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [userId])
  return { data, loading, visitPage, pulse }
}

export function useGamificationStats(userId: string) {
  const [stats, setStats] = useState<any>(null)
  const [totalUsers, setTotalUsers] = useState(0)
  const [avgXp, setAvgXp] = useState(0)
  const [avgLevel, setAvgLevel] = useState(0)
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    fetch(`/api/gamification/stats/${encodeURIComponent(userId)}`)
      .then((res) => res.json())
      .then((d) => {
        setStats(d)
        setTotalUsers(d.total_users || 0)
        setAvgXp(d.avg_xp || 0)
        setAvgLevel(d.avg_level || 0)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [userId])
  return { stats, totalUsers, avgXp, avgLevel, loading }
}

export function useLeaderboard() {
  const { data, loading, error, refetch } = useApiData<any>('/gamification/leaderboard')
  const leaderboardData = data?.leaderboard ?? data ?? []
  const leaderboardCount = data?.count ?? (Array.isArray(leaderboardData) ? leaderboardData.length : 0)
  return { data: leaderboardData, loading, error, refetch, count: leaderboardCount }
}

export function useDiagnostics() {
  const { data, loading, error, refetch } = useApiData<any>('/api/diagnostics')
  return { diagnostics: data, loading, error, refetch }
}

// Helper: find indicator by name
export function getIndicator(items: any[] | null, name: string) {
  if (!items) return null
  return items.find((i: any) => i.name === name) ?? null
}
