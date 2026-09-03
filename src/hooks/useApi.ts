import { useState, useEffect } from 'react'

const API_BASE = '/data'

export function useApiData<T>(endpoint: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch(`${API_BASE}${endpoint}`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [endpoint])

  return { data, loading, error }
}

export function useAllIndicators() {
  return useApiData<any>('indicators.json')
}

export function useEconomicIndicators() {
  return useApiData<any>('economic.json')
}

export function useDemographicIndicators() {
  return useApiData<any>('demographics.json')
}

export function useHousingIndicators() {
  return useApiData<any>('housing.json')
}

export function useWeatherIndicators() {
  return useApiData<any>('climate.json')
}
