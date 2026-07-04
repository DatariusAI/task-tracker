from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Optional
from datetime import datetime, date
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
    description: Optional[str] = Field(None, max_length=2000)
    status: TaskStatus = TaskStatus.ToDo
    priority: TaskPriority = TaskPriority.Medium
    assignee: Optional[str] = Field(None, max_length=200)
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be blank or whitespace")
        return v.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = Field(None, max_length=200)
    due_date: Optional[date] = None

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
    due_date: Optional[date] = None

class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, v):
        if not v.strip():
            raise ValueError("Comment text cannot be blank")
        return v.strip()

class CommentResponse(BaseModel):
    id: str
    task_id: str
    text: str
    created_at: datetime
