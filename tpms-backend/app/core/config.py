import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, RedisDsn


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    PROJECT_NAME: str = "TPMS - Telegram Publishing Management System"
    VERSION: str = "1.3.0"
    DESCRIPTION: str = "Professional system for managing Telegram channel publications"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # API
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: Optional[PostgresDsn] = os.getenv("DATABASE_URL")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "tpms")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "tpms_password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tpms_db")
    
    # Redis
    REDIS_URL: Optional[RedisDsn] = os.getenv("REDIS_URL")
    REDIS_SERVER: str = os.getenv("REDIS_SERVER", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    # Celery
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_API_ID: Optional[str] = os.getenv("TELEGRAM_API_ID")
    TELEGRAM_API_HASH: Optional[str] = os.getenv("TELEGRAM_API_HASH")
    
    # Security
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Encryption
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "your-encryption-key-32-chars!!")
    
    # File uploads
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "52428800"))  # 50MB
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 25
    MAX_PAGE_SIZE: int = 100
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "300"))
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = os.getenv("PROMETHEUS_ENABLED", "true").lower() == "true"
    
    @property
    def DATABASE_URL_ASYNC(self) -> str:
        """Get async database URL."""
        if self.DATABASE_URL:
            return str(self.DATABASE_URL).replace("postgresql://", "postgresql+asyncpg://")
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    
    @property
    def DATABASE_URL_SYNC(self) -> str:
        """Get sync database URL."""
        if self.DATABASE_URL:
            return str(self.DATABASE_URL)
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()