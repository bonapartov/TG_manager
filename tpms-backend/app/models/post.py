from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum

from app.core.database import Base


class PostStatus(enum.Enum):
    """Post statuses."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ERROR = "error"
    CANCELLED = "cancelled"


class ParseMode(enum.Enum):
    """Parse modes for Telegram messages."""
    MARKDOWN = "Markdown"
    HTML = "HTML"


class Post(Base):
    """Post model."""
    
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    content = Column(Text, nullable=False)
    parse_mode = Column(Enum(ParseMode), default=ParseMode.MARKDOWN, nullable=False)
    media = Column(JSONB, nullable=True)  # [{"type": "photo", "file_path": "", "caption": ""}, ...]
    buttons = Column(JSONB, nullable=True)  # [[{"text": "", "url": ""}, ...], ...]
    status = Column(Enum(PostStatus), default=PostStatus.DRAFT, nullable=False)
    publish_at = Column(DateTime(timezone=True), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    published_msg_id = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Settings flags
    disable_notification = Column(Boolean, default=False, nullable=False)
    protect_content = Column(Boolean, default=False, nullable=False)
    has_spoiler = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    channel = relationship("Channel", back_populates="posts")
    created_by_user = relationship("User", back_populates="created_posts", foreign_keys=[created_by])
    history = relationship("PostHistory", back_populates="post", order_by="desc(PostHistory.changed_at)")
    schedule_entry = relationship("ScheduleEntry", back_populates="post", uselist=False)
    
    def __repr__(self):
        return f"<Post(id={self.id}, channel_id={self.channel_id}, status={self.status.value})>"
    
    @property
    def is_scheduled(self) -> bool:
        """Check if post is scheduled."""
        return self.status == PostStatus.SCHEDULED
    
    @property
    def can_be_published(self) -> bool:
        """Check if post can be published."""
        return self.status in [PostStatus.DRAFT, PostStatus.SCHEDULED]
    
    @property
    def media_count(self) -> int:
        """Get number of media files."""
        return len(self.media) if self.media else 0


class PostHistory(Base):
    """Post history model for version control."""
    
    __tablename__ = "posts_history"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    diff = Column(JSONB, nullable=False)  # {"content": {"old": "", "new": ""}, ...}
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    action = Column(String(50), nullable=False)  # created, updated, published, deleted
    
    # Relationships
    post = relationship("Post", back_populates="history")
    changed_by_user = relationship("User", back_populates="post_histories", foreign_keys=[changed_by])
    
    def __repr__(self):
        return f"<PostHistory(id={self.id}, post_id={self.post_id}, action={self.action})>"