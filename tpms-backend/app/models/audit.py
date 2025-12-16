from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum

from app.core.database import Base


class AuditAction(enum.Enum):
    """Audit log actions."""
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    PUBLISH = "publish"
    SCHEDULE = "schedule"
    CANCEL = "cancel"


class AuditObject(enum.Enum):
    """Audit log object types."""
    USER = "user"
    CHANNEL = "channel"
    POST = "post"
    SETTINGS = "settings"


class AuditLog(Base):
    """Audit log model."""
    
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(Enum(AuditAction), nullable=False)
    object_type = Column(Enum(AuditObject), nullable=False)
    object_id = Column(Integer, nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(Text, nullable=True)
    details = Column(JSONB, nullable=True)  # Additional details
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, user_id={self.user_id}, action={self.action.value}, object_type={self.object_type.value})>"