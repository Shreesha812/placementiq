# app/routers/resume.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.schemas.resume import ResumeOut
from app.services.storage_service import upload_file
from app.services.resume_parser import extract_text, parse_sections

router = APIRouter(prefix="/resumes", tags=["Resumes"])

ALLOWED_TYPES = ["application/pdf"]
MAX_SIZE_MB = 5


@router.post("/upload", response_model=ResumeOut, status_code=201)
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed",
        )

    # Read file bytes
    file_bytes = await file.read()

    # Validate file size
    if len(file_bytes) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds {MAX_SIZE_MB}MB limit",
        )

    # Generate unique S3 key
    s3_key = f"resumes/{current_user.id}/{uuid.uuid4()}.pdf"

    # Upload to S3/MinIO
    upload_file(file_bytes, s3_key)

    # Extract text from PDF
    raw_text = extract_text(file_bytes)

    # Parse sections into structured JSON
    parsed_json = parse_sections(raw_text)

    # Save to database
    resume = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        s3_key=s3_key,
        raw_text=raw_text,
        parsed_json=parsed_json,
        parse_status="done",
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)

    return resume


@router.get("/", response_model=list[ResumeOut])
async def list_resumes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select
    result = await db.execute(
        select(Resume)
        .where(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
    )
    return result.scalars().all()