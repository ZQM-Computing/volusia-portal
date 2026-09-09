import { useState, useEffect } from 'react'
import { useDemographicIndicators, useEconomicIndicators } from '../hooks/useApi'
import { Card, SectionTitle, Badge, DataSource, StatCard, Skeleton, EmptyState, ErrorState } from '../components/UI'

export function ResidentsPage() {
  const { data: demographics, loading: demoLoading, error: demoError, refetch: refetchDemo } = useDemographicIndicators()
  const { data: economic } = useEconomicIndicators()
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  useEffect(() => { document.title = 'Residents — Project Volusia' }, [])

  if (demoError) return <ErrorState message={demoError} onRetry={refetchDemo} />
  if (demoLoading) return <Skeleton count={4} />
  if (!demographics?.indicators) return <EmptyState title="No demographic data" description="Demographic data is being refreshed." />

  const getIndicator = (name: string, source?: 'demographics' | 'economic') => {
    if (source === 'economic' && economic?.indicators) return economic.indicators.find((i: any) => i.name === name) ?? null
    return demographics.indicators.find((i: any) => i.name === name) ?? null
  }
  const fmtNum = (v: any) => { if (v == null) return '—'; const n = Number(v); return isNaN(n) ? String(v) : n.toLocaleString() }

  const totalPop = getIndicator('total_population_acs')
  const medianAge = getIndicator('median_age')
  const medianIncome = getIndicator('median_household_income_acs') || getIndicator('median_household_income', 'economic')
  const povertyRate = getIndicator('poverty_rate_acs')
  const pctWhite = getIndicator('pct_white_alone_acs')
  const pctBlack = getIndicator('pct_black_alone_acs')
  const pctHispanic = getIndicator('pct_hispanic_acs')
  const pctAsian = getIndicator('pct_asian_acs')
  const pctOther = getIndicator('pct_other_races_acs')
  const collegeGrad = getIndicator('pct_bachelors_plus')
  const housing = getIndicator('housing_units')
  const ownerOccupied = getIndicator('owner_occupied_pct')
  const medianRent = getIndicator('median_gross_rent')
  const unemployment = getIndicator('unemployment_rate_acs') || getIndicator('unemployment_rate_bls')
  const commute = getIndicator('avg_commute_time')
  const costOfLiving = getIndicator('cost_of_living_index')

  return (
    <div>
      <SectionTitle title="Residents" subtitle="Demographic and cost-of-living data for Volusia County" />
      <Badge variant="info">{demographics.indicators.length} live indicators</Badge>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 my-8">
        <StatCard value={totalPop ? fmtNum(totalPop.value) : '—'} label="Population" change={undefined} changeLabel="Census ACS" />
        <StatCard value={medianIncome ? `$${fmtNum(medianIncome.value)}` : '—'} label="Median Household Income" change={undefined} changeLabel="ACS DP03" />
        <StatCard value={povertyRate ? `${povertyRate.value}%` : '—'} label="Poverty Rate" change={undefined} changeLabel="Census" />
        <StatCard value={medianAge ? `${medianAge.value} yrs` : '—'} label="Median Age" change={undefined} changeLabel="ACS" />
      </div>

      {/* Race & Ethnicity */}
      <Card className="mb-8">
        <h3 className="font-bold text-volusia-navy mb-4">Race & Ethnicity</h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {pctWhite && <div className="text-center p-4 bg-gray-50 rounded-lg"><div className="text-xl font-bold text-volusia-navy">{pctWhite.value}%</div><div className="text-xs text-volusia-slate">White Alone</div></div>}
          {pctBlack && <div className="text-center p-4 bg-gray-50 rounded-lg"><div className="text-xl font-bold text-volusia-navy">{pctBlack.value}%</div><div className="text-xs text-volusia-slate">Black Alone</div></div>}
          {pctHispanic && <div className="text-center p-4 bg-gray-50 rounded-lg"><div className="text-xl font-bold text-volusia-navy">{pctHispanic.value}%</div><div className="text-xs text-volusia-slate">Hispanic</div></div>}
          {pctAsian && <div className="text-center p-4 bg-gray-50 rounded-lg"><div className="text-xl font-bold text-volusia-navy">{pctAsian.value}%</div><div className="text-xs text-volusia-slate">Asian</div></div>}
          {pctOther && <div className="text-center p-4 bg-gray-50 rounded-lg"><div className="text-xl font-bold text-volusia-navy">{pctOther.value}%</div><div className="text-xs text-volusia-slate">Other</div></div>}
        </div>
        <DataSource source="US Census ACS DP05" url="https://data.census.gov/" vintage="2024" />
      </Card>

      {/* Education */}
      {collegeGrad && (
        <Card className="mb-8">
          <h3 className="font-bold text-volusia-navy mb-4">Education</h3>
          <div className="flex justify-between py-2 border-b border-gray-100">
            <span className="text-volusia-slate">Bachelor's Degree or Higher</span>
            <span className="font-medium text-volusia-navy">{collegeGrad.value}%</span>
          </div>
          <DataSource source="ACS DP02" url="https://data.census.gov/" vintage="2024" />
        </Card>
      )}

      {/* Housing */}
      {(housing || medianRent || ownerOccupied) && (
        <Card className="mb-8">
          <h3 className="font-bold text-volusia-navy mb-4">Housing</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="text-xl font-bold text-volusia-navy">{housing ? fmtNum(housing.value) : '—'}</div>
              <div className="text-xs text-volusia-slate">Housing Units</div>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="text-xl font-bold text-volusia-navy">{ownerOccupied ? `${ownerOccupied.value}%` : '—'}</div>
              <div className="text-xs text-volusia-slate">Owner-Occupied</div>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="text-xl font-bold text-volusia-navy">{medianRent ? `$${fmtNum(medianRent.value)}` : '—'}</div>
              <div className="text-xs text-volusia-slate">Median Gross Rent</div>
            </div>
          </div>
          <DataSource source="ACS DP04" url="https://data.census.gov/" vintage="2024" />
        </Card>
      )}

      {/* Cost of Living — honest */}
      <Card className="mb-8">
        <h3 className="font-bold text-volusia-navy mb-4">Cost of Living</h3>
        <p className="text-sm text-volusia-slate mb-4">
          Cost-of-living index from C2ER. Compare against national average (100).
        </p>
        <div className="flex justify-between py-2 border-b border-gray-100">
          <span className="text-volusia-slate">Cost-of-Living Index</span>
          <span className="font-medium text-volusia-navy">{costOfLiving ? costOfLiving.value : '—'}</span>
        </div>
        <DataSource source="C2ER" url="https://www.c2er.org/" vintage="2024" />
      </Card>

      {/* Employment for residents */}
      {unemployment && (
        <Card className="mb-8">
          <h3 className="font-bold text-volusia-navy mb-4">Labor Market</h3>
          <div className="flex justify-between py-2 border-b border-gray-100">
            <span className="text-volusia-slate">Unemployment Rate</span>
            <span className="font-medium text-volusia-navy">{unemployment.value}%</span>
          </div>
          {commute && (
            <div className="flex justify-between py-2 border-b border-gray-100">
              <span className="text-volusia-slate">Avg Commute</span>
              <span className="font-medium text-volusia-navy">{commute.value} min</span>
            </div>
          )}
          <DataSource source="BLS LAUS / ACS DP03" url="https://www.bls.gov/" vintage="2024" />
        </Card>
      )}

      {/* Community resources */}
      <Card>
        <h3 className="font-bold text-volusia-navy mb-4">Community Resources</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <a href="https://www.volusia.org" target="_blank" rel="noopener noreferrer" className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
            <h4 className="font-semibold text-volusia-navy">Volusia County Government</h4>
            <p className="text-sm text-volusia-slate">Services, permits, and community resources.</p>
          </a>
          <a href="https://www.volusia.org" target="_blank" rel="noopener noreferrer" className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
            <h4 className="font-semibold text-volusia-navy">Public Safety</h4>
            <p className="text-sm text-volusia-slate">Emergency services and safety data — Volusia County Sheriff, Fire Rescue.</p>
          </a>
        </div>
      </Card>
    </div>
  )
}
