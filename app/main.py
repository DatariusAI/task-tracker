from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from app.models import TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority
from app.storage import add_task, get_task, list_tasks, update_task, delete_task
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
):
    return list_tasks(
        status=status.value if status else None,
        priority=priority.value if priority else None,
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
