from pydantic import ValidationError

from app.models import TaskCreate, TaskPriority, TaskStatus, TaskUpdate
from app.storage import (
    _reset,
    add_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
)


def check(name: str, condition: bool) -> None:
    if condition:
        print(f"PASS: {name}")
        return
    raise AssertionError(f"FAIL: {name}")


def check_raises_validation_error(name: str, action) -> None:
    try:
        action()
    except ValidationError:
        print(f"PASS: {name}")
        return
    except Exception as exc:
        raise AssertionError(f"FAIL: {name} (unexpected error: {exc})") from exc
    raise AssertionError(f"FAIL: {name} (expected ValidationError)")


_reset()

try:
    # 1. Blank title is rejected.
    check_raises_validation_error(
        "blank title is rejected",
        lambda: TaskCreate(title=""),
    )

    # 2. Whitespace-only title is rejected.
    check_raises_validation_error(
        "whitespace-only title is rejected",
        lambda: TaskCreate(title="   "),
    )

    # 3. Title over 200 characters is rejected.
    check_raises_validation_error(
        "title over 200 characters is rejected",
        lambda: TaskCreate(title="x" * 201),
    )

    # 4. Valid TaskCreate applies defaults.
    created = TaskCreate(title="Valid task")
    check("default status is ToDo", created.status == TaskStatus.TODO)
    check("default priority is Medium", created.priority == TaskPriority.MEDIUM)
    check("default description is empty string", created.description == "")
    check("default assignee is None", created.assignee is None)
    check("default tags is empty list", created.tags == [])

    # 5. Extra fields are rejected.
    check_raises_validation_error(
        "extra fields are rejected",
        lambda: TaskCreate(title="Valid task", unexpected="nope"),
    )

    # 6. Invalid status is rejected.
    check_raises_validation_error(
        "invalid status is rejected",
        lambda: TaskCreate(title="Valid task", status="NotAStatus"),
    )

    # 7. Tags are trimmed and duplicate tags are removed while preserving order.
    tagged = TaskCreate(title="Tagged task", tags=["  alpha ", "beta", "alpha", "  beta  "])
    check("tags are trimmed", tagged.tags == ["alpha", "beta"])
    check("duplicate tags are removed preserving order", tagged.tags == ["alpha", "beta"])

    # 8. Blank tags are rejected.
    check_raises_validation_error(
        "blank tags are rejected",
        lambda: TaskCreate(title="Valid task", tags=["good", "   "]),
    )

    # 9. TaskUpdate rejects explicit null for title.
    check_raises_validation_error(
        "TaskUpdate rejects explicit null for title",
        lambda: TaskUpdate.model_validate({"title": None}),
    )

    # 10. TaskUpdate allows explicit null for assignee.
    update_assignee = TaskUpdate.model_validate({"assignee": None})
    check(
        "TaskUpdate allows explicit null for assignee",
        update_assignee.assignee is None,
    )

    # 11. add_task creates a task with id and timestamps.
    stored = add_task(
        TaskCreate(
            title="Storage baseline task",
            description="searchable description",
            tags=["Alpha"],
        )
    )
    check("add_task returns an id", bool(stored.id))
    check("add_task sets created_at", stored.created_at is not None)
    check("add_task sets updated_at", stored.updated_at is not None)

    # 12. get_task_by_id finds the created task.
    fetched = get_task_by_id(stored.id)
    check(
        "get_task_by_id finds the created task",
        fetched is not None and fetched.id == stored.id,
    )

    # 13. get_all_tasks search and tag filters work.
    search_matches = get_all_tasks(search="baseline")
    check(
        "get_all_tasks search filter works",
        len(search_matches) == 1 and search_matches[0].id == stored.id,
    )

    tag_matches = get_all_tasks(tag="alpha")
    check(
        "get_all_tasks tag filter works",
        len(tag_matches) == 1 and tag_matches[0].id == stored.id,
    )

    # 14. update_task changes the title.
    updated = update_task(stored.id, TaskUpdate(title="Updated baseline task"))
    check(
        "update_task changes the title",
        updated is not None and updated.title == "Updated baseline task",
    )

    # 15. delete_task removes the task.
    deleted = delete_task(stored.id)
    check("delete_task returns True", deleted is True)
    check("delete_task removes the task", get_task_by_id(stored.id) is None)

finally:
    _reset()
