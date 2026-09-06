import { useState, useEffect } from 'react'

const API_BASE = '/api'

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
export function useDownloadCSV(category?: string) {
  const url = category ? `/api/indicators.csv?category=${category}` : '/api/indicators.csv'
  return () => window.open(url, '_blank')
}
export function useDatasets() { return useApiData<any>('/datasets') }
export function useIndicator(name: string) { return useApiData<any>(`/indicators/${encodeURIComponent(name)}`) }
export function useMapLayers() { return useApiData<any>('/map-layers') }
