import { Component, ErrorInfo, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = { hasError: false, error: null }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary:', error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="max-w-7xl mx-auto px-4 py-12 text-center">
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-8">
            <h2 className="text-xl font-bold text-red-800 dark:text-red-200 mb-2">
              Something went wrong
            </h2>
            <p className="text-red-600 dark:text-red-400 mb-4">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            <button onClick={() => this.setState({ hasError: false, error: null })} className="btn-primary">
              Try Again
            </button>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}
