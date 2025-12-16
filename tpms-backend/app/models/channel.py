from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Channel(Base):
    """Channel model."""
    
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, nullable=True, index=True)
    chat_id = Column(String(100), unique=True, nullable=False, index=True)  # '-100...' for private channels
    invite_link = Column(Text, nullable=True)
    is_private = Column(Boolean, default=False, nullable=False)
    bot_token_enc = Column(Text, nullable=False)  # Encrypted bot token
    added_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_checked = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    added_by_user = relationship("User", back_populates="channels", foreign_keys=[added_by])
    posts = relationship("Post", back_populates="channel")
    
    def __repr__(self):
        return f"<Channel(id={self.id}, title={self.title}, username={self.username})>"
    
    @property
    def display_name(self) -> str:
        """Get display name for channel."""
        if self.username:
            return f"@{self.username}"
        return self.title
    
    @property
    def telegram_link(self) -> str:
        """Get Telegram link for channel."""
        if self.username:
            return f"https://t.me/{self.username}"
        elif self.invite_link:
            return self.invite_link
        return None