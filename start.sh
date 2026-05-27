#!/bin/bash
# Start AI Prioritization Tool (backend + frontend)

ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$ROOT/.venv/bin/python3"
UVICORN="$ROOT/.venv/bin/uvicorn"

# Load .env if present (keeps the key out of version control)
if [ -f "$ROOT/.env" ]; then
  export $(grep -v '^#' "$ROOT/.env" | xargs)
fi

if [ -z "$GEMINI_API_KEY" ]; then
  echo "  ⚠️  GEMINI_API_KEY is not set — AI features will be disabled."
  echo "     Add it to .env (see .env.example) or export it before running:"
  echo "     export GEMINI_API_KEY=AIzaSy..."
  echo "     Get a free key: https://aistudio.google.com/app/apikey"
  echo ""
fi

# Kill any existing processes on our ports
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null

echo "Starting backend on http://localhost:8000 ..."
cd "$ROOT/backend"
"$UVICORN" main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

echo "Starting frontend on http://localhost:5173 ..."
cd "$ROOT/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "  Backend:  http://localhost:8000  (API docs: http://localhost:8000/docs)"
echo "  Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
