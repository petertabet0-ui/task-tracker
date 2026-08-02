# Task Tracker

FastAPI task tracker with a vanilla HTML/CSS/JS Kanban frontend and JSON file storage.

Repository: https://github.com/petertabet0-ui/task-tracker

## Prerequisites

- Python 3.13+
- Optional: Docker for containerized API runs

## Local development

### Backend

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Health check: `GET http://127.0.0.1:8000/health` → `{"status":"ok"}`

### Frontend

Serve `frontend/index.html` separately (CORS allows port 5500):

```bash
cd frontend
python -m http.server 5500
```

Open http://127.0.0.1:5500 — the board calls the API at http://127.0.0.1:8000.

### Tests

```bash
python -m pytest tests/ -q
```

Baseline: **33 passed**, 1 deprecation warning (Starlette/httpx).

## Docker (API only)

```bash
docker build -t task-tracker .
docker run --rm -p 8000:8000 task-tracker
curl http://127.0.0.1:8000/health
```

The frontend is not included in the container; run it locally as above.

## Final Project

This release adds engineering deliverables on top of the mid-course baseline — **no new product features**.

| Deliverable | Purpose |
|-------------|---------|
| `.github/workflows/ci.yml` | Run pytest on every push and pull request |
| `Dockerfile` + `.dockerignore` | Reproducible API runtime |
| `AGENTS.md` | Guidance for AI-assisted work in this repo |
| `docs/release-evidence.md` | Verification record for the final release |
| `docs/final-ai-review.md` | AI usage review for the final project |
| `docs/ai-playbook.md` | Reusable AI workflow for this codebase |

**Verified baseline (branch `final-project`):**

- Backend: `python -m uvicorn app.main:app --reload`
- `GET /health` → `{"status":"ok"}`
- Frontend create/edit flow works against the local API
- Tests: `33 passed, 1 warning in 1.21s`

See `docs/release-evidence.md` for full evidence.
