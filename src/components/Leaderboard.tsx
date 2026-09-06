import { useGamification } from '../hooks/useGamification'
import { Card, SectionTitle } from './UI'

interface LeaderboardEntry {
  user_id: string
  total_xp: number
  level: number
  streak_days: number
  indicators_viewed: number
  datasets_downloaded: number
}

export function Leaderboard() {
  const { leaderboard, leaderboardCount, loading } = useGamification('anonymous')
  const entries: LeaderboardEntry[] = leaderboard ?? []

  if (loading) {
    return <div className="text-sm text-gray-500 animate-pulse">Loading leaderboard…</div>
  }

  const medal = (idx: number) => {
    if (idx === 0) return '🥇'
    if (idx === 1) return '🥈'
    if (idx === 2) return '🥉'
    return `${idx + 1}`
  }

  return (
    <div>
      <SectionTitle title="Leaderboard" subtitle="Top contributors by XP" />
      <div className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-100">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rank</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Level</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">XP</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">🔥 Streak</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Explored</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {entries.map((entry, idx) => (
              <tr key={entry.user_id} className={idx === 0 ? 'bg-volusia-navy text-white' : 'hover:bg-gray-50'}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">{medal(idx)}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{entry.user_id}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">Lv.{entry.level}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{entry.total_xp.toLocaleString()}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{entry.streak_days}d</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">{entry.indicators_viewed}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {entries.length === 0 && (
          <div className="px-6 py-8 text-center text-sm text-gray-500">
            No entries yet. Be the first to explore!
          </div>
        )}
      </div>
    </div>
  )
}