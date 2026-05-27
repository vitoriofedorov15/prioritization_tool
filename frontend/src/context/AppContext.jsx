import { createContext, useContext, useState } from 'react'

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const [completedSessions, setCompletedSessions] = useState([])

  const addSession = (session) => {
    setCompletedSessions((prev) => {
      const exists = prev.find((s) => s.session_id === session.session_id)
      if (exists) {
        return prev.map((s) => (s.session_id === session.session_id ? session : s))
      }
      return [...prev, session]
    })
  }

  return (
    <AppContext.Provider value={{ completedSessions, addSession }}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  return useContext(AppContext)
}
