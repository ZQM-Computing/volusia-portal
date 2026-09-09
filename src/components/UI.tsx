import { ReactNode } from 'react'

export function StatCard({ value, label, change, changeLabel }: { value: string; label: string; change?: number | null; changeLabel?: string | null }) {
  const changeColor = change && change > 0 ? 'text-green-600' : change && change < 0 ? 'text-red-600' : 'text-gray-500'
  return (
    <div className="stat-card">
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
      {change !== null && change !== undefined && (
        <div className={`text-xs font-medium mt-1 ${changeColor}`}>
          {change > 0 ? '↑' : change < 0 ? '↓' : ''} {Math.abs(change)}{changeLabel || ''}
        </div>
      )}
    </div>
  )
}

export function Card({ children, className = '', hover = false }: { children: ReactNode; className?: string; hover?: boolean }) {
  return <div className={`card ${hover ? 'hover:shadow-lg transition-shadow cursor-pointer' : ''} ${className}`}>{children}</div>
}

export function SectionTitle({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="mb-6">
      <h2 className="section-title">{title}</h2>
      {subtitle && <p className="section-subtitle">{subtitle}</p>}
    </div>
  )
}

export function Badge({ children, variant = 'default', className = '' }: { children: ReactNode; variant?: 'default' | 'success' | 'warning' | 'error' | 'info'; className?: string }) {
  const colors = {
    default: 'bg-gray-100 text-gray-700',
    success: 'bg-green-100 text-green-700',
    warning: 'bg-yellow-100 text-yellow-700',
    error: 'bg-red-100 text-red-700',
    info: 'bg-blue-100 text-blue-700',
  }
  return <span className={`text-xs font-medium px-2.5 py-1 rounded-full ${colors[variant]} ${className}`.trim()}>{children}</span>
}

export function DataSource({ source, url, vintage }: { source: string; url: string; vintage?: string }) {
  return (
    <div className="text-xs text-gray-500 flex flex-wrap gap-2 items-center">
      <span>Source: <a href={url} target="_blank" rel="noopener noreferrer" className="text-volusia-teal hover:underline">{source}</a></span>
      {vintage && <span className="text-gray-300">|</span>}
      {vintage && <span>Vintage: {vintage}</span>}
    </div>
  )
}

export function Skeleton({ count = 1, className = '' }: { count?: number; className?: string }) {
  return (
    <div className={`animate-pulse space-y-2 ${className}`}>
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="h-4 bg-gray-200 rounded w-full" style={{ width: `${80 + Math.random() * 20}%` }} />
      ))}
    </div>
  )
}

export function EmptyState({ message, title, description }: { message?: string; title?: string; description?: string }) {
  const label = title || message || 'No data available'
  return (
    <div className="text-center py-8 text-gray-500 text-sm">
      <div className="text-3xl mb-2">📊</div>
      <p className="font-medium">{label}</p>
      {description && <p className="text-xs mt-1">{description}</p>}
    </div>
  )
}

export function ErrorState({ message = 'Something went wrong', onRetry }: { message?: string; onRetry?: () => void }) {
  return (
    <div className="text-center py-8 text-red-600 text-sm">
      <div className="text-3xl mb-2">⚠️</div>
      <p>{message}</p>
      {onRetry && (
        <button onClick={onRetry} className="mt-2 px-3 py-1 bg-red-100 text-red-700 rounded text-xs hover:bg-red-200">
          Retry
        </button>
      )}
    </div>
  )
}
