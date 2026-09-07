import { Link } from 'react-router-dom'
import { Card, SectionTitle } from '../components/UI'

export function NotFoundPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-24 text-center">
      <SectionTitle title="404" subtitle="Page not found" />
      <Card className="max-w-md mx-auto">
        <p className="text-xl text-volusia-slate mb-4">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Link to="/" className="btn-primary inline-block no-underline">
          Return to Portal Home
        </Link>
      </Card>
    </div>
  )
}
