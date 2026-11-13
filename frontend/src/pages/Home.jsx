import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import { uploadFiles, analyzeMethod } from '../api'
import requirements from '../../../examples/fintech-quarter/moscow.csv?raw'
import baseline from '../../../examples/fintech-quarter/baseline-weights.csv?raw'
import riskFirst from '../../../examples/fintech-quarter/risk-first-weights.csv?raw'
import topsis from '../../../examples/fintech-quarter/topsis.csv?raw'

const METHODS = [
  {
    id: 'moscow',
    name: 'MoSCoW',
    emoji: '🎯',
    tagline: 'Must / Should / Could / Won\'t categories',
    description: 'Weighted prioritization of requirements by importance category, aggregating opinions from multiple stakeholders.',
    files: '2 CSV files',
    color: 'blue',
  },
  {
    id: 'topsis',
    name: 'TOPSIS',
    emoji: '📐',
    tagline: 'Ideal solution technique',
    description: 'Multi-criteria analysis based on distance to the positive ideal solution and negative ideal solution.',
    files: '1 CSV file',
    color: 'indigo',
  },
  {
    id: 'kano',
    name: 'Kano Model',
    emoji: '😊',
    tagline: 'User satisfaction analysis',
    description: 'Classifies requirements by their impact on user satisfaction: Must-be, Attractive, One-dimensional, Indifferent.',
    files: '1 CSV file',
    color: 'emerald',
  },
  {
    id: 'fuzzy_ahp_type1',
    name: 'Fuzzy AHP',
    emoji: '🔺',
    tagline: 'Fuzzy Analytic Hierarchy Process',
    description: 'AHP with Type-1 triangular or Type-2 interval fuzzy numbers to capture expert uncertainty in pairwise comparisons.',
    files: '1–3 CSV files',
    color: 'violet',
    subTypes: [
      { id: 'fuzzy_ahp_type1', label: 'Type-1 (triangular numbers)' },
      { id: 'fuzzy_ahp_type2', label: 'Type-2 (interval numbers)' },
    ],
  },
  {
    id: 'fuzzy_topsis',
    name: 'Fuzzy TOPSIS',
    emoji: '🌀',
    tagline: 'TOPSIS with fuzzy numbers',
    description: 'TOPSIS using trapezoidal Type-1 fuzzy ratings or intuitionistic fuzzy sets for richer uncertainty modeling.',
    files: '2 CSV files',
    color: 'cyan',
    subTypes: [
      { id: 'fuzzy_topsis', label: 'Fuzzy Type-1 (trapezoidal)' },
      { id: 'intuitionistic_topsis', label: 'Intuitionistic Fuzzy (IFS)' },
    ],
  },
  {
    id: 'fuzzy_delphi',
    name: 'Fuzzy Delphi',
    emoji: '🔮',
    tagline: 'Delphi with fuzzy expert ratings',
    description: 'Aggregates linguistic expert assessments using Interval Type-2 Fuzzy Sets (IT2FS) or Intuitionistic Fuzzy Sets (IFS).',
    files: '1 CSV file',
    color: 'amber',
    subTypes: [
      { id: 'fuzzy_delphi', label: 'Fuzzy Delphi (IT2FS)' },
      { id: 'intuitionistic_delphi', label: 'Intuitionistic Delphi (IFS)' },
    ],
  },
]

const COLOR_MAP = {
  blue: 'bg-blue-50 border-blue-200 hover:border-blue-400',
  indigo: 'bg-indigo-50 border-indigo-200 hover:border-indigo-400',
  emerald: 'bg-emerald-50 border-emerald-200 hover:border-emerald-400',
  violet: 'bg-violet-50 border-violet-200 hover:border-violet-400',
  cyan: 'bg-cyan-50 border-cyan-200 hover:border-cyan-400',
  amber: 'bg-amber-50 border-amber-200 hover:border-amber-400',
}

