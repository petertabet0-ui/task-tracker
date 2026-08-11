# Task Tracker

FastAPI task tracker with a vanilla HTML/CSS/JS Kanban frontend and JSON file storage.

Repository: https://github.com/petertabet0-ui/task-tracker

## Prerequisites

- Python 3.13+
- Optional: Docker for containerized API runs

## Deployment

| Component | URL |
|-----------|-----|
| Frontend (Cloudflare Pages) | https://task-tracker-j0w.pages.dev |
| Backend (Render) | https://task-tracker-j1ru.onrender.com |

The committed `frontend/index.html` sets `API_BASE` to the deployed Render backend (`https://task-tracker-j1ru.onrender.com`). Create and edit flows were verified against that deployed API.

## Local development

### Backend (local run)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Health check: `GET http://127.0.0.1:8000/health` → `{"status":"ok"}`

Use this when developing or testing the API locally. Pytest and Docker instructions below also target the local backend.

### Frontend (deployed vs local serve)

**Deployed frontend:** Open https://task-tracker-j0w.pages.dev — the board calls the Render backend configured in the committed source.

**Local static serve (optional):** To preview the HTML locally while still using the deployed API:

```bash
cd frontend
python -m http.server 5500
```

Open http://127.0.0.1:5500 — the committed `API_BASE` still points at `https://task-tracker-j1ru.onrender.com`, not the local uvicorn instance.

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

- Local backend: `python -m uvicorn app.main:app --reload`; `GET /health` → `{"status":"ok"}`
- Deployed frontend: https://task-tracker-j0w.pages.dev calls Render backend; create/edit verified
- Tests: `33 passed, 1 warning in 1.21s`

See `docs/release-evidence.md` for full evidence.

## AI Use and Verification Summary

AI tools were used during this project as an engineering assistant for code review, debugging, test suggestions, documentation, and release preparation. AI-generated suggestions were treated as proposals rather than automatically accepted changes.

I remained responsible for reviewing and verifying the final implementation. Verification included:

- Running the automated test suite with `python -m pytest tests/ -q`.
- Confirming the test baseline of 33 passing tests.
- Manually checking the FastAPI `/health` endpoint.
- Manually testing the frontend create and edit task flow against the deployed Render API.
- Building and running the API with Docker.
- Reviewing AI suggestions against the actual repository code and runtime behavior before accepting them.

AI output that did not match the project requirements or verified behavior was rejected or corrected. The final code, documentation, and release decisions were reviewed and accepted by me.