from fastapi import HTTPException

from app.models import TaskStatus

VALID_TRANSITIONS = {
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
}


def validate_status_transition(current_status: TaskStatus, new_status: TaskStatus) -> None:
    if (current_status, new_status) not in VALID_TRANSITIONS:
        raise HTTPException(status_code=422, detail="Invalid status transition")
