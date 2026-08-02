# Prompt Log — Mid-Course Project

Selected features: **Tags / Labels** and **Search + Combined Filters**

---

## Feature 1: Tags / Labels

### Prompt 1 — Tag validation in models and storage

| | |
|---|---|
| **Prompt goal** | Add tag rules to the data layer before API routes. |
| **Prompt summary** | Create `app/models.py` and `app/storage.py` with tag list validation, storage CRUD, and case-insensitive tag filter. Show code; wait for approval. |
| **AI response summary** | Proposed `_validate_tags()`, Pydantic models, JSON storage, and `get_all_tasks(tag=...)`. |
| **What I accepted** | Shared validator, v2 field validators, storage filter logic. |
| **What I edited or rejected** | Required `Field(default_factory=list)`; required explicit-null rejection on PATCH for all fields except `assignee`. |

### Prompt 2 — Baseline verification script

| | |
|---|---|
| **Prompt goal** | Verify tag behavior before wiring the API. |
| **Prompt summary** | Create `tests/verify_baseline.py` with tag trim/dedupe, blank-tag rejection, and storage checks. |
| **AI response summary** | Proposed 15 standalone checks with `_reset()` and PASS/FAIL output. |
| **What I accepted** | Full check list and reset pattern. |
| **What I edited or rejected** | Approved as proposed. |

### Prompt 3 — Mid-course gap analysis

| | |
|---|---|
| **Prompt goal** | Ship Feature 1 without rewriting working code. |
| **Prompt summary** | Inspect `models.py`, `storage.py`, `main.py`, `frontend/index.html`, `tests/test_tasks.py`. Gap analysis only. |
| **AI response summary** | Tags already implemented in backend and frontend; recommended **tests only** (4 pytest cases). |
| **What I accepted** | Tests-only plan. |
| **What I edited or rejected** | Rejected re-implementing validation or storage. |

### Prompt 4 — Tag pytest tests

| | |
|---|---|
| **Prompt goal** | Lock in tag behavior at the API level. |
| **Prompt summary** | Add four tests: duplicate normalization, tags preserved on unrelated PATCH, case-insensitive filter, blank tag → 422. |
| **AI response summary** | Added tests; **26 passed**. |
| **What I accepted** | All four test names and assertions. |
| **What I edited or rejected** | No application code changes. |

---

## Feature 2: Search + Combined Filters

### Prompt 1 — Load real tasks in the frontend

| | |
|---|---|
| **Prompt goal** | Replace static sample cards with live API data. |
| **Prompt summary** | Fetch `GET /tasks` on load; loading/error/empty states; render by status; escape HTML. |
| **AI response summary** | Proposed `loadTasks()` and `renderBoard()`. |
| **What I accepted** | Fetch-on-load, HTML escaping, priority sort. |
| **What I edited or rejected** | Approved; filter UI deferred to Feature 2. |

### Prompt 2 — Gap analysis

| | |
|---|---|
| **Prompt goal** | Plan search/filters without duplicating backend logic. |
| **Prompt summary** | Inspect `main.py`, `storage.py`, `frontend/index.html`. Report gaps; smallest plan; wait for approval. |
| **AI response summary** | Backend filtering complete; missing filter bar, query params in `loadTasks()`, combined-filter tests. |
| **What I accepted** | Frontend + tests only; no backend changes. |
| **What I edited or rejected** | Rejected client-side filtering of `currentTasks`. |

### Prompt 3 — Filter bar and pytest coverage

| | |
|---|---|
| **Prompt goal** | Deliver Feature 2 end-to-end. |
| **Prompt summary** | Seven pytest tests; filter bar with Apply/Clear; `URLSearchParams`; preserve filters after CRUD/drag. |
| **AI response summary** | Added tests and filter UI; **33 passed**. |
| **What I accepted** | All seven tests, filter controls, active-state styling. |
| **What I edited or rejected** | No backend edits — tests confirmed existing behavior. |

---

## Weak prompt → Strong prompt

**Weak:** "Add search and filters to my task tracker."

**Strong:** Inspect `app/main.py`, `app/storage.py`, and `frontend/index.html` first. Implement Search + Combined Filters with the smallest change set. Filter via `GET /tasks` query params with **AND** logic; search title/description only. Add filter bar with Apply/Clear; do not filter in JavaScript. Add pytest for combined filters and invalid enum → 422. Show plan and wait for approval.

---

## Evidence: inspected existing code first

- Feature 1: explicit inspect prompt across five files before any mid-course tag work.
- Feature 2: inspect prompt before filter bar; agent reported backend already complete.
- Every major step used **show plan → wait for approval → apply**.

## Evidence: avoided unnecessary code changes

- Feature 1: **0 application files changed** — only 4 pytest tests added.
- Feature 2: **0 backend files changed** — frontend filter bar + 7 pytest tests only.
- Rejected full rewrites of `_validate_tags()` and `get_all_tasks()` when gap analysis showed they already met requirements.

## Evidence: pytest and browser verification

| Milestone | Pytest | Manual browser |
|-----------|--------|----------------|
| Baseline | 22 passed | Swagger `/docs` |
| Feature 1 | 26 passed | Tags on cards via create/edit modal |
| Feature 2 | 33 passed | Apply/Clear filters, combined AND, empty state, CRUD/drag with filters active |
