# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.routers import auth, resume
from app.routers import auth, resume, analysis

app = FastAPI(
    title="PlacementIQ API",
    description="AI-powered placement intelligence platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(analysis.router)

@app.get("/")
async def root():
    return {"message": "PlacementIQ API is running", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}