from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from app.models import TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority, CommentCreate, CommentResponse
from app.storage import add_task, get_task, list_tasks, update_task, delete_task, add_comment, list_comments, delete_comment, count_comments
from app.business_rules import validate_status_transition

app = FastAPI(title="Task Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(payload: TaskCreate):
    return add_task(payload)

@app.get("/tasks", response_model=list[TaskResponse])
def read_tasks(
    status: Optional[TaskStatus] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    overdue: bool = Query(False),
):
    return list_tasks(
        status=status.value if status else None,
        priority=priority.value if priority else None,
        overdue=overdue,
    )

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def patch_task(task_id: str, payload: TaskUpdate):
    existing = get_task(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")
    if payload.status and payload.status != existing.status:
        if not validate_status_transition(existing.status, payload.status):
            raise HTTPException(
                status_code=422,
                detail=f"Invalid transition from {existing.status} to {payload.status}",
            )
    return update_task(task_id, payload)

@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: str):
    if not delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks/{task_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(task_id: str, payload: CommentCreate):
    result = add_comment(task_id, payload)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

@app.get("/tasks/{task_id}/comments", response_model=list[CommentResponse])
def read_comments(task_id: str):
    result = list_comments(task_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

@app.delete("/tasks/{task_id}/comments/{comment_id}", status_code=204)
def remove_comment(task_id: str, comment_id: str):
    result = delete_comment(task_id, comment_id)
    if result == "task_not_found":
        raise HTTPException(status_code=404, detail="Task not found")
    if result == "comment_not_found":
        raise HTTPException(status_code=404, detail="Comment not found")
