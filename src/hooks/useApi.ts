import { useState, useEffect } from 'react'

const API_BASE = '/data'

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

export function useAllIndicators() { return useApiData<any>('/indicators.json') }
export function useEconomicIndicators() { return useApiData<any>('/economic.json') }
export function useDemographicIndicators() { return useApiData<any>('/demographics.json') }
export function useClimateIndicators() { return useApiData<any>('/climate.json') }
export function useDatasets() { return useApiData<any>('/datasets.json') }
export function useMapLayers() { return useApiData<any>('/map-layers.json') }
export function useNews() { return useApiData<any>('/news.json') }
export function useHealth() { return useApiData<any>('/health.json') }
export function useDownloadCSV(category?: string) {
  const url = category ? `/data/indicators.csv?category=${category}` : '/data/indicators.csv'
  return () => window.open(url, '_blank')
}
export function useIndicator(name: string) { return useApiData<any>(`/indicators/${encodeURIComponent(name)}`) }
