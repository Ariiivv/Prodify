#!/usr/bin/env bash
# Local development bootstrap: env file + Alembic migrations
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

if [[ -d venv ]]; then
  # shellcheck source=/dev/null
  source venv/bin/activate
fi

alembic upgrade head
echo "Database ready. Start API with: uvicorn app.main:app --reload"
