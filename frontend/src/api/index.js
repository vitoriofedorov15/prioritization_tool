import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export async function uploadFiles(method, fileMap) {
  const form = new FormData()
  form.append('method', method)
  for (const [key, file] of Object.entries(fileMap)) {
    if (file) form.append(key, file)
  }
  const { data } = await api.post('/upload', form)
  return data
}

export async function analyzeMethod(method, sessionId) {
  const { data } = await api.post(`/analyze/${method}`, { session_id: sessionId })
  return data
}

export async function getAiInterpretation(sessionId) {
  const { data } = await api.post('/ai/interpret', { session_id: sessionId })
  return data
}

export async function getAiConflicts(sessionId) {
  const { data } = await api.post('/ai/conflicts', { session_id: sessionId })
  return data
}

export async function getSessionData(sessionId) {
  const { data } = await api.get(`/session/${sessionId}`)
  return data
}

export async function streamChat(sessionId, message, history, onChunk, onDone) {
  const response = await fetch('/api/ai/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, message, history }),
  })

  const reader = response.body.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    const text = decoder.decode(value)
    for (const line of text.split('\n')) {
      if (!line.startsWith('data: ')) continue
      try {
        const parsed = JSON.parse(line.slice(6))
        if (parsed.chunk) onChunk(parsed.chunk)
        if (parsed.done) onDone()
      } catch {}
    }
  }
}
