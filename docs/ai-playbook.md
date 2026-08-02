# AI Playbook — Task Tracker

Reusable workflow for AI-assisted work in this repository.

## 1. Set context

Tell the agent:

- Current branch and verified baseline (tests, health check)
- Scope: release-only vs feature work
- Constraint: no rebuilds; smallest safe diff; approval before edits

## 2. Inspect-first prompt template

```
Inspect [files]. Do not modify yet.
Report: what exists, what's missing, smallest change set.
Wait for approval before applying changes.
```

## 3. Implementation prompt template

```
Implement only [specific files].
Do not change app/ or frontend/ unless required.
Run: python -m pytest tests/ -q
Report results.
```

## 4. Verification checklist

- [ ] `python -m pytest tests/ -q` → 33 passed
- [ ] `GET /health` → `{"status":"ok"}`
- [ ] Frontend create/edit still works (if touching CORS or API)
- [ ] CI green on push (if touching workflow or dependencies)
- [ ] Docker health check (if touching Dockerfile)

## 5. Anti-patterns (reject these)

- Rewriting working CRUD, storage, or filter logic
- Adding auth, database, or "nice to have" features during release
- CI with `continue-on-error`, `|| true`, or skipped pytest
- Copying `.env` into Docker images

## 6. Key commands

```bash
python -m uvicorn app.main:app --reload
cd frontend && python -m http.server 5500
python -m pytest tests/ -q
docker build -t task-tracker .
docker run --rm -p 8000:8000 task-tracker
```
