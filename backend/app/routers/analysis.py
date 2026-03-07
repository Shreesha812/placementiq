# app/routers/analysis.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.analysis_result import AnalysisResult
from app.schemas.analysis import AnalysisRequest, AnalysisOut
from app.services.scoring_engine import run_scoring_engine

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post("/run", response_model=AnalysisOut, status_code=201)
async def run_analysis(
    payload: AnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ── Fetch resume ─────────────────────────────────────────
    result = await db.execute(
        select(Resume).where(
            Resume.id == payload.resume_id,
            Resume.user_id == current_user.id,
        )
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )
    if not resume.raw_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume has not been parsed yet",
        )

    # ── Save or reuse JD ─────────────────────────────────────
    jd_hash = JobDescription.compute_hash(payload.jd_text)

    existing_jd = await db.execute(
        select(JobDescription).where(JobDescription.jd_hash == jd_hash)
    )
    jd = existing_jd.scalar_one_or_none()

    if not jd:
        from app.services.skill_extractor import extract_skills_from_text
        jd_skills = extract_skills_from_text(payload.jd_text)
        jd = JobDescription(
            user_id=current_user.id,
            title=payload.jd_title,
            company=payload.jd_company,
            raw_text=payload.jd_text,
            jd_hash=jd_hash,
            extracted_skills=jd_skills,
        )
        db.add(jd)
        await db.flush()  # get jd.id without committing

    # ── Run scoring engine ────────────────────────────────────
    scores = run_scoring_engine(
        resume_text=resume.raw_text,
        resume_parsed=resume.parsed_json or {},
        jd_text=payload.jd_text,
    )

    # ── Save analysis result ──────────────────────────────────
    analysis = AnalysisResult(
        user_id=current_user.id,
        resume_id=resume.id,
        jd_id=jd.id,
        overall_score=scores["overall_score"],
        score_breakdown=scores["score_breakdown"],
        matched_skills=scores["matched_skills"],
        missing_skills=scores["missing_skills"],
        status="done",
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)

    # Add these for the response (not stored in DB)
    analysis.resume_skills = scores["resume_skills"]
    analysis.jd_skills = scores["jd_skills"]

    return analysis


@router.get("/history", response_model=list[AnalysisOut])
async def analysis_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(AnalysisResult)
        .where(AnalysisResult.user_id == current_user.id)
        .order_by(AnalysisResult.created_at.desc())
    )
    return result.scalars().all()