const BADGE_MAP = {
  blue: 'bg-blue-100 text-blue-700',
  indigo: 'bg-indigo-100 text-indigo-700',
  emerald: 'bg-emerald-100 text-emerald-700',
  violet: 'bg-violet-100 text-violet-700',
  cyan: 'bg-cyan-100 text-cyan-700',
  amber: 'bg-amber-100 text-amber-700',
}

export default function Home() {
  const navigate = useNavigate()
  const { addSession } = useApp()
  const [demoBusy, setDemoBusy] = useState(false)
  const [demoError, setDemoError] = useState('')

  const runDemo = async () => {
    setDemoBusy(true)
    setDemoError('')
    try {
      for (const [method, title, inputs] of [
        ['moscow', 'MoSCoW · baseline', {requirements_file: requirements, weights_file: baseline}],
        ['moscow', 'MoSCoW · risk-first', {requirements_file: requirements, weights_file: riskFirst}],
        ['topsis', 'TOPSIS · equal criteria', {data_file: topsis}],
      ]) {
        const files = Object.fromEntries(Object.entries(inputs).map(([key, text]) =>
          [key, new File([text], `${key}.csv`, {type: 'text/csv'})]))
        const { session_id } = await uploadFiles(method, files)
        const result = await analyzeMethod(method, session_id)
        addSession({session_id, method, method_name: title, ...result})
      }
      navigate('/dashboard')
    } catch (error) {
      setDemoError(error.response?.data?.detail || error.message)
    } finally {
      setDemoBusy(false)
    }
  }

  const handleSelect = (methodId) => {
    navigate(`/analysis?method=${methodId}`)
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      <div className="mb-10 text-center">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">
          Select a Prioritization Method
        </h1>
        <p className="text-slate-500 text-lg">
          Upload your CSV data, run the analysis, and get AI-powered insights
        </p>
      </div>

      <section className="card border border-blue-200 bg-blue-50 p-6 mb-8">
        <h2 className="text-xl font-bold text-slate-900">Which onboarding improvements should ship next?</h2>
        <p className="text-slate-600 mt-2 mb-4">Educational case · 12 synthetic options · Product, Operations and Risk.
          Compare a baseline with increased Risk influence and an equal-criteria TOPSIS reference. No API key required.</p>
        <button className="btn-primary" onClick={runDemo} disabled={demoBusy}>
          {demoBusy ? 'Running three analyses…' : 'Run fintech demo →'}
        </button>
        {demoError && <p role="alert" className="text-red-700 mt-3">{demoError}</p>}
      </section>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {METHODS.map((m) => (
          <div
            key={m.id}
            className={`card border-2 p-6 cursor-pointer transition-all duration-200 ${COLOR_MAP[m.color]}`}
            onClick={() => handleSelect(m.subTypes ? m.subTypes[0].id : m.id)}
          >
            <div className="flex items-start justify-between mb-3">
              <span className="text-3xl">{m.emoji}</span>
              <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${BADGE_MAP[m.color]}`}>
                {m.files}
              </span>
            </div>

            <h2 className="text-xl font-bold text-slate-900 mb-0.5">{m.name}</h2>
            <p className="text-sm font-medium text-slate-500 mb-3">{m.tagline}</p>
            <p className="text-sm text-slate-600 leading-relaxed mb-4">{m.description}</p>

            {m.subTypes ? (
              <div className="flex flex-col gap-2">
                {m.subTypes.map((sub) => (
                  <button
                    key={sub.id}
                    onClick={(e) => { e.stopPropagation(); handleSelect(sub.id) }}
                    className="btn-primary text-sm py-1.5 text-left px-3"
                  >
                    {sub.label}
                  </button>
                ))}
              </div>
            ) : (
              <button
                onClick={(e) => { e.stopPropagation(); handleSelect(m.id) }}
                className="btn-primary w-full"
              >
                Select →
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
