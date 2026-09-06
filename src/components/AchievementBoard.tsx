import { useGamification } from '../hooks/useGamification'
import { Card, SectionTitle, Badge } from './UI'

interface Achievement {
  id: string
  name: string
  desc: string
  icon: string
  xp: number
  unlocked: boolean
}

interface AchievementBoardProps {
  userId: string
}

export function AchievementBoard({ userId }: AchievementBoardProps) {
  const { achievements, unlockedCount, totalAchievements, loading } = useGamification(userId)

  if (loading) {
    return <div className="text-sm text-gray-500 animate-pulse">Loading achievements…</div>
  }

  return (
    <div>
      <SectionTitle title="Achievements" subtitle={`${unlockedCount} of ${totalAchievements} unlocked`} />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {achievements.map((ach) => (
          <Card
            key={ach.id}
            className={`p-4 ${ach.unlocked ? 'bg-volusia-navy text-white' : 'bg-gray-100 grayscale'}`}
          >
            <div className="flex items-start gap-3">
              <span className="text-2xl">{ach.icon}</span>
              <div>
                <div className="font-bold">{ach.name}</div>
                <div className={`text-sm ${ach.unlocked ? 'text-gray-300' : 'text-gray-400'}`}>
                  {ach.desc}
                </div>
                <Badge variant={ach.unlocked ? 'warning' : 'default'} className="mt-2">
                  {ach.xp} XP
                </Badge>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}