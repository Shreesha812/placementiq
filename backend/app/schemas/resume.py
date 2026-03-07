# app/schemas/resume.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ResumeOut(BaseModel):
    id: UUID
    file_name: str
    parse_status: str
    version: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}