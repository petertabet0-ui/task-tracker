# AI Playbook — Task Tracker

Reusable workflow for AI-assisted work in this repository.

## Tools used

- **Cursor Agent** — inspect repo, propose changes, run pytest, implement edits after approval
- **ChatGPT** — clarify requirements, tighten prompts, review design choices

---

## 1. Set context

When starting AI-assisted work on this repo, I tell the agent:

| Item | Value for this project |
|------|------------------------|
| **Branch** | `final-project` |
| **Baseline** | `python -m pytest tests/ -q` → **33 passed**, 1 non-blocking deprecation warning; `GET /health` → `{"status":"ok"}` |
| **Scope** | Release engineering only — **no new product features** |
| **Constraints** | Smallest safe diff; preserve existing behavior; inspect before editing; verify before claiming success; wait for approval before applying changes |

---

## 2. Inspect-first prompt (example)

Real example from Feature 2 (Search + Combined Filters):

```
Inspect app/main.py, app/storage.py, and frontend/index.html.
Do not modify any files yet.

Report: what already works for search and combined filters, what is missing,
and the smallest change set.

Wait for my approval before applying changes.
```

Outcome in this project: backend filtering was already complete; only frontend filter bar and pytest tests were needed.

---

## 3. Implementation prompt (example)

Real example from Feature 2 implementation:

```
Approve the plan.

Implement Feature 2 with the smallest change set:
- Add seven pytest tests to tests/test_tasks.py
- Modify only frontend/index.html for the filter bar (search, tag, status, priority, assignee)
- Build URLSearchParams from non-empty values; backend remains source of truth
- Do not modify app/models.py, app/storage.py, or app/main.py unless a test fails

Run the full pytest suite and report results.
```

Outcome in this project: 33 tests passed; no backend files changed.

---

## 4. Verification checklist

Mark only what existing project evidence supports:

- [x] `python -m pytest tests/ -q` → **33 passed**, 1 non-blocking warning (`docs/release-evidence.md`)
- [x] `GET /health` → `{"status":"ok"}` (`docs/release-evidence.md` baseline)
- [x] Frontend create/edit works against local API (`docs/release-evidence.md` baseline; `README.md` Final Project section)
- [x] Manual tag check: tags appear on cards after create/edit (`docs/midcourse/verification.md`, Feature 1)
- [x] GitHub Actions CI green on `final-project` (`docs/release-evidence.md`)
- [x] `docker build -t task-tracker .` successful (`docs/release-evidence.md`)
- [x] Docker health: `GET /health` from container → `{"status":"ok"}` (`docs/release-evidence.md`)
- [x] Docker non-root: `docker run --rm task-tracker id` → `uid=999(appuser) gid=999(appuser) groups=999(appuser)` (`docs/release-evidence.md`)

---

## 5. Anti-patterns (reject these)

- Rewriting working CRUD, storage, or filter logic
- Adding auth, database, or "nice to have" features during release
- CI with `continue-on-error`, `|| true`, or skipped pytest
- Copying `.env` into Docker images

---

## 6. Key commands

```bash
python -m uvicorn app.main:app --reload
cd frontend && python -m http.server 5500
python -m pytest tests/ -q
docker build -t task-tracker .
docker run --rm -p 8000:8000 task-tracker
docker run --rm task-tracker id
```

---

## Personal AI-use rules

1. **I inspect existing code and documentation before accepting AI changes**, especially when a feature may already be implemented.
2. **I require deliberate review and explicit approval** before the agent applies edits; I reject or revise drafts that over-scope or weaken validation.
3. **I verify behavior with pytest and documented manual checks** before treating a claim as complete; I do not rely on AI assertions alone.

---

## Rejected AI output (example)

| | |
|---|---|
| **AI proposed** | `tags: list[str] = []` as the default for `TaskCreate.tags` in `app/models.py` |
| **Why I rejected it** | A mutable list default is shared across instances and can cause cross-task data leakage. |
| **What I did instead** | `tags: list[str] = Field(default_factory=list)` (`docs/midcourse/prompt-log.md`) |
| **Result** | Tag behavior verified by pytest; final suite **33 passed** |

---

## Weak prompt → Strong prompt

From `docs/midcourse/prompt-log.md`:

**Weak:** "Add search and filters to my task tracker."

**Strong:** Inspect `app/main.py`, `app/storage.py`, and `frontend/index.html` first. Implement Search + Combined Filters with the smallest change set. Filter via `GET /tasks` query params with **AND** logic; search title/description only. Add filter bar with Apply/Clear; do not filter in JavaScript. Add pytest for combined filters and invalid enum → 422. Show plan and wait for approval.

---

## Decision Card — Docker non-root user

Project decision record (from `docs/release-evidence.md` and `Dockerfile` changes). Not a separate official course template — fields based on verified evidence only.

| | |
|---|---|
| **Decision / topic** | Run the API container as a non-root user |
| **Context / problem** | After `docker build`, `docker run --rm task-tracker id` returned `uid=0(root)` — container ran as root |
| **Options considered** | (1) Leave as root — simpler but weaker security posture. (2) Add dedicated non-root user with ownership of `/app` including `data/` — required for JSON read/write |
| **Decision made** | Create system user `appuser`, `chown -R appuser:appuser /app`, set `USER appuser` in `Dockerfile` |
| **Why** | Reduces container privilege; `data/tasks.json` still writable by the app process |
| **Verification / evidence** | Rebuilt image; `docker run --rm task-tracker id` → `uid=999(appuser) gid=999(appuser) groups=999(appuser)`; health check still returns `{"status":"ok"}` |
| **Outcome** | Claim initially false, corrected, then verified (`docs/release-evidence.md`, Claim-versus-reality check #3) |

---

## Ownership / verification summary

I reviewed AI-assisted changes in this repository, confirmed verification in `docs/release-evidence.md` and `docs/final-ai-review.md`, and do not treat AI output as complete without pytest and documented checks. I take responsibility for the submitted code, tests, Dockerfile, and documentation (`README.md`, Final Project section).
