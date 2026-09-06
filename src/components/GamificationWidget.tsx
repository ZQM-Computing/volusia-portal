import { useState } from 'react'
import { useGamification } from '../hooks/useGamification'
import { Card, SectionTitle, Badge } from './UI'

interface GamificationWidgetProps {
  userId: string
}

export function GamificationWidget({ userId }: GamificationWidgetProps) {
  const { profile, visitPage, loading } = useGamification(userId)
  const [visited, setVisited] = useState<string[]>([])

  const handleVisit = async (page: string) => {
    const result = await visitPage(page)
    if (result?.xp_earned) {
      setVisited(prev => [...prev, page])
    }
  }

  if (loading || !profile) {
    return <div className="text-sm text-gray-500 animate-pulse">Loading profile…</div>
  }

  return (
    <Card>
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-full bg-volusia-gold flex items-center justify-center text-volusia-navy font-bold text-lg">
          {profile.level}
        </div>
        <div>
          <div className="font-bold text-volusia-navy">Level {profile.level}</div>
          <div className="text-sm text-volusia-slate">{profile.total_xp} XP</div>
        </div>
        <Badge variant={profile.streak_days >= 3 ? 'warning' : profile.streak_days >= 1 ? 'success' : 'default'}>
          🔥 {profile.streak_days}d streak
        </Badge>
      </div>
      <div className="grid grid-cols-3 gap-2 text-center text-sm">
        <div>
          <div className="font-bold text-volusia-navy">{profile.indicators_viewed}</div>
          <div className="text-gray-500">Explored</div>
        </div>
        <div>
          <div className="font-bold text-volusia-navy">{profile.datasets_downloaded}</div>
          <div className="text-gray-500">Downloaded</div>
        </div>
        <div>
          <div className="font-bold text-volusia-navy">{profile.achievements_unlocked?.length ?? 0}</div>
          <div className="text-gray-500">Earned</div>
        </div>
      </div>
    </Card>
  )
}