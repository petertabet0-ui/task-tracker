# Release Evidence — Final Project

Branch: `final-project`  
Repository: https://github.com/petertabet0-ui/task-tracker

## Baseline (pre-release engineering work)

| Check | Result | How verified |
|-------|--------|--------------|
| Health endpoint | Pass | `GET /health` → `{"status":"ok"}` |
| Backend starts | Pass | `python -m uvicorn app.main:app --reload` |
| Deployed frontend | Pass | https://task-tracker-j0w.pages.dev (Cloudflare Pages); committed `API_BASE` calls https://task-tracker-j1ru.onrender.com; create/edit verified against deployed backend |
| Automated tests | Pass | `python -m pytest tests/ -q` → **33 passed, 1 warning in 1.21s** |

Warning: StarletteDeprecationWarning about `httpx` vs `httpx2` in TestClient — pre-existing, non-blocking.

## Release deliverables

| Deliverable | Status | Evidence |
|-------------|--------|----------|
| GitHub Actions CI | Pass | GitHub Actions CI completed successfully on the `final-project` branch. Multiple pushed commits produced green CI runs. |
| Dockerfile | Pass | `docker build` + `GET /health` from container; non-root user verified (see below) |
| `.dockerignore` | Pass | Excludes `.env`, `.venv`, development artifacts, and `docs/`, `tests/`, `frontend/` from the API image |
| README Final Project section | Pass | Documents setup, tests, Docker, release deliverables, and AI-use/verification summary |
| AGENTS.md | Pass | Contains repository-specific AI workflow constraints and commands |
| docs/final-ai-review.md | Pass | Contains 3 graded code-review comments, 3 graded security findings, manual check, rejected AI output, 3 AI rules, ownership statement |
| docs/ai-playbook.md | Pass | Completed personal reusable workflow, verified examples, AI rules, rejected output, weak-to-strong prompt, Decision Card, ownership summary |

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

## Claim-versus-reality checks

### 1. Automated test suite

- **Claim:** The automated test suite passes.
- **How checked:** `python -m pytest tests/ -q`
- **Reality:** 33 tests passed with 1 non-blocking deprecation warning.
- **Action/result:** Claim confirmed.

### 2. GitHub Actions CI

- **Claim:** GitHub Actions CI runs successfully on the final-project branch.
- **How checked:** GitHub Actions workflow history.
- **Reality:** Multiple CI runs on final-project completed successfully with green checkmarks.
- **Action/result:** Claim confirmed.

### 3. Docker non-root user

- **Claim:** The Docker container runs as a non-root user.
- **How checked:** `docker run --rm task-tracker id`
- **Reality:** The first check returned `uid=0(root)`, so the claim was false. The Dockerfile was changed to create and use `appuser`. After rebuilding, the command returned:
  `uid=999(appuser) gid=999(appuser) groups=999(appuser)`
- **Action/result:** Claim initially rejected, corrected, and then verified.

## Scope confirmation

No new product features were added during release engineering. Deployment wiring changes were made as integration work, not product features:

- `frontend/index.html`: `API_BASE` changed to the Render backend (`https://task-tracker-j1ru.onrender.com`)
- `app/main.py`: CORS updated to allow the Cloudflare Pages frontend (`https://task-tracker-j0w.pages.dev`)
