from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import structlog

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import engine, Base
from app.core.logging import setup_logging
from app.core.celery import celery_app

# Setup logging
setup_logging()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting TPMS application")
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database tables created")
    yield
    
    logger.info("Shutting down TPMS application")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to TPMS - Telegram Publishing Management System",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": "2025-06-17T10:00:00Z"}


@app.get("/health/db")
async def db_health_check():
    """Database health check endpoint."""
    try:
        from app.core.database import AsyncSessionLocal
        from sqlalchemy import text
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@app.get("/health/celery")
async def celery_health_check():
    """Celery health check endpoint."""
    try:
        # Check if Celery workers are available
        result = celery_app.control.inspect()
        if result.active() is not None:
            return {"status": "healthy", "celery": "connected"}
        else:
            return {"status": "unhealthy", "celery": "no_workers"}
    except Exception as e:
        return {"status": "unhealthy", "celery": "disconnected", "error": str(e)}