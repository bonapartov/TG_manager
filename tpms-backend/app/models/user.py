from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class UserRole(enum.Enum):
    """User roles."""
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    EDITOR = "editor"
    GUEST = "guest"


class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=True, index=True)
    username = Column(String(50), unique=True, nullable=True, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.EDITOR, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    created_posts = relationship("Post", back_populates="created_by_user", foreign_keys="Post.created_by")
    channels = relationship("Channel", back_populates="added_by_user", foreign_keys="Channel.added_by")
    audit_logs = relationship("AuditLog", back_populates="user")
    post_histories = relationship("PostHistory", back_populates="changed_by_user", foreign_keys="PostHistory.changed_by")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role.value})>"
    
    @property
    def is_superadmin(self) -> bool:
        """Check if user is superadmin."""
        return self.role == UserRole.SUPERADMIN
    
    @property
    def is_admin(self) -> bool:
        """Check if user is admin or superadmin."""
        return self.role in [UserRole.ADMIN, UserRole.SUPERADMIN]
    
    @property
    def is_editor(self) -> bool:
        """Check if user is editor or higher."""
        return self.role in [UserRole.EDITOR, UserRole.ADMIN, UserRole.SUPERADMIN]