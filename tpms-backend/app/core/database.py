from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create sync engine for migrations and admin operations
sync_engine = create_engine(
    settings.DATABASE_URL_SYNC,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error("Database session error", error=str(e))
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))
        raise