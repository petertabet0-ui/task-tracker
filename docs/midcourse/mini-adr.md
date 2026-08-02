# Mini ADR

## Context

The mid-course project extends the existing Task Tracker with two small, end-to-end features. The application already supports task CRUD, status transitions, and a Kanban frontend backed by JSON file storage. The goal is to add meaningful functionality without large architectural changes, while keeping the work simple, testable, and suitable for an AI-assisted development workflow.

## Decision

The selected features are:

- **Tags / Labels**
- **Search + Combined Filters**

These features were chosen because they are visible on the Kanban board, require coordinated backend and frontend work, and extend the current task model naturally. They fit the project scope: validation rules, query behavior, and UI controls can be delivered incrementally. They are also straightforward to verify with automated tests using the existing API and pytest setup.

## Alternatives Considered

Other options were reviewed but not selected:

- **Due dates + overdue filter** — adds date handling, overdue logic, and extra UI state.
- **Task comments** — introduces a new related entity and additional CRUD flows.
- **Activity log** — requires tracking history and displaying audit data across the app.

Each alternative would expand the data model and testing surface more than the selected features.

## AI Suggestions Reviewed

AI tools suggested several ideas that were intentionally rejected as out of scope:

- Full-text search across all task fields
- OR-based filter combinations
- Bulk operations on tasks
- Persistent saved filters
- Advanced frontend animations

The project will use focused search (title and description), AND-based combined filters, and minimal UI changes aligned with the existing vanilla frontend.

## Consequences

Implementation will remain incremental: backend behavior and tests first, then frontend updates. The JSON storage approach stays unchanged, avoiding database migration. Scope stays bounded, making documentation and review easier to maintain throughout the mid-course deliverable.
