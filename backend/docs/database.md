# Database management (Phase A)

Prodify uses **environment-based configuration**, **Alembic migrations**, and an optional **dev-only** `create_all` path. Production must never rely on `create_all`.

## Configuration

From `backend/`:

```bash
cp .env.example .env
# or: ./scripts/dev_setup.sh
```

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | SQLAlchemy URL (default `sqlite:///./prodify.db`) |
| `ENVIRONMENT` | `development` \| `production` \| `test` |
| `AUTO_CREATE_DB` | If `true`, runs `create_all` on startup (**dev only**) |
| `LOG_LEVEL` | Python log level |

`.env` is gitignored. `DATABASE_URL` is loaded via Pydantic Settings in `app/core/config.py`.

### Production rules

- `ENVIRONMENT=production`
- `AUTO_CREATE_DB=false` (enforced — startup fails if both production + auto create)
- Apply schema with Alembic before serving traffic

## Development workflow (recommended)

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
./scripts/dev_setup.sh    # creates .env if missing, runs migrations
uvicorn app.main:app --reload
```

### Alternative: quick local hack (no Alembic)

In `.env` set `AUTO_CREATE_DB=true`. Tables are created on startup via `init_db()`. Use only for throwaway local DBs — not for shared or production environments.

## Migrations (Alembic)

```bash
cd backend
source venv/bin/activate

alembic upgrade head
alembic current
alembic revision --autogenerate -m "describe_change"
alembic downgrade -1
```

Initial revision: `001_initial` — full schema (users, workspaces, work_items, tasks, sessions, behavioral_states) including `ix_sessions_user_id_started_at`.

## Tests

```bash
cd backend
pytest
```

Tests set `ENVIRONMENT=test`, in-memory SQLite, and `AUTO_CREATE_DB=true` via `tests/conftest.py` (no Alembic required in CI).

## Architecture

```
.env / environment
    → app/core/config.py (Settings)
    → app/core/database.py (engine, SessionLocal, init_db)
    → alembic/env.py (same Settings + Base.metadata)
    → app/main.py (init_db only if AUTO_CREATE_DB)
```

API routes are unchanged; only the data platform bootstrap path was formalized.
