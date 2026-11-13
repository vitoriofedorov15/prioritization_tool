#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$ROOT/.venv/bin/python"
if [[ ! -x "$PYTHON" || ! -d "$ROOT/frontend/node_modules" ]]; then
  echo "Install dependencies first; see README.md Quick start." >&2
  exit 1
fi
for port in 8000 5173; do
  if lsof -tiTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "Port $port is busy. Stop its service or run the servers manually on other ports." >&2
    exit 1
  fi
done
cleanup() {
  kill "${BACKEND_PID:-}" "${FRONTEND_PID:-}" 2>/dev/null || true
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
cd "$ROOT/backend"
"$PYTHON" -m uvicorn main:app --host 127.0.0.1 --port 8000 --env-file "$ROOT/.env" &
BACKEND_PID=$!
cd "$ROOT/frontend"
npm run dev -- --host 127.0.0.1 --strictPort &
FRONTEND_PID=$!
echo "Frontend: http://localhost:5173 | API: http://localhost:8000/docs"
while kill -0 "$BACKEND_PID" 2>/dev/null && kill -0 "$FRONTEND_PID" 2>/dev/null; do
  sleep 1
done
exit 1
