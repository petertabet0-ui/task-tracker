# AI Playbook — Task Tracker

Reusable workflow for AI-assisted work in this repository.

**Tools:** Cursor Agent (inspect repo, propose changes, run pytest, implement after approval); ChatGPT (clarify requirements, tighten prompts, review design choices).

**Project context:** Branch `final-project`; baseline `python -m pytest tests/ -q` → **33 passed**, 1 non-blocking deprecation warning; `GET /health` → `{"status":"ok"}`; committed frontend uses `https://task-tracker-j1ru.onrender.com` as `API_BASE`.

## When I reach for AI first

- **Gap analysis before feature work** — e.g. Feature 1 tags: inspect `models.py`, `storage.py`, `main.py`, `frontend/index.html`, `tests/test_tasks.py` before editing (`docs/midcourse/prompt-log.md`).
- **Mapping release deliverables** — ask the agent to compare the repo against CI/Docker/docs requirements without re-reading the whole assignment brief.
- **Inspect-first prompts** — real Feature 2 example:

```
Inspect app/main.py, app/storage.py, and frontend/index.html.
Do not modify any files yet.

Report: what already works for search and combined filters, what is missing,
and the smallest change set.

Wait for my approval before applying changes.
```

Outcome: backend filtering was already complete; only frontend filter bar and pytest tests were needed.

- **Implementation prompts after approval** — Feature 2 example: seven pytest tests, filter bar only in `frontend/index.html`, `URLSearchParams`, no backend edits unless a test fails; **33 passed**.

## When I do not

- Rewriting working CRUD, storage, or filter logic when gap analysis shows behavior already meets requirements.
- Adding auth, database, or "nice to have" features during release engineering.
- Accepting client-side filtering when the backend already supports query params with AND logic.
- CI with `continue-on-error`, `|| true`, or skipped pytest.
- Copying `.env` or dev artifacts into Docker images.

**Weak prompt:** "Add search and filters to my task tracker."

**Strong prompt:** Inspect `app/main.py`, `app/storage.py`, and `frontend/index.html` first. Implement Search + Combined Filters with the smallest change set. Filter via `GET /tasks` query params with **AND** logic; search title/description only. Add filter bar with Apply/Clear; do not filter in JavaScript. Add pytest for combined filters and invalid enum → 422. Show plan and wait for approval.

## My non-negotiables

1. **Inspect existing code and documentation before accepting AI changes**, especially when a feature may already be implemented.
2. **Smallest safe diff** — build on working code; do not rebuild features that already pass tests.
3. **No new product features during release work** unless explicitly requested.
4. **Explicit approval before apply** — inspect → propose → approve → apply for every major step.
5. **Verify with pytest and documented checks** before treating a claim as complete; do not rely on AI assertions alone.

## My review rules

- Reject or revise drafts that over-scope, weaken validation, or duplicate working logic.
- Require `Field(default_factory=list)` for mutable defaults; reject `tags: list[str] = []` (`docs/midcourse/prompt-log.md`).
- Keep status transition validation in `app/business_rules.py` and JSON persistence in `app/storage.py`; keep API routes thin (`AGENTS.md`).
- Run `python -m pytest tests/ -q` after backend-impacting changes.
- Match existing Pydantic v2 patterns in `app/models.py`.
- Human-review deployment wiring (`API_BASE`, CORS) as integration changes, not product features.

Verified checklist:

- [x] `python -m pytest tests/ -q` → **33 passed**, 1 non-blocking warning (`docs/release-evidence.md`)
- [x] `GET /health` → `{"status":"ok"}` (`docs/release-evidence.md` baseline)
- [x] Deployed frontend create/edit verified against Render backend (`README.md`, `docs/release-evidence.md`)
- [x] Manual tag check: tags appear on cards after create/edit (`docs/midcourse/verification.md`, Feature 1)
- [x] GitHub Actions CI Run #8 (commit `4615345`, success): https://github.com/petertabet0-ui/task-tracker/actions/runs/31483999941
- [x] `docker build -t task-tracker .` successful (`docs/release-evidence.md`)
- [x] Docker health: `GET /health` from container → `{"status":"ok"}` (`docs/release-evidence.md`)
- [x] Docker non-root: `docker run --rm task-tracker id` → `uid=999(appuser) gid=999(appuser) groups=999(appuser)` (`docs/release-evidence.md`)

**Key commands:**

```bash
python -m uvicorn app.main:app --reload
cd frontend && python -m http.server 5500
python -m pytest tests/ -q
docker build -t task-tracker .
docker run --rm -p 8000:8000 task-tracker
docker run --rm task-tracker id
```

## What I am still figuring out

- How much deployment wiring (CORS, `API_BASE`, hosted URLs) belongs in release-engineering scope versus mid-course feature delivery.
- When pytest alone is enough versus when browser checks are mandatory for frontend filter and modal behavior (`docs/midcourse/reflection.md`).
- Whether to standardize on one hosted backend URL or keep local/prod switching documented separately without changing committed defaults.

## Decision Card

### New feature

Inspect relevant files first; report gaps and the smallest change set; wait for approval. Feature 1 shipped as four pytest tests with zero application file changes; Feature 2 shipped as frontend filter controls plus seven tests with no backend edits (`docs/midcourse/prompt-log.md`).

### Code review

Review AI output against actual code and tests before merge. Examples from this project: reject a full tag-logic rewrite when behavior already worked; fix Dockerfile running as root; reject `tags: list[str] = []` in favor of `Field(default_factory=list)`.

### Debugging

Use failing pytest output and targeted inspection before asking for broad rewrites. Break tests in `docs/midcourse/verification.md` (blank tag → 422, invalid status query → 422) map to concrete automated cases rather than speculative fixes.

### Infrastructure

**Docker non-root:** Initial image ran as root (`uid=0`). I added system user `appuser`, `chown -R appuser:appuser /app`, and `USER appuser`. Re-verified: `uid=999(appuser) gid=999(appuser) groups=999(appuser)`; health check still returns `{"status":"ok"}` (`docs/release-evidence.md`, Claim-versus-reality check #3).

CI must run pytest on push/PR without `continue-on-error`. CORS in `app/main.py` was reviewed as deployment wiring for Cloudflare Pages, not a product feature.

### Never-paste

Do not paste secrets (`.env`) into Docker images or commits. Do not accept mutable list defaults or explicit-null PATCH behavior without review. Do not copy AI-suggested full rewrites of working validators or storage filters.

### One rule

**Inspect → propose → approve → verify with pytest (and documented manual checks when UI is involved) before calling work complete.**

---

I reviewed AI-assisted changes in this repository, confirmed verification in `docs/release-evidence.md` and `docs/final-ai-review.md`, and take responsibility for the submitted code, tests, Dockerfile, and documentation.
