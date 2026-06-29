import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.storage import reset_storage

@pytest.fixture(autouse=True)
def clean_storage():
    reset_storage()
    yield
    reset_storage()

client = TestClient(app)

# ---- Original baseline tests ----

def test_health():
    r = client.get("/health")
    assert r.status_code == 200

def test_create_task():
    r = client.post("/tasks", json={"title": "Test task"})
    assert r.status_code == 201
    assert r.json()["title"] == "Test task"

def test_create_task_blank_title():
    r = client.post("/tasks", json={"title": "   "})
    assert r.status_code == 422

def test_list_tasks():
    client.post("/tasks", json={"title": "A"})
    client.post("/tasks", json={"title": "B"})
    r = client.get("/tasks")
    assert len(r.json()) == 2

def test_filter_by_status():
    client.post("/tasks", json={"title": "A", "status": "ToDo"})
    client.post("/tasks", json={"title": "B", "status": "InProgress"})
    r = client.get("/tasks?status=ToDo")
    assert len(r.json()) == 1

def test_get_task_not_found():
    r = client.get("/tasks/nonexistent")
    assert r.status_code == 404

def test_update_task():
    r = client.post("/tasks", json={"title": "Original"})
    task_id = r.json()["id"]
    r = client.patch(f"/tasks/{task_id}", json={"title": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"

def test_invalid_status_transition():
    r = client.post("/tasks", json={"title": "Task"})
    task_id = r.json()["id"]
    r = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert r.status_code == 422

def test_valid_status_transition():
    r = client.post("/tasks", json={"title": "Task"})
    task_id = r.json()["id"]
    r = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
    assert r.status_code == 200

def test_delete_task():
    r = client.post("/tasks", json={"title": "Delete me"})
    task_id = r.json()["id"]
    r = client.delete(f"/tasks/{task_id}")
    assert r.status_code == 204

def test_delete_task_not_found():
    r = client.delete("/tasks/nonexistent")
    assert r.status_code == 404

# ---- Feature 1: Due Dates tests ----

def test_create_task_with_due_date():
    due = str(date.today() + timedelta(days=7))
    r = client.post("/tasks", json={"title": "Deadline task", "due_date": due})
    assert r.status_code == 201
    assert r.json()["due_date"] == due

def test_create_task_invalid_due_date():
    r = client.post("/tasks", json={"title": "Bad date", "due_date": "not-a-date"})
    assert r.status_code == 422

def test_overdue_filter():
    yesterday = str(date.today() - timedelta(days=1))
    tomorrow = str(date.today() + timedelta(days=1))
    client.post("/tasks", json={"title": "Overdue", "due_date": yesterday})
    client.post("/tasks", json={"title": "Future", "due_date": tomorrow})
    r = client.get("/tasks?overdue=true")
    assert len(r.json()) == 1
    assert r.json()[0]["title"] == "Overdue"

def test_update_due_date():
    r = client.post("/tasks", json={"title": "Task"})
    task_id = r.json()["id"]
    new_date = str(date.today() + timedelta(days=14))
    r = client.patch(f"/tasks/{task_id}", json={"due_date": new_date})
    assert r.status_code == 200
    assert r.json()["due_date"] == new_date

def test_done_tasks_not_overdue():
    yesterday = str(date.today() - timedelta(days=1))
    r = client.post("/tasks", json={"title": "Done task", "due_date": yesterday, "status": "ToDo"})
    task_id = r.json()["id"]
    client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
    client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    r = client.get("/tasks?overdue=true")
    assert len(r.json()) == 0

# ---- Feature 2: Comments tests ----

def test_add_comment():
    r = client.post("/tasks", json={"title": "Task"})
    task_id = r.json()["id"]
    r = client.post(f"/tasks/{task_id}/comments", json={"text": "First comment"})
    assert r.status_code == 201
    assert r.json()["text"] == "First comment"

def test_add_blank_comment():
    r = client.post("/tasks", json={"title": "Task"})
    task_id = r.json()["id"]
    r = client.post(f"/tasks/{task_id}/comments", json={"text": "   "})
    assert r.status_code == 422

def test_list_comments():
    r = client.post("/tasks", json={"title": "Task"})
    task_id = r.json()["id"]
    client.post(f"/tasks/{task_id}/comments", json={"text": "Comment 1"})
    client.post(f"/tasks/{task_id}/comments", json={"text": "Comment 2"})
    r = client.get(f"/tasks/{task_id}/comments")
    assert len(r.json()) == 2

def test_delete_comment():
    r = client.post("/tasks", json={"title": "Task"})
    task_id = r.json()["id"]
    r = client.post(f"/tasks/{task_id}/comments", json={"text": "To delete"})
    comment_id = r.json()["id"]
    r = client.delete(f"/tasks/{task_id}/comments/{comment_id}")
    assert r.status_code == 204

def test_comment_on_missing_task():
    r = client.post("/tasks/nonexistent/comments", json={"text": "Orphan"})
    assert r.status_code == 404

def test_delete_task_removes_comments():
    r = client.post("/tasks", json={"title": "Task"})
    task_id = r.json()["id"]
    client.post(f"/tasks/{task_id}/comments", json={"text": "Comment"})
    client.delete(f"/tasks/{task_id}")
    r = client.get(f"/tasks/{task_id}/comments")
    assert r.status_code == 404
