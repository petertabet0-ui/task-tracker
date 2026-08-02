from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


def _validate_title(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Title cannot be blank")
    if len(value) > 200:
        raise ValueError("Title must be at most 200 characters")
    return value


def _validate_tags(value: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for tag in value:
        trimmed = tag.strip()
        if not trimmed:
            raise ValueError("Tags cannot be blank")
        if len(trimmed) > 30:
            raise ValueError("Each tag must be at most 30 characters")
        if trimmed not in seen:
            seen.add(trimmed)
            normalized.append(trimmed)
    if len(normalized) > 10:
        raise ValueError("At most 10 tags allowed")
    return normalized


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    tags: list[str] = Field(default_factory=list)

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: str) -> str:
        return _validate_title(value)

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        return _validate_tags(value)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    tags: Optional[list[str]] = None

    @model_validator(mode="before")
    @classmethod
    def reject_explicit_nulls(cls, data: object) -> object:
        if not isinstance(data, dict):
            return data
        for field in ("title", "description", "status", "priority", "tags"):
            if field in data and data[field] is None:
                raise ValueError(f"{field} cannot be null")
        return data

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return _validate_title(value)

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, value: Optional[list[str]]) -> Optional[list[str]]:
        if value is None:
            return value
        return _validate_tags(value)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str] = None
    tags: list[str]
    created_at: datetime
    updated_at: datetime
