from datetime import datetime, timezone
import uuid
from app.models import TaskCreate, TaskUpdate, TaskResponse

_tasks = {}

def add_task(payload):
    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "title": payload.title,
        "description": payload.description,
        "status": payload.status.value,
        "priority": payload.priority.value,
        "assignee": payload.assignee,
        "created_at": datetime.now(timezone.utc),
    }
    _tasks[task_id] = task
    return TaskResponse(**task)

def get_task(task_id):
    task = _tasks.get(task_id)
    return TaskResponse(**task) if task else None

def list_tasks(status=None, priority=None):
    results = list(_tasks.values())
    if status:
        results = [t for t in results if t["status"] == status]
    if priority:
        results = [t for t in results if t["priority"] == priority]
    return [TaskResponse(**t) for t in results]

def update_task(task_id, payload):
    task = _tasks.get(task_id)
    if not task:
        return None
    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        if hasattr(value, "value"):
            task[key] = value.value
        else:
            task[key] = value
    return TaskResponse(**task)

def delete_task(task_id):
    return _tasks.pop(task_id, None) is not None

def reset_storage():
    _tasks.clear()
