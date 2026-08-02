# Agent Instructions — Task Tracker

## Project

FastAPI CRUD API + vanilla Kanban frontend. JSON storage in `data/tasks.json`. No database, no authentication.

## Commands

```bash
# Backend
python -m uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend && python -m http.server 5500

# Tests
python -m pytest tests/ -q
```

## Constraints

- Do **not** add product features during release/final-project work unless explicitly requested.
- Prefer the smallest safe diff; build on existing code — do not rebuild working features.
- `app/business_rules.py` owns status transition validation — do not duplicate in routes.
- `app/storage.py` owns JSON persistence — keep API routes thin.
- Frontend is a single file: `frontend/index.html` (vanilla HTML/CSS/JS only).
- CORS allows `http://127.0.0.1:5500` and `http://localhost:5500`.

## Workflow

1. Inspect relevant files before proposing changes.
2. Produce a gap analysis and wait for approval.
3. Implement incrementally; run `python -m pytest tests/ -q` after backend changes.
4. Match existing Pydantic v2 patterns in `app/models.py`.

## Key files

| File | Role |
|------|------|
| `app/main.py` | Routes, CORS |
| `app/models.py` | Pydantic models and validation |
| `app/storage.py` | JSON CRUD and filters |
| `app/business_rules.py` | Status transition rules |
| `frontend/index.html` | Kanban UI |
| `tests/test_tasks.py` | API integration tests (33 tests) |
