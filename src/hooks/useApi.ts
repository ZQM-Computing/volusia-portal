import { useState, useEffect } from 'react'

const API_BASE = ''

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

export function useAllIndicators() { return useApiData<any>('/indicators') }
export function useEconomicIndicators() { return useApiData<any>('/indicators?category=Economic') }
export function useDemographicIndicators() { return useApiData<any>('/indicators?category=Demographics') }
export function useClimateIndicators() { return useApiData<any>('/indicators?category=Climate') }
export function useDatasets() { return useApiData<any>('/datasets') }
export function useMapLayers() { return useApiData<any>('/map-layers') }
export function useGamification(userId: string) {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const visitPage = () => {
    fetch(`/gamification/visit/${userId}`, { method: 'POST' })
      .then((res) => res.json())
      .then(setData)
      .catch(() => {})
  }
  return { data, loading, visitPage }
}
export function useGamificationStats(userId: string) {
  const [stats, setStats] = useState<any>(null)
  const [totalUsers, setTotalUsers] = useState(0)
  const [avgXp, setAvgXp] = useState(0)
  const [avgLevel, setAvgLevel] = useState(0)
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    fetch(`/gamification/stats/${userId}`)
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
export function useDownloadCSV(category?: string) {
  const url = category ? `/indicators.csv?category=${category}` : '/indicators.csv'
  return () => window.open(url, '_blank')
}
export function useIndicator(name: string) {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    fetch(`/indicators/${name}`)
      .then((res) => res.json())
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [name])
  return { data, loading }
}
