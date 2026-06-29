import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage import reset_storage

@pytest.fixture(autouse=True)
def clean_storage():
    reset_storage()
    yield
    reset_storage()

client = TestClient(app)

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
