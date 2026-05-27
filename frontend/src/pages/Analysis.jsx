import { useState, useCallback, useRef } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { uploadFiles, analyzeMethod, getAiInterpretation, getAiConflicts } from '../api'
import { useApp } from '../context/AppContext'
import ResultsChart from '../components/ResultsChart'
import ConflictAlert from '../components/ConflictAlert'
import ChatPanel from '../components/ChatPanel'

const METHOD_INFO = {
  moscow: { name: 'MoSCoW', emoji: '🎯', files: [
    { key: 'requirements_file', label: 'Requirements file', hint: 'Columns: Alternative, Criterion, Stakeholder, Rating' },
    { key: 'weights_file', label: 'Stakeholder weights file', hint: 'Columns: Stakeholder, Weight' },
  ]},
  topsis: { name: 'TOPSIS', emoji: '📐', files: [
    { key: 'data_file', label: 'Data file', hint: 'Columns: Alternative, [criteria...], Stakeholder Weight' },
  ]},
  kano: { name: 'Kano Model', emoji: '😊', files: [
    { key: 'data_file', label: 'Data file', hint: 'Columns: Alternative, Stakeholder, Functional, Dysfunctional, Weight' },
  ]},
  fuzzy_ahp_type1: { name: 'Fuzzy AHP Type-1', emoji: '🔺', files: [
    { key: 'criteria_file', label: 'Criteria matrix', hint: 'Pairwise comparison matrix of criteria' },
    { key: 'alternatives_file', label: 'Alternatives ratings', hint: 'Columns: Alternative, Expert, [criteria...]' },
    { key: 'weights_file', label: 'Expert weights', hint: 'Columns: Expert, Weight' },
  ]},
  fuzzy_ahp_type2: { name: 'Fuzzy AHP Type-2', emoji: '🔺', files: [
    { key: 'data_file', label: 'Data file', hint: 'Columns: Expert, Weight, [criteria pairs...]' },
  ]},
  fuzzy_topsis: { name: 'Fuzzy TOPSIS', emoji: '🌀', files: [
    { key: 'data_file', label: 'Ratings matrix', hint: 'Columns: Alternative, [criteria with linguistic ratings]' },
    { key: 'scale_file', label: 'Rating scale', hint: 'Columns: Expert Rating, Trapezoidal Number' },
  ]},
  intuitionistic_topsis: { name: 'Intuitionistic TOPSIS', emoji: '🌀', files: [
    { key: 'data_file', label: 'Ratings matrix', hint: 'Columns: Alternative, [criteria with linguistic ratings]' },
    { key: 'scale_file', label: 'IFS scale', hint: 'Columns: Expert Rating, Membership Degree, Non-membership Degree, Hesitancy Degree' },
  ]},
  fuzzy_delphi: { name: 'Fuzzy Delphi', emoji: '🔮', files: [
    { key: 'data_file', label: 'Data file', hint: 'Columns: Alternative, Expert, Expert Weight, [criteria...]' },
  ]},
  intuitionistic_delphi: { name: 'Intuitionistic Delphi', emoji: '🔮', files: [
    { key: 'data_file', label: 'Data file (IFS)', hint: 'Columns: Alternative, Expert, Expert Weight, [criteria as (μ,ν,π) tuples]' },
  ]},
}

function DropZone({ fileKey, label, hint, value, onChange }) {
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef(null)

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) onChange(fileKey, file)
  }, [fileKey, onChange])

  return (
    <div
      className={`border-2 border-dashed rounded-xl p-5 text-center cursor-pointer transition-colors ${
        dragging ? 'border-blue-400 bg-blue-50' : value ? 'border-green-400 bg-green-50' : 'border-slate-300 hover:border-blue-300 hover:bg-slate-50'
      }`}
      onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".csv"
        className="hidden"
        onChange={(e) => { if (e.target.files[0]) onChange(fileKey, e.target.files[0]) }}
      />
      {value ? (
        <div className="flex items-center justify-center gap-2 text-green-700">
          <span className="text-xl">✓</span>
          <div className="text-left">
            <p className="font-medium text-sm">{value.name}</p>
            <p className="text-xs text-green-600">{(value.size / 1024).toFixed(1)} KB</p>
          </div>
        </div>
      ) : (
        <>
          <p className="text-slate-500 text-sm font-medium mb-1">📎 {label}</p>
          <p className="text-slate-400 text-xs">{hint}</p>
          <p className="text-blue-500 text-xs mt-2">Drag & drop or click to browse</p>
        </>
      )}
    </div>
  )
}

