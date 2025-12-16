from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.models.post import PostStatus, ParseMode


class MediaItem(BaseModel):
    """Schema for media item."""
    type: str  # "photo", "video", "document"
    file_path: str
    caption: Optional[str] = None


class ButtonItem(BaseModel):
    """Schema for button item."""
    text: str
    url: str


class PostBase(BaseModel):
    """Base post schema."""
    channel_id: int
    content: str
    parse_mode: ParseMode = ParseMode.MARKDOWN
    media: Optional[List[MediaItem]] = None
    buttons: Optional[List[List[ButtonItem]]] = None
    status: PostStatus = PostStatus.DRAFT
    publish_at: Optional[datetime] = None
    disable_notification: bool = False
    protect_content: bool = False
    has_spoiler: bool = False


class PostCreate(PostBase):
    """Schema for creating posts."""
    pass


class PostUpdate(BaseModel):
    """Schema for updating posts."""
    content: Optional[str] = None
    parse_mode: Optional[ParseMode] = None
    media: Optional[List[MediaItem]] = None
    buttons: Optional[List[List[ButtonItem]]] = None
    status: Optional[PostStatus] = None
    publish_at: Optional[datetime] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    has_spoiler: Optional[bool] = None


class PostInDB(PostBase):
    """Schema for post in database."""
    id: int
    published_at: Optional[datetime] = None
    published_msg_id: Optional[int] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class Post(PostInDB):
    """Schema for post response."""
    channel_title: Optional[str] = None
    created_by_username: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class PostList(BaseModel):
    """Schema for post list response."""
    items: List[Post]
    total: int
    page: int
    size: int


class PostHistory(BaseModel):
    """Schema for post history."""
    id: int
    post_id: int
    diff: Dict[str, Any]
    changed_by: int
    changed_at: datetime
    action: str
    changed_by_username: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class PostAction(BaseModel):
    """Schema for post actions."""
    action: str  # "publish_now", "cancel", "retry"
    reason: Optional[str] = None


class PostFilter(BaseModel):
    """Schema for post filtering."""
    channel_id: Optional[int] = None
    status: Optional[PostStatus] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    created_by: Optional[int] = None
    search: Optional[str] = None