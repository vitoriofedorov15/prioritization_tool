import { useState } from 'react'

export default function ConflictAlert({ conflict }) {
  const [expanded, setExpanded] = useState(false)
  const isHard = conflict.type === 'hard'

  return (
    <div
      className={`border rounded-xl overflow-hidden ${
        isHard ? 'border-red-200 bg-red-50' : 'border-amber-200 bg-amber-50'
      }`}
    >
      <button
        onClick={() => setExpanded((v) => !v)}
        className="w-full flex items-start gap-3 p-4 text-left"
      >
        <span className="text-lg flex-shrink-0">{isHard ? '🔴' : '🟡'}</span>
        <div className="flex-1 min-w-0">
          <p className={`font-semibold text-sm ${isHard ? 'text-red-800' : 'text-amber-800'}`}>
            {isHard ? 'Hard Conflict' : 'Soft Conflict'}: {conflict.alternative}
          </p>
          <p className={`text-xs mt-0.5 ${isHard ? 'text-red-600' : 'text-amber-600'}`}>
            {conflict.description}
          </p>
        </div>
        <span className={`text-xs flex-shrink-0 ${isHard ? 'text-red-400' : 'text-amber-400'}`}>
          {expanded ? '▲' : '▼'} AI explanation
        </span>
      </button>

      {expanded && (
        <div className={`border-t px-4 py-3 ${isHard ? 'border-red-100 bg-red-50/80' : 'border-amber-100 bg-amber-50/80'}`}>
          {conflict.ai_why || conflict.ai_resolution ? (
            <div className="flex flex-col gap-3">
              {conflict.ai_why && (
                <div>
                  <p className={`text-xs font-semibold mb-1 ${isHard ? 'text-red-700' : 'text-amber-700'}`}>
                    💡 Why this conflict occurred:
                  </p>
                  <p className="text-xs text-slate-600 leading-relaxed">{conflict.ai_why}</p>
                </div>
              )}
              {conflict.ai_resolution && (
                <div>
                  <p className={`text-xs font-semibold mb-1 ${isHard ? 'text-red-700' : 'text-amber-700'}`}>
                    🛠️ How to resolve:
                  </p>
                  <p className="text-xs text-slate-600 leading-relaxed">{conflict.ai_resolution}</p>
                </div>
              )}
            </div>
          ) : (
            <p className="text-xs text-slate-400 italic">AI explanation not available</p>
          )}
        </div>
      )}
    </div>
  )
}
