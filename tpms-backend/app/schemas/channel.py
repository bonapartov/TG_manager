from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ChannelBase(BaseModel):
    """Base channel schema."""
    title: str
    username: Optional[str] = None
    chat_id: str
    invite_link: Optional[str] = None
    is_private: bool = False
    is_active: bool = True


class ChannelCreate(ChannelBase):
    """Schema for creating channels."""
    bot_token: str


class ChannelUpdate(BaseModel):
    """Schema for updating channels."""
    title: Optional[str] = None
    bot_token: Optional[str] = None
    is_active: Optional[bool] = None


class ChannelInDB(ChannelBase):
    """Schema for channel in database."""
    id: int
    added_by: int
    created_at: datetime
    updated_at: datetime
    last_checked: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class Channel(ChannelInDB):
    """Schema for channel response."""
    added_by_username: Optional[str] = None
    post_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)


class ChannelCheck(BaseModel):
    """Schema for checking channel access."""
    channel_id: int
    has_access: bool
    error_message: Optional[str] = None


class ChannelList(BaseModel):
    """Schema for channel list response."""
    items: List[Channel]
    total: int
    page: int
    size: int