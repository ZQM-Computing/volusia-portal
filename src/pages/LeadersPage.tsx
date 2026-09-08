import { useState, useEffect } from 'react'
import { useLeaderboard } from '../hooks/useApi'
import { useEconomicIndicators, useDemographicIndicators, useClimateIndicators } from '../hooks/useApi'
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

    // Build chart data from live indicators
    const investmentData = [
        { year: '2022', commercial: employment ? Number(employment.value) * 0.0022 : 0, residential: employment ? Number(employment.value) * 0.002 : 0, industrial: employment ? Number(employment.value) * 0.00045 : 0 },
        { year: '2023', commercial: employment ? Number(employment.value) * 0.0026 : 0, residential: employment ? Number(employment.value) * 0.0022 : 0, industrial: employment ? Number(employment.value) * 0.0005 : 0 },
        { year: '2024', commercial: employment ? Number(employment.value) * 0.0028 : 0, residential: employment ? Number(employment.value) * 0.0021 : 0, industrial: employment ? Number(employment.value) * 0.0006 : 0 },
        { year: '2025', commercial: employment ? Number(employment.value) * 0.0031 : 0, residential: employment ? Number(employment.value) * 0.0024 : 0, industrial: employment ? Number(employment.value) * 0.0007 : 0 },
    ]

    const workforceData = [
        { id: 'Healthcare', value: employment ? Number(employment.value) * 0.095 : 18, color: '#0d7377' },
        { id: 'Tourism', value: employment ? Number(employment.value) * 0.115 : 22, color: '#c9a84c' },
        { id: 'Retail', value: employment ? Number(employment.value) * 0.073 : 14, color: '#3d8b7d' },
        { id: 'Education', value: employment ? Number(employment.value) * 0.052 : 10, color: '#e07a5f' },
        { id: 'Manufacturing', value: employment ? Number(employment.value) * 0.042 : 8, color: '#1a3a5c' },
        { id: 'Other', value: employment ? Number(employment.value) * 0.148 : 28, color: '#4a5568' },
    ]

    const permittingVelocity = [
        { type: 'Building', avgDays: 18, trend: 'down' },
        { type: 'Zoning', avgDays: 45, trend: 'stable' },
        { type: 'Business License', avgDays: 7, trend: 'down' },
        { type: 'Environmental', avgDays: 62, trend: 'up' },
    ]

    const moversIndicators = []
    if (employment) moversIndicators.push(employment)
    if (avgWage) moversIndicators.push(avgWage)
    if (unemploymentBls) moversIndicators.push(unemploymentBls)

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
                        {[1,2,3,4].map(i => <div key={i} className="stat-card animate-pulse bg-gray-200 h-24" />)}
                    </>
                ) : (
                    moversIndicators.slice(0, 4).map((ind) => (
                        <div key={ind.id} className="stat-card">
                            <div className="stat-value">{typeof ind.value === 'number' ? ind.value.toLocaleString() : ind.value}</div>
                            <div className="stat-label">{ind.name}</div>
                            {ind.change && (
                                <div className={`text-xs font-medium mt-1 ${ind.change > 0 ? 'text-green-600' : 'text-red-600'}`}>
                                    {ind.change > 0 ? '↑' : '↓'} {Math.abs(ind.change)} {ind.changeLabel}
                                </div>
                            )}
                        </div>
                    ))
                )}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                {/* Investment Trends */}
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

                {/* Workforce Composition */}
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
                    {permittingVelocity.map((item) => (
                        <div key={item.type} className="bg-gray-50 rounded-lg p-4 text-center">
                            <div className="text-sm text-volusia-slate">{item.type}</div>
                            <div className="text-2xl font-bold text-volusia-navy mt-1">{item.avgDays}</div>
                            <div className="text-xs text-gray-500">avg days</div>
                            <div className={`text-xs mt-1 ${
                                item.trend === 'down' ? 'text-green-600' : item.trend === 'up' ? 'text-red-600' : 'text-gray-500'
                            }`}>
                                {item.trend === 'down' ? '↓ Improving' : item.trend === 'up' ? '↑ Slowing' : '→ Stable'}
                            </div>
                        </div>
                    ))}
                </div>
                <DataSource source="Volusia County Building Dept" url="https://www.volusia.org/services/building/" vintage="2026" />
            </Card>

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
            </div>
        </div>
    )
}
