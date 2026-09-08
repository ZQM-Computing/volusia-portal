import { useState } from 'react'
import { useGamification, useLeaderboard } from '../hooks/useApi'
import { Card, SectionTitle, Badge } from '../components/UI'

export function GamificationPage() {
  const { data: profile, loading, visitPage } = useGamification()
  const { data: leaderboard } = useLeaderboard()
  const [visited, setVisited] = useState(false)

  const handleVisit = () => {
    if (!visited) {
      visitPage()
      setVisited(true)
    }
  }

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-48" />
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[1,2,3,4].map(i => <div key={i} className="h-32 bg-gray-200 rounded-lg" />)}
          </div>
        </div>
      </div>
    )
  }

  const levelThresholds = [0, 100, 500, 1500, 5000]
  const currentLevelIndex = levelThresholds.findIndex((t, i) => i > 0 && (profile?.total_xp || 0) < t) - 1
  const currentThreshold = levelThresholds[Math.max(0, currentLevelIndex >= 0 ? currentLevelIndex : 0)]
  const nextThreshold = levelThresholds[Math.min(currentLevelIndex + 1, levelThresholds.length - 1)]
  const xpInLevel = (profile?.total_xp || 0) - currentThreshold
  const xpToNext = nextThreshold - currentThreshold
  const progressPercent = nextThreshold > currentThreshold ? Math.round((xpInLevel / xpToNext) * 100) : 100

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <SectionTitle title="Gamification Hub" subtitle="Earn XP, level up, and climb the leaderboard by exploring Volusia data" />

      <Card className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-2xl font-bold text-volusia-navy">
              Welcome, {profile?.user_id === 'anonymous' ? 'Explorer' : profile?.user_id}
            </h3>
            {profile?.total_xp === undefined && <p className="text-volusia-slate text-sm mt-1">Connect your profile to track progress</p>}
            <p className="text-volusia-slate mt-1">Level {profile?.level} · {profile?.total_xp || 0} XP</p>
          </div>
          <button onClick={handleVisit} className="btn-primary">
            Visit Page (+3 XP)
          </button>
        </div>

        <div className="mt-4 w-full bg-gray-200 rounded-full h-4 overflow-hidden">
          <div
            className="bg-gradient-to-r from-volusia-teal to-volusia-blue h-4 rounded-full transition-all duration-700 ease-out"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
        <p className="text-xs text-volusia-slate mt-1">{xpInLevel} / {xpToNext} XP to Level {nextThreshold > 0 ? Math.min(currentLevelIndex + 2, 5) : 1}</p>
      </Card>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="stat-card">
          <div className="stat-value">{profile?.level || 1}</div>
          <div className="stat-label">Your Level</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{profile?.total_xp || 0}</div>
          <div className="stat-label">Total XP</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{profile?.streak_days || 0}</div>
          <div className="stat-label">Day Streak</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{leaderboard?.length || 0}</div>
          <div className="stat-label">Leaderboard Entries</div>
        </div>
      </div>

      <SectionTitle title="Leaderboard" subtitle="Top explorers by XP" />
      <Card>
        {leaderboard && leaderboard.length > 0 ? (
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-semibold text-volusia-navy">Rank</th>
                <th className="text-left py-3 px-4 font-semibold text-volusia-navy">User</th>
                <th className="text-left py-3 px-4 font-semibold text-volusia-navy">XP</th>
                <th className="text-left py-3 px-4 font-semibold text-volusia-navy">Level</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((entry: any, i: number) => (
                <tr key={entry.user_id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 font-bold text-volusia-teal">{i + 1}</td>
                  <td className="py-3 px-4">{entry.user_id}</td>
                  <td className="py-3 px-4">{entry.total_xp}</td>
                  <td className="py-3 px-4">{entry.level}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="py-8 text-center text-volusia-slate">No entries yet. Be the first to explore!</p>
        )}
      </Card>
    </div>
  )
}
