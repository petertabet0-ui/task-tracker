import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

from app.models import TaskCreate, TaskResponse, TaskUpdate

TASKS_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def _ensure_file() -> None:
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]", encoding="utf-8")
        return
    if TASKS_FILE.read_text(encoding="utf-8").strip() == "":
        TASKS_FILE.write_text("[]", encoding="utf-8")


def _load_raw() -> list[dict]:
    _ensure_file()
    content = TASKS_FILE.read_text(encoding="utf-8").strip()
    if not content:
        return []
    return json.loads(content)


def _load_tasks() -> list[TaskResponse]:
    return [TaskResponse.model_validate(record) for record in _load_raw()]


def _save_tasks(tasks: list[TaskResponse]) -> None:
    _ensure_file()
    data = [task.model_dump(mode="json") for task in tasks]
    TASKS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def add_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)
    task = TaskResponse(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        tags=payload.tags,
        created_at=now,
        updated_at=now,
    )
    tasks = _load_tasks()
    tasks.append(task)
    _save_tasks(tasks)
    return task


def get_all_tasks(
    status=None,
    priority=None,
    assignee=None,
    tag=None,
    search=None,
) -> list[TaskResponse]:
    tasks = _load_tasks()

    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if assignee is not None:
        tasks = [task for task in tasks if task.assignee == assignee]
    if tag is not None:
        tag_lower = tag.lower()
        tasks = [
            task
            for task in tasks
            if any(item.lower() == tag_lower for item in task.tags)
        ]
    if search is not None:
        search_lower = search.lower()
        tasks = [
            task
            for task in tasks
            if search_lower in task.title.lower()
            or search_lower in task.description.lower()
        ]

    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    for task in _load_tasks():
        if task.id == task_id:
            return task
    return None


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    tasks = _load_tasks()
    for index, task in enumerate(tasks):
        if task.id != task_id:
            continue

        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            return task

        current = task.model_dump()
        if not any(current.get(key) != value for key, value in updates.items()):
            return task

        updated = task.model_copy(
            update={**updates, "updated_at": datetime.now(timezone.utc)}
        )
        tasks[index] = updated
        _save_tasks(tasks)
        return updated

    return None


def delete_task(task_id: str) -> bool:
    tasks = _load_tasks()
    filtered = [task for task in tasks if task.id != task_id]
    if len(filtered) == len(tasks):
        return False
    _save_tasks(filtered)
    return True


def _reset() -> None:
    _ensure_file()
    TASKS_FILE.write_text("[]", encoding="utf-8")
