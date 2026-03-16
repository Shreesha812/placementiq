# app/schemas/analysis.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class AnalysisRequest(BaseModel):
    resume_id: UUID
    jd_text: str
    jd_title: str | None = None
    jd_company: str | None = None


class ScoreBreakdownItem(BaseModel):
    score: float
    weight: float
    contribution: float


class ScoreBreakdown(BaseModel):
    skill_match: ScoreBreakdownItem
    experience_weight: ScoreBreakdownItem
    project_relevance: ScoreBreakdownItem
    keyword_context: ScoreBreakdownItem


class AnalysisOut(BaseModel):
    id: UUID
    overall_score: float
    score_breakdown: dict
    matched_skills: list[str]
    missing_skills: list[str]
    resume_skills: list[str]
    jd_skills: list[str]
    llm_insights: dict | None = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}