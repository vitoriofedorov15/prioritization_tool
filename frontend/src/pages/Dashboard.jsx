import { useState } from 'react'
import { Link } from 'react-router-dom'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { useApp } from '../context/AppContext'
import ChatPanel from '../components/ChatPanel'

const METHOD_COLORS = [
  '#3B82F6', '#8B5CF6', '#10B981', '#F59E0B', '#EF4444', '#06B6D4',
]

function buildComparisonData(sessions) {
  const allAlts = new Set()
  sessions.forEach((s) => Object.keys(s.results || {}).forEach((a) => allAlts.add(a)))

  return Array.from(allAlts).map((alt) => {
    const row = { alt }
    sessions.forEach((s) => {
      const score = s.results?.[alt]?.score
      if (score !== undefined) row[s.session_id] = score
    })
    return row
  })
}

export default function Dashboard() {
  const { completedSessions } = useApp()
  const [selectedId, setSelectedId] = useState(null)

  if (completedSessions.length === 0) {
    return (
      <div className="flex flex-1 items-center justify-center flex-col gap-4 text-center p-10">
        <span className="text-6xl">📊</span>
        <h2 className="text-2xl font-bold text-slate-700">Dashboard Empty</h2>
        <p className="text-slate-500 max-w-sm">
          Run at least one analysis to see results here. When two or more methods are run, a comparative chart will appear.
        </p>
        <Link to="/" className="btn-primary mt-2">Select Method →</Link>
      </div>
    )
  }

  const comparisonData = completedSessions.length >= 2 ? buildComparisonData(completedSessions) : null
  const activeSession = selectedId
    ? completedSessions.find((s) => s.session_id === selectedId)
    : completedSessions[completedSessions.length - 1]

  return (
    <div className="flex flex-1 min-h-0">
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-5xl mx-auto px-6 py-8">
          <h1 className="text-2xl font-bold text-slate-900 mb-6">Analysis Dashboard</h1>

          {/* Session chips */}
          <div className="flex flex-wrap gap-2 mb-8">
            {completedSessions.map((s, i) => (
              <button
                key={s.session_id}
                onClick={() => setSelectedId(s.session_id)}
                className={`px-3 py-1.5 rounded-full text-sm font-medium border transition-colors ${
                  activeSession?.session_id === s.session_id
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-slate-200 bg-white text-slate-600 hover:border-slate-300'
                }`}
              >
                <span style={{ color: METHOD_COLORS[i % METHOD_COLORS.length] }}>●</span>{' '}
                {s.method_name || s.method}
              </button>
            ))}
            <Link to="/" className="px-3 py-1.5 rounded-full text-sm border border-dashed border-slate-300 text-slate-400 hover:border-blue-300 hover:text-blue-500">
              + Add Method
            </Link>
          </div>

          {/* Comparison chart */}
          {comparisonData && (
            <div className="card p-6 mb-6">
              <h2 className="font-semibold text-slate-700 mb-4">Scenario and Method Comparison</h2>
              <p className="text-sm text-slate-500 mb-4">Synthetic educational data. Compare rank order: MoSCoW scores are relative to the best option;
                TOPSIS scores measure closeness to an ideal. Score differences across methods are not equivalent.</p>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={comparisonData} margin={{ top: 5, right: 20, bottom: 110, left: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis
                    dataKey="alt"
                    tick={{ fontSize: 11, fill: '#64748b' }}
                    angle={-35}
                    textAnchor="end"
                    interval={0}
                  />
                  <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: '#64748b' }} />
                  <Tooltip
                    contentStyle={{ borderRadius: 8, border: '1px solid #e2e8f0', fontSize: 12 }}
                  />
                  <Legend verticalAlign="top" height={40} wrapperStyle={{ fontSize: 12 }} />
                  {completedSessions.map((session, i) => (
                    <Bar
                      key={session.session_id}
                      dataKey={session.session_id}
                      name={session.method_name || session.method}
                      fill={METHOD_COLORS[i % METHOD_COLORS.length]}
                      radius={[4, 4, 0, 0]}
                    />
                  ))}
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Active session detail */}
          {activeSession && (
            <div className="card p-6">
              <h2 className="font-semibold text-slate-700 mb-4">
                Details: {activeSession.method_name || activeSession.method}
              </h2>
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-200">
                    <th className="text-left py-2 pr-4 text-slate-500 font-medium">Rank</th>
                    <th className="text-left py-2 pr-4 text-slate-500 font-medium">Alternative</th>
                    <th className="text-right py-2 text-slate-500 font-medium">Score</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(activeSession.results || {})
                    .sort(([, a], [, b]) => b.score - a.score)
                    .map(([alt, data], i) => (
                      <tr key={alt} className="border-b border-slate-100 hover:bg-slate-50">
                        <td className="py-2.5 pr-4 text-slate-400 font-mono">#{i + 1}</td>
                        <td className="py-2.5 pr-4 font-medium text-slate-800">{alt}</td>
                        <td className="py-2.5 text-right">
                          <span className={`font-bold ${data.score >= 70 ? 'text-green-600' : data.score >= 40 ? 'text-amber-600' : 'text-red-500'}`}>
                            {typeof data.score === 'number' ? data.score.toFixed(1) : data.score}
                          </span>
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>

              {activeSession.conflicts?.length > 0 && (
                <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                  <p className="text-sm font-medium text-amber-700 mb-1">
                    ⚠️ {activeSession.conflicts.length} conflict(s) detected
                  </p>
                  {activeSession.conflicts.map((c, i) => (
                    <p key={i} className="text-xs text-amber-600">• {c.description}</p>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <ChatPanel sessionId={activeSession?.session_id} disabled={!activeSession} />
    </div>
  )
}
