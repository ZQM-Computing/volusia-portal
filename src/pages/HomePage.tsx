import { Link } from 'react-router-dom'
import { indicators, newsItems, stakeholderGroups } from '../data/sampleData'
import { StatCard, Card, SectionTitle, Badge } from '../components/UI'

export function HomePage() {
  const featuredIndicators = indicators.slice(0, 4)

  return (
    <div>
      {/* Hero */}
      <section className="bg-gradient-to-br from-volusia-navy via-volusia-blue to-volusia-teal text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <Badge variant="info">v1.0 — September 2026</Badge>
            <h1 className="text-4xl md:text-5xl font-bold mt-4 mb-6 font-display leading-tight">
              Open Intelligence for Volusia County
            </h1>
            <p className="text-xl text-gray-200 mb-8 leading-relaxed">
              Free, open-source data and analytics for business owners, residents, tourists, and industry movers.
              Real numbers. Real sources. No paywalls.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link to="/data" className="btn-primary no-underline bg-volusia-gold text-volusia-navy hover:bg-yellow-400">
                Explore Data
              </Link>
              <Link to="/maps" className="btn-secondary no-underline border-white text-white hover:bg-white hover:text-volusia-navy">
                View Maps
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Indicators */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {featuredIndicators.map((ind) => (
            <StatCard
              key={ind.id}
              value={typeof ind.value === 'number' ? ind.value.toLocaleString() : ind.value}
              label={ind.name}
              change={ind.change}
              changeLabel={ind.changeLabel}
            />
          ))}
        </div>
      </section>

      {/* Mission */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-3xl font-bold text-volusia-navy mb-4 font-display">
              Technology-Driven Business Growth
            </h2>
            <p className="text-volusia-slate leading-relaxed mb-4">
              Project Volusia accelerates business growth by building and integrating open, scalable
              technology systems that improve commerce, democratize data access, and harness big data
              intelligence.
            </p>
            <p className="text-volusia-slate leading-relaxed mb-6">
              We serve four core constituencies: business owners, residents, tourists, and industry movers.
              Every dataset, every chart, every recommendation is judged by one question: does this make
              life better for the people who live, work, visit, and invest in Volusia County?
            </p>
            <div className="flex flex-wrap gap-2">
              <Badge>Open Source</Badge>
              <Badge>Privacy by Design</Badge>
              <Badge>Measurable Impact</Badge>
              <Badge>Iterative Delivery</Badge>
            </div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-100">
            <h3 className="text-lg font-semibold text-volusia-navy mb-4">Strategic Outcomes</h3>
            <ul className="space-y-3 text-sm text-volusia-slate">
              <li className="flex items-start gap-2">
                <span className="text-volusia-teal font-bold mt-0.5">→</span>
                30% reduction in time-to-market for new commerce features
              </li>
              <li className="flex items-start gap-2">
                <span className="text-volusia-teal font-bold mt-0.5">→</span>
                100% of business-critical data available via governed API
              </li>
              <li className="flex items-start gap-2">
                <span className="text-volusia-teal font-bold mt-0.5">→</span>
                Single customer view across all touchpoints
              </li>
              <li className="flex items-start gap-2">
                <span className="text-volusia-teal font-bold mt-0.5">→</span>
                Sub-second analytics on core business events
              </li>
              <li className="flex items-start gap-2">
                <span className="text-volusia-teal font-bold mt-0.5">→</span>
                Open developer portal with 99.9% uptime SLA
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Stakeholder Groups */}
      <section className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionTitle
            title="Built for Everyone"
            subtitle="Four constituencies. One platform. Tailored intelligence for each."
          />
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {stakeholderGroups.map((group) => (
              <Card key={group.id} hover>
                <div className="text-3xl mb-3">{group.icon}</div>
                <h3 className="text-lg font-semibold text-volusia-navy mb-2">{group.name}</h3>
                <p className="text-sm text-volusia-slate mb-4">{group.description}</p>
                <ul className="space-y-1.5">
                  {group.highlights.map((h, i) => (
                    <li key={i} className="text-xs text-volusia-slate flex items-start gap-1.5">
                      <span className="text-volusia-teal mt-0.5">•</span> {h}
                    </li>
                  ))}
                </ul>
                <Link
                  to={`/${group.id}`}
                  className="inline-block mt-4 text-sm font-medium text-volusia-teal hover:underline no-underline"
                >
                  Explore →
                </Link>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* News */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <SectionTitle title="Latest Updates" subtitle="Platform releases, data updates, and community news" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {newsItems.map((item) => (
            <Card key={item.id}>
              <div className="flex items-center gap-2 mb-2">
                <Badge variant="info">{item.category}</Badge>
                <span className="text-xs text-gray-400">{item.date}</span>
              </div>
              <h3 className="text-lg font-semibold text-volusia-navy mb-2">{item.title}</h3>
              <p className="text-sm text-volusia-slate">{item.summary}</p>
            </Card>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="bg-volusia-teal text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4 font-display">Ready to Use the Data?</h2>
          <p className="text-lg text-gray-200 mb-8 max-w-2xl mx-auto">
            All datasets are free, open, and available in machine-readable formats.
            Download, analyze, build on top.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link to="/data" className="btn-primary no-underline bg-volusia-gold text-volusia-navy hover:bg-yellow-400">
              Browse Datasets
            </Link>
            <Link to="/maps" className="btn-secondary no-underline border-white text-white hover:bg-white hover:text-volusia-teal">
              Explore Maps
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
