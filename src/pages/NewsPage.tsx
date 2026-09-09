import { useNews } from '../hooks/useApi'
import { Card, SectionTitle, Badge } from '../components/UI'

export function NewsPage() {
  const { data: news, loading } = useNews()

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="animate-pulse space-y-4">
          {[1,2,3].map(i => <div key={i} className="h-32 bg-gray-200 rounded-lg" />)}
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <SectionTitle title="News & Updates" subtitle="Latest from Project Volusia" />
      <div className="space-y-4">
        {news && news.map((article: any) => (
          <Card key={article.id} className="hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-lg font-bold text-volusia-navy">{article.title}</h3>
                <p className="text-volusia-slate mt-1">{article.summary}</p>
              </div>
              <Badge variant="success">{article.category}</Badge>
            </div>
            <p className="text-xs text-gray-400 mt-3">{article.date}</p>
          </Card>
        ))}
      </div>
    </div>
  )
}
