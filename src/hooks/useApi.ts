import { useState, useEffect } from 'react'

const API_BASE = ''

// Generic hook for static JSON data
export function useApiData<T>(endpoint: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  useEffect(() => {
    fetch(`${API_BASE}${endpoint}`)
      .then((res) => { if (!res.ok) throw new Error(`HTTP ${res.status}`); return res.json() })
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [endpoint])
  return { data, loading, error }
}

// Category-specific hooks (static JSON files from /data/)
export function useAllIndicators() { return useApiData<any>('/indicators.json') }
export function useEconomicIndicators() { return useApiData<any>('/economic.json') }
export function useDemographicIndicators() { return useApiData<any>('/demographics.json') }
export function useClimateIndicators() { return useApiData<any>('/climate.json') }
export function useDatasets() { return useApiData<any>('/datasets.json') }
export function useMapLayers() { return useApiData<any>('/map-layers.json') }
export function useNews() { return useApiData<any>('/news.json') }
export function useHealth() { return useApiData<any>('/health.json') }
export function useStakeholderGroups() { return useApiData<any>('/stakeholders.json') }
export function useDownloadCSV(category?: string) {
  const url = category ? `/api/indicators.csv?category=${category}` : '/api/indicators.csv'
  return () => window.open(url, '_blank')
}
export function useIndicator(name: string) { return useApiData<any>(`/indicators/${encodeURIComponent(name)}`) }
export function useIndicatorList() { return useApiData<any>('/indicators.json') }

// Gamification hooks (dynamic API via /api/)
interface GamificationState {
  data: any
  loading: boolean
  visitPage: () => void
  pulse: any[]
}

export function useGamification(userId: string = 'anonymous'): GamificationState {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [pulse, setPulse] = useState<any[]>([])

  const visitPage = () => {
    fetch(`/api/gamification/visit/${userId}`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({page: window.location.pathname}) })
      .then((res) => res.json())
      .then(setData)
      .catch(() => {})
  }

  useEffect(() => {
    fetch('/api/pulse.json')
      .then((res) => res.json())
      .then(setPulse)
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return { data, loading, visitPage, pulse }
}

interface GamificationStatsState {
  stats: any
  totalUsers: number
  avgXp: number
  avgLevel: number
  loading: boolean
}

export function useGamificationStats(userId: string): GamificationStatsState {
  const [stats, setStats] = useState<any>(null)
  const [totalUsers, setTotalUsers] = useState(0)
  const [avgXp, setAvgXp] = useState(0)
  const [avgLevel, setAvgLevel] = useState(0)
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    fetch(`/api/gamification/stats/${userId}`)
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

export function useLeaderboard() { return useApiData<any>('/gamification/leaderboard') }

export function useDiagnostics() {
  const [diagnostics, setDiagnostics] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    fetch('/api/diagnostics')
      .then((res) => res.json())
      .then((d) => { setDiagnostics(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])
  return { diagnostics, loading }
}
