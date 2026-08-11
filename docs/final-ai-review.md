# Final AI Review — Task Tracker Release

## Tools used

- **Cursor Agent** — primary: inspected repo, proposed CI/Docker/docs, ran pytest
- **ChatGPT** — clarified requirements, tightened prompts, reviewed design choices
- Used inspect → propose → approve → apply workflow (same as mid-course)

## What AI did well

- Mapped missing deliverables against a verified baseline without re-reading the assignment brief
- Proposed minimal Dockerfile (API-only) aligned with current architecture (no static file serving)
- Inspected `app/` and `tests/` imports before trimming `requirements.txt`, then verified the reduced set with a fresh venv and pytest
- Identified that Feature 1 and Feature 2 backend behavior already existed and recommended the smallest follow-up changes (tests and frontend only)

## What required human review

- Confirming `requirements.txt` trim (removes unused Windows-only and unrelated packages only)
- Confirming Docker runs API only (frontend stays local)
- Approving exact doc wording and evidence baseline numbers
- Correcting AI drafts before apply (see rejected output below)

## Risks avoided

- No new product features added during release work
- CI configured without `continue-on-error` or skipped pytest
- `.dockerignore` excludes `.env` and dev artifacts

---

## Graded code-review comments

### 1. Dockerfile ran as root

| | |
|---|---|
| **File/location** | `Dockerfile` |
| **Review finding** | Initial image had no `USER` instruction; `docker run --rm task-tracker id` returned `uid=0(root)`. |
| **Grade/severity** | High |
| **Resolution/status** | Fixed — added system user `appuser`, `chown -R appuser:appuser /app`, and `USER appuser`. Re-verified: `uid=999(appuser) gid=999(appuser) groups=999(appuser)`. |

### 2. Mutable default for tags list

| | |
|---|---|
| **File/location** | `app/models.py` — `TaskCreate.tags` |
| **Review finding** | AI first proposed `tags: list[str] = []`, which shares one list across model instances. |
| **Grade/severity** | Medium |
| **Resolution/status** | Fixed before merge — changed to `tags: list[str] = Field(default_factory=list)` per my review (`docs/midcourse/prompt-log.md`). |

### 3. Unnecessary tag-logic rewrite at mid-course

| | |
|---|---|
| **File/location** | Feature 1 gap analysis (`app/models.py`, `app/storage.py`, frontend) |
| **Review finding** | Tag validation, storage, modal input, and chips already met requirements; a full re-implementation would duplicate working code. |
| **Grade/severity** | Low (scope/process) |
| **Resolution/status** | Accepted tests-only plan — added four pytest tests; zero application file changes for Feature 1. |

---

## Graded security findings

### 1. Docker container privilege

| | |
|---|---|
| **Finding** | Container initially ran as root inside the image. |
| **Severity** | High |
| **How it was checked** | `docker run --rm task-tracker id` (documented in `docs/release-evidence.md`) |
| **Mitigation/status** | Corrected Dockerfile to run as non-root `appuser`; verified after rebuild. |

### 2. Secrets and dev artifacts in image

| | |
|---|---|
| **Finding** | `.env` or local dev files could be copied into the image if not excluded. |
| **Severity** | Medium |
| **How it was checked** | Inspected `.dockerignore` — lists `.env`, `.env.*`, `.venv`, `.git`, `tests/`, `docs/` |
| **Mitigation/status** | Mitigated — sensitive and non-runtime paths excluded from build context. |

### 3. API input validation

| | |
|---|---|
| **Finding** | Unvalidated task input could allow bad data into storage. |
| **Severity** | Medium |
| **How it was checked** | `python -m pytest tests/ -q` — includes `test_post_blank_tags_returns_422`, `test_post_blank_title_returns_422`, `test_get_tasks_invalid_status_returns_422` |
| **Mitigation/status** | Mitigated — Pydantic validators on `TaskCreate`/`TaskUpdate` reject invalid input with HTTP 422; covered by automated tests. |

---

## Manual check

Documented in `docs/midcourse/verification.md` (Feature 1 — Tags / Labels).

| | |
|---|---|
| **What I tested** | Tag entry in the create/edit modal and tag chips on task cards |
| **Steps** | Started backend (`uvicorn app.main:app --reload`) and frontend (`python -m http.server 5500` in `frontend/`). Created a task with comma-separated tags in the modal. Reloaded the board. Opened the task in edit mode. |
| **Expected result** | Tags from the modal appear as chips on the correct card after reload. |
| **Actual result** | Tags appeared on cards after create and edit, matching submitted values. |
| **Pass/fail** | **Pass** (as recorded in mid-course verification evidence) |

---

## Rejected AI output

| | |
|---|---|
| **What AI proposed** | `tags: list[str] = []` as the default for `TaskCreate.tags` in `app/models.py` |
| **Why I rejected it** | A mutable list default is shared across instances and can cause cross-task data leakage in Python/Pydantic models. |
| **What I did instead** | Required `tags: list[str] = Field(default_factory=list)` and kept explicit-null rejection on PATCH fields (`docs/midcourse/prompt-log.md`). |
| **Result** | Tag behavior verified by pytest (`test_post_duplicate_tags_normalize_preserving_order`, `test_patch_unrelated_update_preserves_tags`, and related tests); final suite **33 passed**. |

---

## Personal AI-use rules

1. **I inspect existing code and documentation before accepting AI changes**, especially when a feature may already be implemented.
2. **I require deliberate review and explicit approval** before the agent applies edits; I reject or revise drafts that over-scope or weaken validation.
3. **I verify behavior with pytest and documented manual checks** before treating a claim as complete; I do not rely on AI assertions alone.

---

## Verification summary

AI proposed files and commands; I confirmed:

1. `python -m pytest tests/ -q` → **33 passed** (1 non-blocking deprecation warning)
2. Docker health check returns `{"status":"ok"}`
3. GitHub Actions CI green on `final-project`
4. Docker non-root user: `docker run --rm task-tracker id` → `uid=999(appuser) gid=999(appuser) groups=999(appuser)`

---

## Takeaway

Release engineering (CI, Docker, docs) benefits from the same constrained AI workflow as feature work: inspect first, smallest diff, explicit approval, pytest as gate.

---

## Ownership statement

I reviewed all AI-assisted changes in this repository, performed the verification steps documented above and in `docs/release-evidence.md`, and understand the submitted implementation. I take responsibility for the final submitted code, tests, Dockerfile, and documentation.
