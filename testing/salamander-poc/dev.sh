#!/usr/bin/env bash
# dev.sh -- boot the salamander backend + frontend together and stream
# both consoles into one with [backend]/[frontend] prefixes.
#
# Idempotent: creates the backend venv and installs deps on first run, and
# runs `npm install` if frontend/node_modules is missing. Subsequent runs
# skip straight to booting.
#
# Press Ctrl-C to stop both services.

set -e
cd "$(dirname "$0")"

# --- colors (tput would be nicer but ANSI is universal enough for a terminal)
CYAN=$'\033[36m'
MAGENTA=$'\033[35m'
GREEN=$'\033[32m'
DIM=$'\033[2m'
RESET=$'\033[0m'

note() { echo "${GREEN}>${RESET} $*"; }

# --- Backend setup (idempotent) ---
if [ ! -d backend/venv ]; then
  note "creating backend/venv (first run, ~5s)"
  python3 -m venv backend/venv
fi

note "syncing backend deps"
backend/venv/bin/pip install --disable-pip-version-check -q -r backend/requirements.txt

# --- Frontend setup (idempotent) ---
if [ ! -d frontend/node_modules ]; then
  note "installing frontend deps (first run, ~10s)"
  (cd frontend && npm install --silent)
fi

# --- Boot ---
note "backend  -> http://localhost:8000"
note "frontend -> http://localhost:5173"
note "ctrl-c to stop"
echo

# python -u plus our flush=True prints means logs land in real time.
# awk prefixes each line with a colored tag and fflush() so the pipe
# doesn't buffer when stdout isn't a tty.
(cd backend && ./venv/bin/python -u main.py 2>&1) \
  | awk -v p="${CYAN}[backend ]${RESET}" '{ print p, $0; fflush(); }' &

(cd frontend && npm run dev 2>&1) \
  | awk -v p="${MAGENTA}[frontend]${RESET}" '{ print p, $0; fflush(); }' &

cleanup() {
  echo
  note "shutting down..."
  # SIGINT goes to the whole foreground process group on Ctrl-C, but be
  # explicit anyway in case this is invoked under a process manager that
  # only signals the script.
  jobs -p | xargs -r kill 2>/dev/null || true
  wait 2>/dev/null || true
  note "done"
  exit 0
}
trap cleanup INT TERM

wait
