import { useState } from 'react'
import { useState } from 'react'
import { useGamification } from '../hooks/useGamification'
import { Card, SectionTitle, Badge } from './UI'

interface GamificationWidgetProps {
  userId: string
  showXP?: boolean
  showAchievements?: boolean
}

export function GamificationWidget({ userId, showXP = true, showAchievements = true }: GamificationWidgetProps) {
  const { profile, visitPage, loading } = useGamification(userId)
  const [visited, setVisited] = useState<string[]>([])
  const [xpEarned, setXpEarned] = useState(0)

  const handleVisit = async (page: string) => {
    const result = await visitPage(page)
    if (result?.xp_earned) {
      setVisited(prev => [...prev, page])
      setXpEarned(prev => prev + result.xp_earned)
    }
  }

  if (loading || !profile) {
    return <div className="text-sm text-gray-500 animate-pulse">Loading profile…</div>
  }

  return (
    <Card className="p-6 shadow-sm">
      <div className="flex items-center gap-4 mb-6">
        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-volusia-gold via-volusia-teal to-volusia-navy flex items-center justify-center text-volusia-gold font-bold text-xl">
          {profile.level}
        </div>
        <div>
          <div className="font-bold text-volusia-navy">Level {profile.level}</div>
          {showXP && <div className="text-sm text-volusia-slate">{profile.total_xp} XP</div>}
        </div>
      </div>

      {/* Streak indicator */}
      {profile.streak_days > 0 && (
        <div className="mb-4">
          <Badge variant="warning">
            🔥 {profile.streak_days} day{'s'.repeat(profile.streak_days > 1)} streak
          </Badge>
        </div>
      )}

      {/* Key stats grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-center text-sm">
        <div>
          <div className="font-bold text-volusia-navy">{profile.indicators_viewed}</div>
          <div className="text-gray-500 mt-1">Explored</div>
        </div>
        <div>
          <div className="font-bold text-volusia-navy">{profile.datasets_downloaded}</div>
          <div className="text-gray-500 mt-1">Downloaded</div>
        </div>
        {showAchievements && (
          <div>
            <div className="font-bold text-volusia-navy">{profile.achievements_unlocked?.length ?? 0}</div>
            <div className="text-gray-500 mt-1">Earned</div>
          </div>
        )}
      </div>

      {/* XP progress and page visits */}
      {showXP && (
        <div className="mt-6 pt-4 border-t border-gray-200">
          <p className="text-sm text-volusia-slate mb-2">Pages visited for XP</p>
          <div className="grid grid-cols-2 gap-2">
            {visited.map((page) => (
              <div key={page} className="bg-volusia-teal/10 rounded p-2 text-center">
                <div className="font-bold text-volusia-navy">{page}</div>
                <div className="text-xs text-volusia-gold">+3 XP</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </Card>
  )
}