MISSING_TASK_ID = "00000000-0000-0000-0000-000000000000"


def create_task(client, title="Sample task", **fields):
    response = client.post("/tasks", json={"title": title, **fields})
    assert response.status_code == 201
    return response.json()


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_tasks_creates_task_with_201(client):
    response = client.post("/tasks", json={"title": "New task"})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "New task"
    assert body["id"]


def test_post_applies_default_status_todo(client):
    task = create_task(client, title="Default status task")
    assert task["status"] == "ToDo"


def test_post_applies_default_priority_medium(client):
    task = create_task(client, title="Default priority task")
    assert task["priority"] == "Medium"


def test_post_blank_title_returns_422(client):
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_post_extra_field_returns_422(client):
    response = client.post("/tasks", json={"title": "Valid task", "unexpected": "nope"})
    assert response.status_code == 422


def test_post_invalid_priority_returns_422(client):
    response = client.post("/tasks", json={"title": "Valid task", "priority": "Urgent"})
    assert response.status_code == 422


def test_get_tasks_returns_created_tasks(client):
    created = create_task(client, title="Listed task")
    response = client.get("/tasks")
    assert response.status_code == 200
    ids = [task["id"] for task in response.json()]
    assert created["id"] in ids


def test_get_tasks_supports_search(client):
    created = create_task(
        client,
        title="Searchable task",
        description="find this description",
    )
    response = client.get("/tasks", params={"search": "searchable"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == created["id"]


def test_get_tasks_supports_tag_filter(client):
    created = create_task(client, title="Tagged task", tags=["Alpha"])
    response = client.get("/tasks", params={"tag": "alpha"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == created["id"]


def test_get_tasks_with_no_matches_returns_empty_list(client):
    create_task(client, title="Existing task")
    response = client.get("/tasks", params={"search": "does-not-exist"})
    assert response.status_code == 200
    assert response.json() == []


def test_get_missing_task_returns_404(client):
    response = client.get(f"/tasks/{MISSING_TASK_ID}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_patch_updates_title(client):
    created = create_task(client, title="Original title")
    response = client.patch(
        f"/tasks/{created['id']}",
        json={"title": "Updated title"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"


def test_patch_missing_task_returns_404(client):
    response = client.patch(
        f"/tasks/{MISSING_TASK_ID}",
        json={"title": "Updated title"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_patch_todo_to_in_progress_returns_200(client):
    created = create_task(client, title="Transition ToDo to InProgress")
    response = client.patch(
        f"/tasks/{created['id']}",
        json={"status": "InProgress"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_in_progress_to_done_returns_200(client):
    created = create_task(client, title="Transition InProgress to Done")
    client.patch(f"/tasks/{created['id']}", json={"status": "InProgress"})
    response = client.patch(f"/tasks/{created['id']}", json={"status": "Done"})
    assert response.status_code == 200
    assert response.json()["status"] == "Done"


def test_patch_todo_to_done_returns_422(client):
    created = create_task(client, title="Invalid ToDo to Done")
    response = client.patch(f"/tasks/{created['id']}", json={"status": "Done"})
    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid status transition"


def test_patch_done_to_in_progress_returns_200(client):
    created = create_task(client, title="Transition Done to InProgress")
    client.patch(f"/tasks/{created['id']}", json={"status": "InProgress"})
    client.patch(f"/tasks/{created['id']}", json={"status": "Done"})
    response = client.patch(f"/tasks/{created['id']}", json={"status": "InProgress"})
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_in_progress_to_todo_returns_422(client):
    created = create_task(client, title="Invalid InProgress to ToDo")
    client.patch(f"/tasks/{created['id']}", json={"status": "InProgress"})
    response = client.patch(f"/tasks/{created['id']}", json={"status": "ToDo"})
    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid status transition"


def test_patch_without_status_still_succeeds(client):
    created = create_task(client, title="Title before patch")
    response = client.patch(
        f"/tasks/{created['id']}",
        json={"title": "Title after patch"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Title after patch"
    assert response.json()["status"] == "ToDo"


def test_delete_returns_204(client):
    created = create_task(client, title="Task to delete")
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_task_returns_404(client):
    response = client.delete(f"/tasks/{MISSING_TASK_ID}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
