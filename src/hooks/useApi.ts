import { useState, useEffect } from 'react'

const API_BASE = 'http://localhost:8000'

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
  return useApiData<Record<string, any>>('/indicators')
}

export function useEconomicIndicators() {
  return useApiData<Record<string, any>>('/indicators/economic')
}

export function useDemographicIndicators() {
  return useApiData<any>('/indicators/demographics')
}

export function useHousingIndicators() {
  return useApiData<Record<string, any>>('/indicators/housing')
}

export function useWeatherIndicators() {
  return useApiData<Record<string, any>>('/indicators/weather')
}
