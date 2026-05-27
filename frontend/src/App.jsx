import { Routes, Route, Link, useLocation } from 'react-router-dom'
import Home from './pages/Home'
import Analysis from './pages/Analysis'
import Dashboard from './pages/Dashboard'
import { useApp } from './context/AppContext'

function Navbar() {
  const location = useLocation()
  const { completedSessions } = useApp()

  const links = [
    { to: '/', label: 'Methods' },
    { to: '/dashboard', label: `Dashboard${completedSessions.length > 0 ? ` (${completedSessions.length})` : ''}` },
  ]

  return (
    <nav className="bg-white border-b border-slate-200 px-6 py-3 flex items-center gap-8 sticky top-0 z-40">
      <Link to="/" className="text-lg font-bold text-blue-600 flex items-center gap-2">
        <span className="text-2xl">⚡</span>
        AI Prioritization Tool
      </Link>
      <div className="flex gap-1">
        {links.map((l) => (
          <Link
            key={l.to}
            to={l.to}
            className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
              location.pathname === l.to
                ? 'bg-blue-50 text-blue-700'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            {l.label}
          </Link>
        ))}
      </div>
    </nav>
  )
}

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analysis" element={<Analysis />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </div>
  )
}
