import { Link } from 'react-router-dom'
import { useGamification } from '../hooks/useGamification'
import { GamificationWidget } from '../components/GamificationWidget'
import { AchievementBoard } from '../components/AchievementBoard'
import { Leaderboard } from '../components/Leaderboard'
import { Card, SectionTitle, Badge } from '../components/UI'
import { useState } from 'react'

const pages = [
  { to: '/', label: 'Portal Home', desc: 'View featured indicators and explore the portal' },
  { to: '/data', label: 'Data Explorer', desc: 'Browse all indicators and datasets' },
  { to: '/maps', label: 'Maps', desc: 'Explore geographic data layers' },
  { to: '/business', label: 'Business', desc: 'Business benchmarks and growth signals' },
  { to: '/residents', label: 'Residents', desc: 'Demographics and cost-of-living data' },
  { to: '/tourists', label: 'Tourists', desc: 'Visitor volume and hotel trends' },
  { to: '/leaders', label: 'Leaders', desc: 'Investment and workforce analytics' },
]

export function GamificationPage() {
  const { visitPage, profile, loading } = useGamification('anonymous')
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
    return <div className="max-w-7xl mx-auto px-4 py-8 text-sm text-gray-500 animate-pulse">Loading profile…</div>
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <SectionTitle
        title="Gamification"
        subtitle="Earn XP by exploring the portal — level up and unlock achievements"
      />

      {/* Hero */}
      <div className="bg-gradient-to-br from-volusia-navy via-volusia-teal to-volusia-gold text-white rounded-xl p-8 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
          <div>
            <div className="text-6xl font-bold mb-2">{profile.level}</div>
            <div className="text-lg opacity-90">Level</div>
          </div>
          <div>
            <div className="text-4xl font-bold mb-1">{profile.total_xp + xpEarned}</div>
            <div className="text-lg opacity-90">Total XP{xpEarned > 0 && ` (+${xpEarned} this session)`}</div>
          </div>
          <div>
            <div className="text-4xl font-bold mb-1">🔥 {profile.streak_days + (profile.streak_days >= 1 ? 1 : 0)}d</div>
            <div className="text-lg opacity-90">Streak</div>
          </div>
        </div>
      </div>

      {/* Explore pages for XP */}
      <Card className="mb-8">
        <h2 className="text-xl font-bold text-volusia-navy mb-4">Explore Pages to Earn XP</h2>
        <p className="text-sm text-volusia-slate mb-4">Visit each page once to earn 3 XP + streak bonuses</p>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {pages.map((page) => {
            const done = visited.includes(page.to)
            return (
              <button
                key={page.to}
                onClick={() => handleVisit(page.to)}
                disabled={done}
                className={`p-4 rounded-lg border text-left transition-colors ${
                  done
                    ? 'bg-green-50 border-green-200 cursor-default'
                    : 'bg-white border-gray-200 hover:border-volusia-teal hover:bg-green-50 cursor-pointer'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-semibold text-sm text-volusia-navy">{page.label}</div>
                    <div className="text-xs text-gray-500 mt-1">{page.desc}</div>
                  </div>
                  <span className="text-xs font-bold text-volusia-gold">+3 XP</span>
                </div>
                {done && <div className="text-xs text-green-600 mt-2">✓ Explored</div>}
              </button>
            )
          })}
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <AchievementBoard userId="anonymous" />
        <Leaderboard />
      </div>

      <div className="mt-8">
        <Link to="/" className="text-volusia-teal hover:underline text-sm">← Back to Portal Home</Link>
      </div>
    </div>
  )
}