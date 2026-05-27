import { useState, useRef, useEffect } from 'react'
import { streamChat } from '../api'

function Message({ msg }) {
  const isUser = msg.role === 'user'
  return (
    <div className={`flex gap-2 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs flex-shrink-0 ${
        isUser ? 'bg-blue-500 text-white' : 'bg-violet-100 text-violet-700'
      }`}>
        {isUser ? 'U' : '🤖'}
      </div>
      <div className={`max-w-[85%] px-3 py-2 rounded-2xl text-sm leading-relaxed ${
        isUser
          ? 'bg-blue-600 text-white rounded-tr-sm'
          : 'bg-white border border-slate-200 text-slate-700 rounded-tl-sm'
      } ${msg.streaming ? 'streaming' : ''}`}>
        {msg.content}
      </div>
    </div>
  )
}

export default function ChatPanel({ sessionId, disabled }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! I\'m your AI analyst. Once you run an analysis, I can answer questions about the results, explain priorities, and give actionable recommendations.' }
  ])
  const [input, setInput] = useState('')
  const [streaming, setStreaming] = useState(false)
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const send = async () => {
    const text = input.trim()
    if (!text || streaming || disabled || !sessionId) return

    setInput('')
    const userMsg = { role: 'user', content: text }
    const historyForApi = messages.filter((m) => !m.streaming).map((m) => ({
      role: m.role, content: m.content,
    }))

    setMessages((prev) => [...prev, userMsg, { role: 'assistant', content: '', streaming: true }])
    setStreaming(true)

    try {
      await streamChat(
        sessionId,
        text,
        historyForApi,
        (chunk) => {
          setMessages((prev) => {
            const next = [...prev]
            const last = next[next.length - 1]
            if (last?.streaming) next[next.length - 1] = { ...last, content: last.content + chunk }
            return next
          })
        },
        () => {
          setMessages((prev) => {
            const next = [...prev]
            const last = next[next.length - 1]
            if (last?.streaming) next[next.length - 1] = { ...last, streaming: false }
            return next
          })
          setStreaming(false)
        }
      )
    } catch {
      setMessages((prev) => {
        const next = [...prev]
        next[next.length - 1] = { role: 'assistant', content: 'Connection error. Please try again.', streaming: false }
        return next
      })
      setStreaming(false)
    }
  }

  const SUGGESTIONS = [
    'Which requirement should be implemented first?',
    'Explain the methodology in simple terms',
    'What changes if we remove a stakeholder?',
    'Which requirements belong in the first sprint?',
  ]

  return (
    <div className="w-[340px] flex-shrink-0 flex flex-col border-l border-slate-200 bg-white">
      {/* Header */}
      <div className="px-4 py-3 border-b border-slate-100 bg-gradient-to-r from-violet-50 to-white">
        <div className="flex items-center gap-2">
          <span className="text-lg">🤖</span>
          <div>
            <p className="font-semibold text-slate-800 text-sm">AI Assistant</p>
            <p className="text-xs text-violet-500">
              {disabled ? 'Waiting for analysis...' : 'Ready'}
            </p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
        {messages.map((msg, i) => (
          <Message key={i} msg={msg} />
        ))}
        {disabled && messages.length === 1 && (
          <div className="mt-4">
            <p className="text-xs text-slate-400 mb-2 text-center">Example questions after analysis:</p>
            <div className="flex flex-col gap-1.5">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  disabled
                  className="text-left text-xs px-3 py-2 rounded-lg bg-slate-50 text-slate-400 border border-dashed border-slate-200 cursor-default"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}
        {!disabled && messages.length === 1 && (
          <div className="mt-2">
            <p className="text-xs text-slate-400 mb-2 text-center">Try asking:</p>
            <div className="flex flex-col gap-1.5">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => { setInput(s); inputRef.current?.focus() }}
                  className="text-left text-xs px-3 py-2 rounded-lg bg-violet-50 text-violet-600 border border-violet-100 hover:bg-violet-100 transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="p-3 border-t border-slate-100">
        <div className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() } }}
            placeholder={disabled ? 'Run analysis first...' : 'Ask a question...'}
            disabled={disabled || streaming}
            className="flex-1 text-sm border border-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:border-violet-400 disabled:bg-slate-50 disabled:text-slate-400"
          />
          <button
            onClick={send}
            disabled={!input.trim() || streaming || disabled || !sessionId}
            className="w-9 h-9 rounded-lg bg-violet-600 hover:bg-violet-700 text-white flex items-center justify-center disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            {streaming ? (
              <span className="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            )}
          </button>
        </div>
      </div>
    </div>
  )
}
