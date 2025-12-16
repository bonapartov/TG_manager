from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.channel import Channel
from app.schemas.channel import Channel as ChannelSchema, ChannelCreate, ChannelUpdate, ChannelList, ChannelCheck
from app.services.channel_service import ChannelService
from app.services.user_service import UserService
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=ChannelList)
async def get_channels(
    skip: int = Query(0, ge=0),
    limit: int = Query(25, ge=1, le=100),
    is_active: Optional[bool] = Query(None),
    is_private: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Get list of channels."""
    channel_service = ChannelService(db)
    channels = await channel_service.get_channels(
        skip=skip,
        limit=limit,
        is_active=is_active,
        is_private=is_private
    )
    
    total = await channel_service.get_channels_count(is_active, is_private)
    
    return ChannelList(
        items=channels,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.post("/", response_model=ChannelSchema)
async def create_channel(
    channel_data: ChannelCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Create new channel."""
    channel_service = ChannelService(db)
    channel = await channel_service.create_channel(channel_data, current_user)
    return channel


@router.get("/{channel_id}", response_model=ChannelSchema)
async def get_channel(
    channel_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Get channel by ID."""
    channel_service = ChannelService(db)
    channel = await channel_service.get_channel(channel_id)
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    return channel


@router.put("/{channel_id}", response_model=ChannelSchema)
async def update_channel(
    channel_id: int,
    channel_data: ChannelUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Update channel."""
    channel_service = ChannelService(db)
    channel = await channel_service.update_channel(channel_id, channel_data, current_user)
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    return channel


@router.delete("/{channel_id}")
async def delete_channel(
    channel_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Delete channel."""
    channel_service = ChannelService(db)
    success = await channel_service.delete_channel(channel_id, current_user)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    return {"message": "Channel deleted successfully"}


@router.post("/{channel_id}/check_access")
async def check_channel_access(
    channel_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Check channel access permissions."""
    channel_service = ChannelService(db)
    result = await channel_service.check_channel_access(channel_id)
    
    return ChannelCheck(
        channel_id=channel_id,
        has_access=result["has_access"],
        error_message=result.get("error_message")
    )


@router.get("/{channel_id}/posts")
async def get_channel_posts(
    channel_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(25, ge=1, le=100),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Get posts for specific channel."""
    channel_service = ChannelService(db)
    posts = await channel_service.get_channel_posts(
        channel_id=channel_id,
        skip=skip,
        limit=limit,
        status=status
    )
    
    return posts


@router.get("/{channel_id}/stats")
async def get_channel_stats(
    channel_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Get channel statistics."""
    channel_service = ChannelService(db)
    stats = await channel_service.get_channel_stats(channel_id)
    
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found"
        )
    
    return stats