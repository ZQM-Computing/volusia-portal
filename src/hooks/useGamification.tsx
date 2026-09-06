import { useState, useEffect, createContext, useContext } from 'react'
import { useApiData } from './useApi'
import type {
  GamificationProfile,
  ContributorReputation,
  LeaderboardEntry,
  PulseItem,
  QualityTier,
} from '../types'

const GAMIFICATION_API = '/gamification'

interface GamificationContextType {
  profile: GamificationProfile | null
  leaderboard: LeaderboardEntry[]
  pulse: PulseItem[]
  loading: boolean
  refresh: () => void
}

export const GamificationContext = createContext<GamificationContextType>({
  profile: null,
  leaderboard: [],
  pulse: [],
  loading: true,
  refresh: () => {},
})

export function GamificationProvider({ children }: { children: React.ReactNode }) {
  const [loading, setLoading] = useState(true)
  const [profile, setProfile] = useState<GamificationProfile | null>(null)
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([])
  const [pulse, setPulse] = useState<PulseItem[]>([])

  const refresh = () => {
    setLoading(true)
    Promise.all([
      fetch(`${GAMIFICATION_API}/profile/zqmco`).then((r) => r.json()).catch(() => null),
      fetch(`${GAMIFICATION_API}/leaderboard?limit=10`).then((r) => r.json()).catch(() => ({ entries: [] })),
      fetch(`${GAMIFICATION_API}/pulse`).then((r) => r.json()).catch(() => ({ items: [] })),
    ]).then(([p, lb, pl]) => {
      setProfile(p)
      setLeaderboard(lb.entries || [])
      setPulse(pl.items || [])
      setLoading(false)
    }).catch(() => setLoading(false))
  }

  useEffect(() => { refresh() }, [])

  return (
    <GamificationContext.Provider value={{ profile, leaderboard, pulse, loading, refresh }}>
      {children}
    </GamificationContext.Provider>
  )
}

export function useGamification() {
  return useContext(GamificationContext)
}

export function useContributor(contributorId: string) {
  const { data: reputation } = useApiData<ContributorReputation>(
    `${GAMIFICATION_API}/reputation/${contributorId}`
  )
  const { data: quality } = useApiData<{ quality_score: { overall: number; tier: QualityTier } }>(
    `${GAMIFICATION_API}/quality?contributor_id=${contributorId}`
  )
  return { reputation, quality }
}

export function tierColor(tier: QualityTier): string {
  switch (tier) {
    case 'verified': return 'text-green-600 bg-green-100'
    case 'reviewed': return 'text-blue-600 bg-blue-100'
    case 'pending': return 'text-gray-600 bg-gray-100'
    case 'flagged': return 'text-red-600 bg-red-100'
  }
}

export function tierBadge(tier: QualityTier): string {
  switch (tier) {
    case 'verified': return '[Verified]'
    case 'reviewed': return '[Reviewed]'
    case 'pending': return '[Pending]'
    case 'flagged': return '[Flagged]'
  }
}