# Mid-Course Project — User Stories

Selected features: **Tags / Labels** and **Search + Combined Filters**

Scope is limited to the existing Task Tracker (FastAPI backend, vanilla frontend, JSON storage).

---

## Tags / Labels

### Story 1 — Add tags when creating a task

**As a** student organizing coursework, **I want** to add optional tags when I create a task, **so that** I can group related work (e.g. `backend`, `report`).

**Acceptance criteria**

- **Success:** A new task can be created with zero or more tags; tags appear on the task card after reload.
- **Success:** Creating a task without tags results in an empty tag list.
- **Success:** Tags entered as a comma-separated list are stored as separate labels on the task.
- **Failure:** A blank tag returns **422** with a validation error.
- **Failure:** More than 10 tags on one task returns **422**.
- **Failure:** Any tag longer than 30 characters returns **422**.

> **Corrected AI assumption:** Tags are **not** a single free-text label on the task. Each task holds a **list of separate tag values**.

---

### Story 2 — Normalize and validate tags on update

**As a** student maintaining my board, **I want** tag edits to be cleaned automatically, **so that** duplicate or messy tags do not clutter tasks.

**Acceptance criteria**

- **Success:** Updating tags trims whitespace on each tag before saving.
- **Success:** Duplicate tags in the same request are removed while **preserving first-seen order** (e.g. `" alpha "`, `alpha`, `beta` → `alpha`, `beta`).
- **Success:** Updating a task with an empty tag list clears all tags on that task.
- **Failure:** Setting tags to `null` returns **422**; omitting tags from an update leaves existing tags unchanged.
- **Failure:** Invalid tag content (blank entry, too many tags, tag too long) returns **422** and leaves the task unchanged.

> **Corrected AI assumption:** Duplicate tags are **removed on save**, not kept as repeated labels on the same task.

---

### Story 3 — Filter tasks by tag and keep tags on unrelated edits

**As a** student reviewing one topic, **I want** to filter the board by tag and still edit other fields safely, **so that** labels stay useful without accidental data loss.

**Acceptance criteria**

- **Success:** Filtering by tag shows only tasks that include that tag.
- **Success:** Tag filtering is **case-insensitive** (`Backend` matches `backend`).
- **Success:** Updating only title, priority, or assignee leaves existing tags unchanged.
- **Success:** Tag chips remain visible on cards after unrelated updates.
- **Failure:** A tag filter with no matches returns **200** and an empty result set (not **404**).
- **Edge case:** A task with no tags is excluded from any non-empty tag filter.

---

## Search + Combined Filters

### Story 4 — Search tasks by title or description

**As a** student with many tasks, **I want** to search by keyword, **so that** I can quickly find work without scanning every column.

**Acceptance criteria**

- **Success:** Searching for a keyword returns tasks where the keyword appears in the **title or description** (case-insensitive).
- **Success:** Search matches substrings (e.g. `api` matches `"Build API endpoints"`).
- **Success:** Applying search refreshes the board to show only matching tasks.
- **Failure / edge:** Search does **not** match assignee, tags, status, or priority.
- **Failure / edge:** No matches returns **200** with an empty board and a clear empty state (not an error).

> **Corrected AI assumption:** Search is **not** full-text across every task field. It applies only to **title and description**.

---

### Story 5 — Combine filters with AND logic

**As a** student planning my week, **I want** to combine status, priority, assignee, tag, and search filters, **so that** I see only tasks that match **all** selected criteria.

**Acceptance criteria**

- **Success:** Applying multiple filters (e.g. status, priority, and tag) returns only tasks that match **every** active filter.
- **Success:** Adding an assignee filter further narrows results (exact assignee match).
- **Success:** Leaving a filter unset means it is not applied.
- **Failure / edge:** Combined filters with no matches return **200** and an empty result set.
- **Failure:** Invalid status or priority filter values (e.g. `Blocked`, `Urgent`) return **422**.

> **Corrected AI assumption:** Filters use **AND** logic, not OR. A task must satisfy **every** active filter to appear in results.

---

### Story 6 — Frontend filter controls and clear action

**As a** student using the Kanban board, **I want** visible filter controls and a way to reset them, **so that** I can explore tasks and return to the full board easily.

**Acceptance criteria**

- **Success:** The board exposes controls for search, tag, status, priority, and assignee.
- **Success:** Applying filters reloads tasks from the server using the selected criteria.
- **Success:** A **Clear filters** action resets all controls and shows the full unfiltered task list.
- **Success:** Active filters are visually distinguishable from the default state.
- **Failure / edge:** Clear filters works even when the current result set is already empty.
- **Failure:** Invalid status or priority selections are prevented in the UI or shown as a readable error when the server returns **422**.

> **Corrected AI assumption:** The filter bar is **part of the planned mid-course work**, not an assumed existing UI on the board.
