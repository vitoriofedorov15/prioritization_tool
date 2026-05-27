import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell, ResponsiveContainer,
} from 'recharts'

function getColor(score) {
  if (score >= 70) return '#22C55E'
  if (score >= 40) return '#F59E0B'
  return '#EF4444'
}

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  const { alt, score, comment } = payload[0].payload
  return (
    <div className="bg-white border border-slate-200 rounded-lg shadow-lg p-3 text-xs max-w-[220px]">
      <p className="font-semibold text-slate-800 mb-1">{alt}</p>
      <p className="text-slate-500">Score: <span className="font-bold text-slate-800">{score?.toFixed(1)}</span></p>
      {comment && <p className="text-slate-400 mt-1 leading-snug">{comment}</p>}
    </div>
  )
}

export default function ResultsChart({ results }) {
  const data = Object.entries(results || {})
    .map(([alt, d]) => ({ alt, score: d.score, comment: d.comment }))
    .sort((a, b) => b.score - a.score)

  if (!data.length) return null

  const barHeight = Math.max(260, data.length * 44)

  return (
    <ResponsiveContainer width="100%" height={barHeight}>
      <BarChart
        layout="vertical"
        data={data}
        margin={{ top: 4, right: 30, bottom: 4, left: 0 }}
      >
        <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
        <XAxis
          type="number"
          domain={[0, 100]}
          tick={{ fontSize: 11, fill: '#94a3b8' }}
          tickLine={false}
        />
        <YAxis
          type="category"
          dataKey="alt"
          width={160}
          tick={{ fontSize: 12, fill: '#475569' }}
          tickLine={false}
        />
        <Tooltip content={<CustomTooltip />} cursor={{ fill: '#f8fafc' }} />
        <Bar dataKey="score" radius={[0, 6, 6, 0]} maxBarSize={28}>
          {data.map((entry) => (
            <Cell key={entry.alt} fill={getColor(entry.score)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
