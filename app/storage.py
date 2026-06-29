from datetime import datetime, timezone, date
import uuid
from app.models import TaskCreate, TaskUpdate, TaskResponse, CommentCreate, CommentResponse

_tasks = {}
_comments = {}

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
        "due_date": payload.due_date,
    }
    _tasks[task_id] = task
    return TaskResponse(**task)

def get_task(task_id):
    task = _tasks.get(task_id)
    return TaskResponse(**task) if task else None

def list_tasks(status=None, priority=None, overdue=False):
    results = list(_tasks.values())
    if status:
        results = [t for t in results if t["status"] == status]
    if priority:
        results = [t for t in results if t["priority"] == priority]
    if overdue:
        today = date.today()
        results = [t for t in results if t.get("due_date") and t["due_date"] < today and t["status"] != "Done"]
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
    if task_id in _tasks:
        _tasks.pop(task_id)
        keys_to_remove = [k for k in _comments if k.startswith(task_id + ":")]
        for k in keys_to_remove:
            _comments.pop(k)
        return True
    return False

def reset_storage():
    _tasks.clear()
    _comments.clear()

def add_comment(task_id, payload):
    if task_id not in _tasks:
        return None
    comment_id = str(uuid.uuid4())
    comment = {
        "id": comment_id,
        "task_id": task_id,
        "text": payload.text,
        "created_at": datetime.now(timezone.utc),
    }
    _comments[task_id + ":" + comment_id] = comment
    return CommentResponse(**comment)

def list_comments(task_id):
    if task_id not in _tasks:
        return None
    results = [v for k, v in _comments.items() if k.startswith(task_id + ":")]
    results.sort(key=lambda c: c["created_at"])
    return [CommentResponse(**c) for c in results]

def delete_comment(task_id, comment_id):
    key = task_id + ":" + comment_id
    if task_id not in _tasks:
        return "task_not_found"
    if key not in _comments:
        return "comment_not_found"
    _comments.pop(key)
    return "deleted"

def count_comments(task_id):
    return sum(1 for k in _comments if k.startswith(task_id + ":"))
