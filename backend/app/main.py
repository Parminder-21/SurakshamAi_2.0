"""
Suraksham AI — FastAPI Backend
Entry point for the multi-agent fraud detection API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routers import analyze, news, report

app = FastAPI(
    title="Suraksham AI API",
    description="AI-powered Cyber Safety & Fraud Detection for India",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(analyze.router)
app.include_router(news.router)
app.include_router(report.router)


# ── Health Check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": "Suraksham AI API",
        "version": "1.0.0",
        "llm_provider": settings.llm_provider,
    }


@app.get("/", tags=["System"])
async def root():
    return {
        "message": "🛡️ Suraksham AI API",
        "docs": "/docs",
        "health": "/health",
    }


# ── Exception Handlers ────────────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )
