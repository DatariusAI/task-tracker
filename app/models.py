from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Optional
from datetime import datetime
import uuid

class TaskStatus(str, Enum):
    ToDo = "ToDo"
    InProgress = "InProgress"
    Done = "Done"

class TaskPriority(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.ToDo
    priority: TaskPriority = TaskPriority.Medium
    assignee: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be blank or whitespace")
        return v.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Title cannot be blank or whitespace")
        return v.strip() if v else v

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str] = None
    created_at: datetime