export default function Analysis() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { addSession } = useApp()

  const method = searchParams.get('method') || 'moscow'
  const info = METHOD_INFO[method]

  const [uploadedFiles, setUploadedFiles] = useState({})
  const [sessionId, setSessionId] = useState(null)
  const [status, setStatus] = useState('idle')
  const [error, setError] = useState(null)
  const [results, setResults] = useState(null)
  const [conflicts, setConflicts] = useState([])
  const [aiSummary, setAiSummary] = useState(null)
  const [aiLoading, setAiLoading] = useState(false)

  const handleFileChange = (key, file) => {
    setUploadedFiles((prev) => ({ ...prev, [key]: file }))
    setSessionId(null)
    setStatus('idle')
  }

  const allFilesSelected = info?.files.every((f) => uploadedFiles[f.key])

  const handleCalculate = async () => {
    setError(null)
    setStatus('uploading')
    try {
      const uploadRes = await uploadFiles(method, uploadedFiles)
      const sid = uploadRes.session_id
      setSessionId(sid)
      setStatus('calculating')

      const analysisRes = await analyzeMethod(method, sid)
      setResults(analysisRes.results)
      setConflicts(analysisRes.conflicts || [])
      setStatus('done')

      addSession({
        session_id: sid,
        method,
        method_name: info.name,
        results: analysisRes.results,
        conflicts: analysisRes.conflicts || [],
      })

      setAiLoading(true)
      try {
        const [interpRes, conflictRes] = await Promise.all([
          getAiInterpretation(sid),
          analysisRes.conflicts?.length ? getAiConflicts(sid) : Promise.resolve({ conflicts: [] }),
        ])
        setAiSummary(interpRes.summary)
        if (conflictRes.conflicts?.length) setConflicts(conflictRes.conflicts)
      } finally {
        setAiLoading(false)
      }
    } catch (e) {
      setError(e.response?.data?.detail || e.message)
      setStatus('error')
    }
  }

  if (!info) {
    return <div className="p-10 text-center text-slate-500">Unknown method: {method}</div>
  }

  return (
    <div className="flex flex-1 min-h-0">
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-6 py-8">
          {/* Header */}
          <div className="flex items-center gap-3 mb-6">
            <button onClick={() => navigate('/')} className="text-slate-400 hover:text-slate-600 text-sm">← Back</button>
            <span className="text-slate-300">|</span>
            <span className="text-2xl">{info.emoji}</span>
            <h1 className="text-2xl font-bold text-slate-900">{info.name}</h1>
          </div>

          {/* Upload section */}
          <div className="card p-6 mb-6">
            <h2 className="font-semibold text-slate-700 mb-4">1. Upload Data Files</h2>
            <div className={`grid gap-4 ${info.files.length === 1 ? 'grid-cols-1' : info.files.length === 2 ? 'grid-cols-2' : 'grid-cols-3'}`}>
              {info.files.map((f) => (
                <DropZone
                  key={f.key}
                  fileKey={f.key}
                  label={f.label}
                  hint={f.hint}
                  value={uploadedFiles[f.key]}
                  onChange={handleFileChange}
                />
              ))}
            </div>

            <div className="mt-5 flex items-center gap-4">
              <button
                className="btn-primary px-8 py-2.5 text-base"
                disabled={!allFilesSelected || status === 'uploading' || status === 'calculating'}
                onClick={handleCalculate}
              >
                {status === 'uploading' ? '⏫ Uploading...' :
                 status === 'calculating' ? '⚙️ Calculating...' :
                 '▶ Calculate'}
              </button>
              {!allFilesSelected && (
                <span className="text-sm text-slate-400">
                  Upload {info.files.length === 1 ? 'the file' : 'all files'} to run analysis
                </span>
              )}
            </div>

            {error && (
              <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-3 text-red-700 text-sm">
                <strong>Error:</strong> {error}
              </div>
            )}
          </div>

          {/* Results */}
          {status === 'done' && results && (
            <>
              {conflicts.length > 0 && (
                <div className="mb-6">
                  <h2 className="font-semibold text-slate-700 mb-3">⚠️ Detected Conflicts</h2>
                  <div className="flex flex-col gap-3">
                    {conflicts.map((c, i) => (
                      <ConflictAlert key={i} conflict={c} />
                    ))}
                  </div>
                </div>
              )}

              <div className="card p-6 mb-6">
                <h2 className="font-semibold text-slate-700 mb-4">2. Analysis Results</h2>
                <ResultsChart results={results} method={method} />
              </div>

              <div className={`card p-6 mb-6 border-l-4 border-l-violet-400 ${aiLoading ? 'animate-pulse' : ''}`}>
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-lg">🤖</span>
                  <h2 className="font-semibold text-violet-700">AI Interpretation</h2>
                  {aiLoading && <span className="text-xs bg-violet-100 text-violet-600 px-2 py-0.5 rounded-full">analyzing...</span>}
                </div>
                {aiSummary ? (
                  <p className="text-slate-600 text-sm leading-relaxed italic">{aiSummary}</p>
                ) : aiLoading ? (
                  <div className="h-16 bg-slate-50 rounded-lg flex items-center justify-center">
                    <span className="text-slate-400 text-sm">Generating analysis...</span>
                  </div>
                ) : (
                  <div className="flex items-center gap-2 text-slate-400 text-sm">
                    <span>🔑</span>
                    <span>AI unavailable — set <code className="bg-slate-100 px-1 rounded">GEMINI_API_KEY</code> to enable automatic insights</span>
                  </div>
                )}
              </div>

              <div className="card p-6">
                <h2 className="font-semibold text-slate-700 mb-4">3. Priority Table</h2>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-slate-200">
                        <th className="text-left py-2 pr-4 text-slate-500 font-medium">Rank</th>
                        <th className="text-left py-2 pr-4 text-slate-500 font-medium">Alternative</th>
                        <th className="text-right py-2 pr-4 text-slate-500 font-medium">Score</th>
                        <th className="text-left py-2 text-slate-500 font-medium">Interpretation</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(results)
                        .sort(([, a], [, b]) => b.score - a.score)
                        .map(([alt, data], i) => (
                          <tr key={alt} className="border-b border-slate-100 hover:bg-slate-50">
                            <td className="py-2.5 pr-4 text-slate-400 font-mono">#{i + 1}</td>
                            <td className="py-2.5 pr-4 font-medium text-slate-800">{alt}</td>
                            <td className="py-2.5 pr-4 text-right">
                              <span className={`font-bold ${data.score >= 70 ? 'text-green-600' : data.score >= 40 ? 'text-amber-600' : 'text-red-500'}`}>
                                {typeof data.score === 'number' ? data.score.toFixed(1) : data.score}
                              </span>
                            </td>
                            <td className="py-2.5 text-slate-500">{data.comment}</td>
                          </tr>
                        ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      <ChatPanel sessionId={sessionId} disabled={status !== 'done'} />
    </div>
  )
}
