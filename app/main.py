from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate
from app.storage import add_task, delete_task, get_all_tasks, get_task_by_id, update_task

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(payload: TaskCreate) -> TaskResponse:
    return add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    assignee: str | None = None,
    tag: str | None = None,
    search: str | None = None,
) -> list[TaskResponse]:
    return get_all_tasks(
        status=status,
        priority=priority,
        assignee=assignee,
        tag=tag,
        search=search,
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: str) -> TaskResponse:
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def patch_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    existing = get_task_by_id(task_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if "status" in payload.model_fields_set:
        validate_status_transition(existing.status, payload.status)

    task = update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: str) -> Response:
    if not delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=204)
