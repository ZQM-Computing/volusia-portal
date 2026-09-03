import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { stakeholderGroups } from '../data/sampleData'

const navLinks = [
  { to: '/', label: 'Portal Home' },
  { to: '/data', label: 'Data Explorer' },
  { to: '/maps', label: 'Maps' },
  { to: '/business', label: 'Business' },
  { to: '/residents', label: 'Residents' },
  { to: '/tourists', label: 'Tourists' },
  { to: '/leaders', label: 'Leaders' },
]

export function Header() {
  const location = useLocation()
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-3 no-underline">
            <div className="w-10 h-10 rounded-lg bg-volusia-teal flex items-center justify-center text-volusia-gold font-bold text-xl">
              V
            </div>
            <div className="flex flex-col">
              <span className="text-volusia-navy font-bold text-lg leading-tight">Project Volusia</span>
              <span className="text-xs text-volusia-slate">Open Intelligence Portal</span>
            </div>
          </Link>

          <nav className="hidden lg:flex items-center space-x-1">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className={`nav-link text-sm ${location.pathname === link.to ? 'nav-link-active' : ''}`}
              >
                {link.label}
              </Link>
            ))}
          </nav>

          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="lg:hidden p-2 rounded-md text-volusia-slate hover:text-volusia-teal"
            aria-label="Toggle menu"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {mobileOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {mobileOpen && (
          <div className="lg:hidden pb-4 border-t border-gray-100">
            <div className="flex flex-col space-y-1 pt-2">
              {navLinks.map((link) => (
                <Link
                  key={link.to}
                  to={link.to}
                  onClick={() => setMobileOpen(false)}
                  className={`nav-link text-sm ${location.pathname === link.to ? 'nav-link-active' : ''}`}
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </header>
  )
}

export function Footer() {
  return (
    <footer className="bg-volusia-navy text-white py-12 mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <h3 className="text-xl font-bold mb-2 text-volusia-gold">Project Volusia</h3>
            <p className="text-gray-300 text-sm leading-relaxed max-w-md">
              Open-source intelligence and data-driven decision-making for Volusia County, Florida.
              Built by ZQM Labs. Serving business owners, residents, tourists, and industry movers.
            </p>
          </div>
          <div>
            <h4 className="font-semibold mb-3 text-gray-200">Platform</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><Link to="/data" className="hover:text-white no-underline text-gray-300">Data Explorer</Link></li>
              <li><Link to="/maps" className="hover:text-white no-underline text-gray-300">Interactive Maps</Link></li>
              <li><Link to="/business" className="hover:text-white no-underline text-gray-300">Business Tools</Link></li>
              <li><Link to="/residents" className="hover:text-white no-underline text-gray-300">Resident Data</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-3 text-gray-200">About</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>Version 1.0</li>
              <li>Launched 2026-09-02</li>
              <li><a href="https://github.com/zqmcomputing" className="hover:text-white no-underline text-gray-300">GitHub</a></li>
              <li><Link to="/leaders" className="hover:text-white no-underline text-gray-300">Investor Data Room</Link></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-sm text-gray-400">
          &copy; 2026 ZQM Labs / ZQM Computing. Released under MIT License. Source available on GitHub.
        </div>
      </div>
    </footer>
  )
}
