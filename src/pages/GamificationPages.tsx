import { Link } from 'react-router-dom'
import { useGamification, tierBadge, tierColor } from '../hooks/useGamification'
import type { LeaderboardEntry } from '../types'

export function ProfilePage() {
  const { profile, loading } = useGamification()

  if (loading || !profile) {
    return <div className="max-w-7xl mx-auto px-4 py-8 text-volusia-slate">Loading profile...</div>
  }

  const { reputation, current_streak, best_streak, badges, quality_tier } = profile

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h2 className="text-3xl font-bold text-volusia-navy mb-2 font-display">Your Profile</h2>
      <p className="text-volusia-slate mb-8">Track your contributions, reputation, and standing in the Volusia intelligence network.</p>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Identity card */}
        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100 lg:col-span-1">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-14 h-14 rounded-full bg-volusia-teal flex items-center justify-center text-white font-bold text-xl">
              {profile.contributor_id.charAt(0).toUpperCase()}
            </div>
            <div>
              <div className="font-bold text-volusia-navy">{profile.contributor_id}</div>
              <span className={`text-xs px-2 py-0.5 rounded-full ${tierColor(quality_tier)}`}>
                {tierBadge(quality_tier)}
              </span>
            </div>
          </div>
          <div className="space-y-2 text-sm text-volusia-slate">
            <div>Verified contributions: <span className="font-medium text-volusia-navy">{reputation.verified_contributions}</span></div>
            <div>Total submissions: <span className="font-medium text-volusia-navy">{reputation.total_submissions}</span></div>
            <div>Accuracy rate: <span className="font-medium text-volusia-navy">{(reputation.accuracy_rate * 100).toFixed(1)}%</span></div>
            <div>Current streak: <span className="font-medium text-volusia-navy">{current_streak} days</span></div>
            <div>Best streak: <span className="font-medium text-volusia-navy">{best_streak} days</span></div>
          </div>
        </div>

        {/* Badges */}
        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100 lg:col-span-2">
          <h3 className="text-lg font-semibold text-volusia-navy mb-4">Badges</h3>
          {badges.length === 0 ? (
            <p className="text-sm text-gray-400">No badges yet. Contribute to earn your first.</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {badges.map((badge) => (
                <span key={badge} className="inline-flex items-center gap-1 text-sm bg-volusia-gold/10 text-volusia-gold px-3 py-1.5 rounded-full border border-volusia-gold/20">
                  {badge}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Contribution breakdown by pathway */}
      <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100 mb-8">
        <h3 className="text-lg font-semibold text-volusia-navy mb-4">Contributions by Pathway</h3>
        {Object.entries(reputation.contribution_count_by_pathway).length === 0 ? (
          <p className="text-sm text-gray-400">No contributions yet. Submit your first contribution to see pathway breakdown.</p>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {Object.entries(reputation.contribution_count_by_pathway).map(([pathway, count]) => (
              <div key={pathway} className="bg-gray-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-volusia-teal">{count}</div>
                <div className="text-xs text-volusia-slate mt-1 capitalize">{pathway.replace(/_/g, ' ')}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export function LeaderboardPage() {
  const { leaderboard, loading } = useGamification()

  if (loading) {
    return <div className="max-w-7xl mx-auto px-4 py-8 text-volusia-slate">Loading leaderboard...</div>
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h2 className="text-3xl font-bold text-volusia-navy mb-2 font-display">Leaderboard</h2>
      <p className="text-volusia-slate mb-8">Top contributors ranked by quality score. Quality gates every entry.</p>
      <div className="bg-white rounded-xl shadow-md border border-gray-100 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-100">
              <th className="text-left px-4 py-3 text-sm font-medium text-volusia-slate">Rank</th>
              <th className="text-left px-4 py-3 text-sm font-medium text-volusia-slate">Contributor</th>
              <th className="text-right px-4 py-3 text-sm font-medium text-volusia-slate">Score</th>
              <th className="text-right px-4 py-3 text-sm font-medium text-volusia-slate">Verified</th>
              <th className="text-right px-4 py-3 text-sm font-medium text-volusia-slate">Streak</th>
              <th className="text-center px-4 py-3 text-sm font-medium text-volusia-slate">Tier</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry) => (
              <tr key={entry.contributor_id} className="border-b border-gray-50 hover:bg-gray-50">
                <td className="px-4 py-3 text-sm font-medium text-volusia-navy">#{entry.rank}</td>
                <td className="px-4 py-3 text-sm text-volusia-navy">{entry.contributor_id}</td>
                <td className="px-4 py-3 text-right text-sm font-medium text-volusia-teal">{entry.score.toFixed(1)}</td>
                <td className="px-4 py-3 text-right text-sm text-volusia-slate">{entry.verified_contributions}</td>
                <td className="px-4 py-3 text-right text-sm text-volusia-slate">{entry.current_streak}</td>
                <td className="px-4 py-3 text-center">
                  <span className={`text-xs px-2 py-0.5 rounded-full ${tierColor(entry.quality_tier)}`}>
                    {entry.quality_tier}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export function PulsePage() {
  const { pulse, loading } = useGamification()

  if (loading) {
    return <div className="max-w-7xl mx-auto px-4 py-8 text-volusia-slate">Loading pulse feed...</div>
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h2 className="text-3xl font-bold text-volusia-navy mb-2 font-display">Volusia Pulse</h2>
      <p className="text-volusia-slate mb-8">Indicators that moved this week. Real-time signals for every constituency.</p>
      {pulse.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-8 border border-gray-100 text-center text-volusia-slate">
          No significant changes detected yet. Check back as new data refreshes.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {pulse.map((item) => {
            const dirIcon = item.direction === 'up' ? '↑' : item.direction === 'down' ? '↓' : '→'
            const dirColor = item.direction === 'up' ? 'text-green-600' : item.direction === 'down' ? 'text-red-600' : 'text-gray-500'
            return (
              <div key={item.indicator_id} className="bg-white rounded-xl shadow-md p-5 border border-gray-100">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-medium text-volusia-slate uppercase">{item.category}</span>
                  <span className={`text-lg font-bold ${dirColor}`}>{dirIcon} {Math.abs(item.delta_pct).toFixed(1)}%</span>
                </div>
                <div className="font-semibold text-volusia-navy">{item.name}</div>
                <div className="text-xs text-gray-400 mt-1">
                  {String(item.old_value)} → {String(item.new_value)}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}