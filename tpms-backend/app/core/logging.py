import structlog
import logging
import sys
from typing import Any, Dict


def setup_logging():
    """Setup structured logging."""
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get logger instance."""
    return structlog.get_logger(name)


class LoggerMixin:
    """Mixin to add logging capabilities to classes."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = get_logger(self.__class__.__module__ + "." + self.__class__.__name__)


def log_api_call(
    method: str,
    path: str,
    status_code: int,
    duration: float,
    user_id: int = None,
    **kwargs: Any
) -> None:
    """Log API call details."""
    logger = get_logger("api")
    logger.info(
        "API call",
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=round(duration * 1000, 2),
        user_id=user_id,
        **kwargs
    )


def log_telegram_api_call(
    method: str,
    chat_id: str,
    success: bool,
    duration: float,
    error: str = None,
    **kwargs: Any
) -> None:
    """Log Telegram API call details."""
    logger = get_logger("telegram")
    log_data = {
        "method": method,
        "chat_id": chat_id,
        "success": success,
        "duration_ms": round(duration * 1000, 2),
        **kwargs
    }
    
    if error:
        log_data["error"] = error
        logger.error("Telegram API call", **log_data)
    else:
        logger.info("Telegram API call", **log_data)