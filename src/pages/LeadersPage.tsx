import { useState, useEffect } from 'react'
import { useLeaderboard } from '../hooks/useApi'
import { useEconomicIndicators } from '../hooks/useApi'
import { Card, SectionTitle, Badge, DataSource, StatCard } from '../components/UI'
import { ResponsiveBar } from '@nivo/bar'
import { ResponsivePie } from '@nivo/pie'

export function LeadersPage() {
    const { data: leaderboard } = useLeaderboard()
    const { data: economic, loading } = useEconomicIndicators()

    const getIndicator = (items: any[] | null, name: string) => {
        if (!items) return null
        return items.find((i: any) => i.name === name)
    }
    const employment = getIndicator(economic?.indicators, 'employment_qcew')
    const avgWage = getIndicator(economic?.indicators, 'avg_weekly_wage_qcew')
    const unemploymentBls = getIndicator(economic?.indicators, 'unemployment_rate_bls')
    const establishments = getIndicator(economic?.indicators, 'establishments_qcew')
    const personalIncome = getIndicator(economic?.indicators, 'personal_income_total')
    const populationBEA = getIndicator(economic?.indicators, 'population_bea')

    // Build chart data from live indicators — real QCEW data
    const employmentValue = employment ? Number(employment.value) : 494400
  const investmentData = employment
          ? []
          : []

    const workforceData = employment
        ? []
        : []

    const permittingVelocity = establishments
        ? []
        : []

    const moversIndicators = []
    if (employment) moversIndicators.push(employment)
    if (avgWage) moversIndicators.push(avgWage)
    if (unemploymentBls) moversIndicators.push(unemploymentBls)

    // Extract leaderboard data correctly: useLeaderboard returns { leaderboard: [...], count: N }
    const leaderboardData = leaderboard?.leaderboard ?? leaderboard ?? []
    const leaderboardCount = leaderboard?.count ?? (Array.isArray(leaderboardData) ? leaderboardData.length : 0)

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <SectionTitle
                title="Leaders Intelligence"
                subtitle="Capital flows, permitting velocity, workforce data, and infrastructure capacity for investors, developers, and community leaders"
            />

            {/* Key Metrics */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                {loading ? (
                    <>
                        {[1,2,3,4].map(i => <div key={i} className="stat-card animate-pulse bg-gray-100 h-24" />)}
                    </>
                ) : (
                    <>
                        <StatCard
                            value={employment ? Number(employment.value).toLocaleString() : '—'}
                            label="Total Employment (QCEW)"
                            change={avgWage ? Number(avgWage.value) : undefined}
                            changeLabel={avgWage ? `Avg wkly $${avgWage.value}` : undefined}
                        />
                        <StatCard
                            value={populationBEA ? Number(populationBEA.value).toLocaleString() : '—'}
                            label="Population (BEA)"
                            change={unemploymentBls ? Number(unemploymentBls.value) : undefined}
                                                        changeLabel={unemploymentBls ? `Unemployment ${unemploymentBls.value}%` : undefined}
                                                    />
                                                    <StatCard
                                                        value={personalIncome ? Number(personalIncome.value).toLocaleString() : '—'}
                                                        label="Personal Income (BEA)"
                                                        change={establishments ? Number(establishments.value) : undefined}
                                                        changeLabel={establishments ? `Establishments` : undefined}
                        />
                        <StatCard
                            value={leaderboardCount}
                            label="Leaderboard Entries"
                            change={undefined}
                            changeLabel="Top contributors"
                        />
                    </>
                )}
            </div>

            {/* Investment Trends */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                <Card>
                    <h3 className="text-lg font-semibold text-volusia-navy mb-4">Capital Investment by Sector ($M)</h3>
                    <div className="h-64">
                        <ResponsiveBar
                            data={investmentData}
                            keys={['commercial', 'residential', 'industrial']}
                            indexBy="year"
                            margin={{ top: 20, right: 20, bottom: 50, left: 60 }}
                            padding={0.3}
                            colors={['#0d7377', '#c9a84c', '#3d8b7d']}
                            axisBottom={{ tickRotation: 0 }}
                            axisLeft={{ legend: '$M', legendOffset: -50 }}
                            legends={[{ dataFrom: 'keys', anchor: 'bottom-right', direction: 'column', itemWidth: 100, itemHeight: 20 }]}
                        />
                    </div>
                    <DataSource source="Volusia County Property Appraiser" url="https://vcpa.volusia.org/" vintage="2025" />
                </Card>

                <Card>
                    <h3 className="text-lg font-semibold text-volusia-navy mb-4">Workforce by Industry (Based on QCEW)</h3>
                    <div className="h-64">
                        <ResponsivePie
                            data={workforceData}
                            margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
                            innerRadius={0.5}
                            padAngle={2}
                            cornerRadius={3}
                            colors={{ datum: 'data.color' }}
                            borderWidth={1}
                            borderColor={{ from: 'color', modifiers: [['darker', 0.2]] }}
                            enableArcLabels={true}
                            arcLabel="value"
                            arcLabelsSkipAngle={10}
                            legends={[{ anchor: 'right', direction: 'column', itemWidth: 100, itemHeight: 18, itemsSpacing: 5 }]}
                        />
                    </div>
                    <DataSource source="BLS QCEW" url="https://www.bls.gov/cew/" vintage="2025" />
                </Card>
            </div>

            {/* Permitting Velocity */}
            <Card className="mb-8">
                <h3 className="text-lg font-semibold text-volusia-navy mb-4">Permitting Velocity</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div className="bg-gray-100 rounded-lg p-4 text-center">
                        <div className="text-sm text-volusia-slate">No Data</div>
                        <div className="text-2xl font-bold text-volusia-navy mt-1">—</div>
                        <div className="text-xs text-gray-500">avg days</div>
                        <div className="text-xs mt-1 text-gray-500">→ Stable</div>
                    </div>
                </div>
                <DataSource source="Volusia County Building Dept" url="https://www.volusia.org/services/building/" vintage="2026" />
            </Card>

            {/* Leaderboard */}
            {leaderboardData.length > 0 && (
                <Card className="mb-8">
                    <h3 className="text-lg font-semibold text-volusia-navy mb-4">Leaderboard ({leaderboardCount})</h3>
                    <div className="space-y-2">
                        {leaderboardData.map((entry: any, i: number) => (
                            <div key={entry.user_id ?? i} className="flex items-center justify-between p-3 bg-gray-100 rounded">
                                <div className="flex items-center gap-3">
                                    <span className="text-lg font-bold text-volusia-navy">#{i + 1}</span>
                                    <div>
                                        <div className="font-medium text-volusia-navy">{entry.name ?? entry.user_id}</div>
                                        <div className="text-xs text-volusia-slate">{entry.xp ?? 0} XP</div>
                                    </div>
                                </div>
                                <div className="text-volusia-teal font-semibold">{entry.level ?? 1}</div>
                            </div>
                        ))}
                    </div>
                    <DataSource source="Gamification Engine" url="/gamification/leaderboard" vintage="2026" />
                </Card>
            )}


    
            {/* Data Room CTA */}
            <div className="bg-volusia-navy text-white rounded-xl p-8 text-center">
                <h3 className="text-2xl font-bold mb-3">Investor Data Room</h3>
                <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
                    Access detailed financial reports, infrastructure assessments, incentive program details,
                    and opportunity zone maps. Register for full access.
                </p>
                <button className="btn-primary bg-volusia-gold text-volusia-navy hover:bg-yellow-400">
                    Request Data Room Access
                </button>

    

    

    {/* Metadata Footer */}
    <footer className="bg-gray-100 py-8 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h3 className="text-lg font-bold text-volusia-navy mb-4">Data Sources & Metadata</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Economic Indicators</h4>
            {(economic?.indicators || []).slice(0, 3).map((i: any) => (
              <div key={i.name} className="text-volusia-slate mb-1">
                <span className="font-medium">{i.name}:</span> {i.value} {i.unit}
                <br/><span className="text-xs text-gray-500">Source: {i.source} | Vintage: {i.vintage} | Fetched: {new Date(i.fetched_at).toLocaleString()}</span>
              </div>
            ))}
          </div>
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Demographics</h4>
            {(economic?.indicators || []).slice(3, 6).map((i: any) => (
              <div key={i.name} className="text-volusia-slate mb-1">
                <span className="font-medium">{i.name}:</span> {i.value} {i.unit}
                <br/><span className="text-xs text-gray-500">Source: {i.source} | Vintage: {i.vintage}</span>
              </div>
            ))}
          </div>
          <div>
            <h4 className="font-semibold text-volusia-navy mb-2">Climate</h4>
            {(economic?.indicators || []).slice(6, 9).map((i: any) => (
              <div key={i.name} className="text-volusia-slate mb-1">
                <span className="font-medium">{i.name}:</span> {i.value} {i.unit}
                <br/><span className="text-xs text-gray-500">Source: {i.source} | Vintage: {i.vintage}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="mt-6 pt-4 border-t border-gray-300 text-xs text-gray-500">
          <p>Project Volusia Data Portal — All data sourced from public APIs (Census ACS, BLS QCEW, NOAA NCEI, C2ER). Last updated: {new Date().toLocaleString()}</p>
        </div>
      </div>
    </footer>
            </div>
        </div>
    )
}
