# Verification Evidence

## Baseline

Before mid-course feature work, the existing pytest suite (`tests/test_tasks.py`) passed with **22 tests**.

---

## Feature 1: Tags / Labels

| Check | Result | Evidence |
|-------|--------|----------|
| Duplicate tags normalized | Pass | `test_post_duplicate_tags_normalize_preserving_order` — `["  alpha ", "beta", "alpha"]` → `["alpha", "beta"]` |
| Blank tags rejected with 422 | Pass | `test_post_blank_tags_returns_422` |
| Tags preserved during unrelated PATCH | Pass | `test_patch_unrelated_update_preserves_tags` |
| Tag filtering case-insensitive | Pass | `test_get_tasks_tag_filter_is_case_insensitive` |

**Manual frontend checks**

- Create/edit modal accepts comma-separated tags and sends them to the API.
- Task cards display tag chips after reload.
- Verified in browser: tags appear correctly on cards after create and edit.

**Pytest after Feature 1:** 26 passed.

---

## Feature 2: Search + Combined Filters

| Check | Result | Evidence |
|-------|--------|----------|
| Search by title | Pass | `test_get_tasks_supports_search` |
| Search by description | Pass | `test_get_tasks_search_matches_description` |
| Filter by tag | Pass | `test_get_tasks_supports_tag_filter` |
| Filter by status | Pass | `test_get_tasks_filter_by_status` |
| Filter by priority | Pass | `test_get_tasks_filter_by_priority` |
| Filter by assignee | Pass | `test_get_tasks_filter_by_assignee` |
| Combined filters use AND logic | Pass | `test_get_tasks_combined_filters_use_and_logic` |
| Invalid enum filters return 422 | Pass | `test_get_tasks_invalid_status_returns_422`, `test_get_tasks_invalid_priority_returns_422` |
| No matches → empty result | Pass | `test_get_tasks_with_no_matches_returns_empty_list` |

**Manual frontend checks** (backend: `uvicorn app.main:app --reload`; frontend: `python -m http.server 5500` in `frontend/`)

- [x] Search by title narrows visible cards
- [x] Search by description matches keyword in description only
- [x] Tag, status, priority, and assignee filters each narrow results
- [x] Combined filters show only tasks matching **all** active criteria
- [x] Clear Filters restores the full board and removes active styling
- [x] Empty results show column empty messages without an error page
- [x] Create, edit, delete, and drag-and-drop reload the board with active filters still applied

**Manual verification result:** In the browser, Apply/Clear filter controls behaved as expected: combined filters narrowed the board using AND logic (`docs/midcourse/prompt-log.md`, Feature 2 manual browser row); Clear restored the full board; empty filter results showed an empty-state board without errors; create, edit, delete, and drag-and-drop reloads kept active filters applied (`docs/midcourse/reflection.md`; `docs/midcourse/prompt-log.md`). Search-by-title, search-by-description-only, and individual tag/status/priority/assignee filter narrowing were manually re-verified in the browser during final submission cleanup.

**Pytest after Feature 2:** 33 passed. No backend files were changed for this feature.

---

## Final tests

```
33 passed
```

Command: `PYTHONPATH=. python -m pytest tests/ -v`

---

## Break tests

| Break test | Action | Expected | Automated test |
|------------|--------|----------|----------------|
| Blank tag | `POST /tasks` with `"tags": ["good", "   "]` | 422 | `test_post_blank_tags_returns_422` |
| Invalid status query | `GET /tasks?status=Blocked` | 422 | `test_get_tasks_invalid_status_returns_422` |
