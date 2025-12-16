from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ScheduleEntry(Base):
    """Schedule entry model for Celery tasks."""
    
    __tablename__ = "schedule_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, unique=True)
    celery_task_id = Column(String(255), nullable=False, unique=True)
    scheduled_for = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    post = relationship("Post", back_populates="schedule_entry")
    
    def __repr__(self):
        return f"<ScheduleEntry(id={self.id}, post_id={self.post_id}, celery_task_id={self.celery_task_id})>"