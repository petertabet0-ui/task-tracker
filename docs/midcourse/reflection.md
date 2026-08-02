# Reflection — AI-Assisted Mid-Course Project

For this Task Tracker project, I used **ChatGPT** and **Cursor Agent**. Cursor Agent was my primary tool inside the repository: it read existing files, proposed changes, ran pytest, and implemented the frontend in small approved steps. ChatGPT helped me clarify requirements, rewrite weak prompts, and review design choices before I sent instructions back to the agent.

AI significantly accelerated work when I paired it with inspection first. For Feature 2 (Search + Combined Filters), I asked Cursor to review `app/main.py`, `app/storage.py`, and `frontend/index.html` before editing anything. It reported that backend AND-filter logic already existed and recommended adding only a filter bar plus pytest tests. That avoided rewriting `get_all_tasks()` and kept the feature delivery focused.

AI also slowed me down when its first suggestions needed correction. During early model design, it proposed `tags: list[str] = []` and did not initially reject explicit `null` for PATCH fields like `tags` and `title`. I had to inspect the draft, compare it to the update rules I wanted, and request revisions before approval. That extra review took time, but it prevented bad PATCH behavior in the API.

My review changed the final result in another important way. I used an inspect → propose → approve → apply workflow for every step, rejected a full re-implementation of tag logic during Feature 1, and required tests before marking features complete. Feature 1 shipped as four new pytest tests with zero application code changes; Feature 2 shipped as frontend filter controls plus seven tests, with no backend edits.

Pytest and browser testing mattered because generated code can look correct while still failing in integration. Automated tests verified duplicate tag normalization, blank tags returning 422, combined filters using AND logic, and invalid enum queries failing safely — ending at **33 passed**. Manual browser checks covered what pytest cannot: comma-separated tag entry, tag chips on cards, Apply/Clear filters, empty result states, and keeping filters active after create, edit, delete, and drag-and-drop.

My main takeaway is to use AI as a fast draft generator, not an automatic decision maker. Strong prompts name constraints, require inspection first, and wait for approval. I still own validation rules, scope control, and verification. Used responsibly, AI sped up repetitive implementation; used blindly, it would have created rework later.
