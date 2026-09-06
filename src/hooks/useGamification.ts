import { useState } from 'react'
import { useApiData } from '../hooks/useApi'

interface Achievement {
  id: string
  name: string
  desc: string
  icon: string
  xp: number
  unlocked: boolean
}

interface Profile {
  user_id: string
  total_xp: number
  level: number
  streak_days: number
  last_active_date: number
  pages_visited: string[]
  achievements_unlocked: string[]
  indicators_viewed: number
  datasets_downloaded: number
  refresh_triggered: number
}

interface LeaderboardEntry {
  user_id: string
  total_xp: number
  level: number
  streak_days: number
  indicators_viewed: number
  datasets_downloaded: number
}

interface HistoryEntry {
  event_type: string
  detail: string
  xp_earned: number
  timestamp: number
}

interface VisitResult {
  xp_earned: number
  streak_bonus_days: number
  level: number
  new_achievements: { id: string; name: string; desc: string; icon: string; xp: number }[]
}

export function useGamification(userId: string) {
  const { data: profile, loading: profileLoading } = useApiData<Profile>(`/gamification/profile/${userId}`)
  const { data: achievements } = useApiData<{ achievements: Achievement[]; unlocked_count: number; total_count: number }>(`/gamification/achievements/${userId}`)
  const { data: history } = useApiData<{ history: HistoryEntry[] }>(`/gamification/history/${userId}`)
  const { data: leaderboard } = useApiData<{ leaderboard: LeaderboardEntry[]; count: number }>('/gamification/leaderboard')
  const [visitResult, setVisitResult] = useState<VisitResult | null>(null)

  const visitPage = async (page: string) => {
    const res = await fetch(`/api/gamification/visit/${userId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ page }),
    })
    const data = await res.json()
    setVisitResult(data)
    return data
  }

  const addXP = async (action: string, source: string = '') => {
    const res = await fetch(`/api/gamification/xp/${userId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, source }),
    })
    return res.json()
  }

  return {
    profile,
    achievements: achievements?.achievements ?? [],
    unlockedCount: achievements?.unlocked_count ?? 0,
    totalAchievements: achievements?.total_count ?? 0,
    history: history?.history ?? [],
    leaderboard: leaderboard?.leaderboard ?? [],
    leaderboardCount: leaderboard?.count ?? 0,
    visitResult,
    visitPage,
    addXP,
    loading: profileLoading,
  }
}