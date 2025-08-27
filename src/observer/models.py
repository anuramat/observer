"""Pydantic models for Observer."""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ProjectType(str, Enum):
    """Project type categories."""

    SYSTEM_CONFIG = "system_configuration"
    ENTERTAINMENT = "entertainment_and_procrastination"
    ML_RESEARCH = "machine_learning_research"


class ActivityOutput(BaseModel):
    """AI model output schema."""

    project_name: str = Field(description="Name of the current project")
    project_type: ProjectType
    details: str = Field(description="What the user is doing")
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Confidence score")


class ActivityRecord(BaseModel):
    """Database record schema."""

    id: Optional[int] = None
    timestamp: datetime
    window_title: str
    window_class: str
    project_name: str
    project_type: ProjectType
    details: str
    confidence: float
    screenshot_path: Optional[str] = None
    context_summary: Optional[str] = None


class ContextWindow(BaseModel):
    """Context for AI model."""

    recent_activities: list[ActivityRecord]
    current_window: dict
    session_summary: Optional[str] = None
