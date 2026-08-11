# Release Evidence — Final Project

Branch: `final-project`  
Repository: https://github.com/petertabet0-ui/task-tracker

## Baseline (pre-release engineering work)

| Check | Result | How verified |
|-------|--------|--------------|
| Health endpoint | Pass | `GET /health` → `{"status":"ok"}` |
| Backend starts | Pass | `python -m uvicorn app.main:app --reload` |
| Frontend loads | Pass | `python -m http.server 5500` in `frontend/`; create/edit works |
| Automated tests | Pass | `python -m pytest tests/ -q` → **33 passed, 1 warning in 1.21s** |

Warning: StarletteDeprecationWarning about `httpx` vs `httpx2` in TestClient — pre-existing, non-blocking.

## Release deliverables

| Deliverable | Status | Evidence |
|-------------|--------|----------|
| GitHub Actions CI | Pass | GitHub Actions CI completed successfully on the `final-project` branch. Multiple pushed commits produced green CI runs. |
| Dockerfile | Pass | `docker build` + `GET /health` from container; non-root user verified (see below) |
| `.dockerignore` | Pending | No `.env`, `.venv`, or secrets in image |
| README Final Project section | Pending | Documents real commands and baseline |
| AGENTS.md | Pending | Agent constraints and commands |
| docs/final-ai-review.md | Pending | AI review document |
| docs/ai-playbook.md | Pending | Reusable workflow |

## Verification commands

```bash
# Tests (must pass before merge)
python -m pytest tests/ -q

# Docker API
docker build -t task-tracker .
docker run --rm -p 8000:8000 task-tracker
curl http://127.0.0.1:8000/health

# Docker non-root user
docker run --rm task-tracker id
# uid=999(appuser) gid=999(appuser) groups=999(appuser)
# Confirms the container runs as a non-root user.

# CI (after push)
# GitHub → Actions → CI workflow green
```

## Scope confirmation

No new product features. `app/` and `frontend/` unchanged unless a verified bug or security fix is required.
