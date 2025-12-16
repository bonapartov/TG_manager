from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_, or_
from fastapi import HTTPException, status

from app.models.channel import Channel
from app.models.post import Post, PostStatus
from app.models.user import User
from app.schemas.channel import ChannelCreate, ChannelUpdate
from app.core.security import encrypt_sensitive_data, decrypt_sensitive_data
from app.services.telegram_service import telegram_service
from app.core.logging import get_logger

logger = get_logger(__name__)


class ChannelService:
    """Service for channel management."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_channel(self, channel_data: ChannelCreate, current_user) -> Channel:
        """Create new channel."""
        # Check if channel with same username or chat_id already exists
        existing = await self.db.execute(
            select(Channel).where(
                or_(
                    Channel.username == channel_data.username,
                    Channel.chat_id == channel_data.chat_id
                )
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Channel with this username or chat_id already exists"
            )
        
        # Encrypt bot token
        bot_token_enc = encrypt_sensitive_data(channel_data.bot_token)
        
        # Create channel
        channel = Channel(
            title=channel_data.title,
            username=channel_data.username,
            chat_id=channel_data.chat_id,
            invite_link=channel_data.invite_link,
            is_private=channel_data.is_private,
            bot_token_enc=bot_token_enc,
            added_by=current_user.id,
            is_active=channel_data.is_active
        )
        
        self.db.add(channel)
        await self.db.commit()
        await self.db.refresh(channel)
        
        # Check access after creation
        try:
            await telegram_service.check_channel_access(channel)
            channel.last_checked = datetime.utcnow()
            await self.db.commit()
        except Exception as e:
            logger.warning("Failed to check channel access", channel_id=channel.id, error=str(e))
        
        return channel
    
    async def get_channel(self, channel_id: int) -> Optional[Channel]:
        """Get channel by ID."""
        return await self.db.get(Channel, channel_id)
    
    async def get_channels(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        is_private: Optional[bool] = None
    ) -> List[Channel]:
        """Get list of channels with filtering."""
        query = select(Channel)
        
        conditions = []
        if is_active is not None:
            conditions.append(Channel.is_active == is_active)
        if is_private is not None:
            conditions.append(Channel.is_private == is_private)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.offset(skip).limit(limit).order_by(Channel.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_channels_count(
        self,
        is_active: Optional[bool] = None,
        is_private: Optional[bool] = None
    ) -> int:
        """Get total count of channels."""
        query = select(func.count(Channel.id))
        
        conditions = []
        if is_active is not None:
            conditions.append(Channel.is_active == is_active)
        if is_private is not None:
            conditions.append(Channel.is_private == is_private)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        result = await self.db.execute(query)
        return result.scalar_one()
    
    async def update_channel(
        self,
        channel_id: int,
        channel_data: ChannelUpdate,
        current_user
    ) -> Optional[Channel]:
        """Update channel."""
        channel = await self.get_channel(channel_id)
        if not channel:
            return None
        
        # Update fields
        update_data = channel_data.model_dump(exclude_unset=True)
        
        if "bot_token" in update_data:
            # Encrypt new bot token
            update_data["bot_token_enc"] = encrypt_sensitive_data(update_data.pop("bot_token"))
        
        for field, value in update_data.items():
            setattr(channel, field, value)
        
        await self.db.commit()
        await self.db.refresh(channel)
        
        return channel
    
    async def delete_channel(self, channel_id: int, current_user) -> bool:
        """Delete channel."""
        channel = await self.get_channel(channel_id)
        if not channel:
            return False
        
        # Check if channel has published posts
        posts_count = await self.db.execute(
            select(func.count(Post.id)).where(
                and_(
                    Post.channel_id == channel_id,
                    Post.status == PostStatus.PUBLISHED
                )
            )
        )
        if posts_count.scalar_one() > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete channel with published posts"
            )
        
        await self.db.delete(channel)
        await self.db.commit()
        
        return True
    
    async def check_channel_access(self, channel_id: int) -> Dict[str, Any]:
        """Check channel access permissions."""
        channel = await self.get_channel(channel_id)
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found"
            )
        
        try:
            has_access = await telegram_service.check_channel_access(channel)
            channel.last_checked = datetime.utcnow()
            await self.db.commit()
            
            return {
                "has_access": has_access,
                "error_message": None
            }
        except Exception as e:
            logger.error("Channel access check failed", channel_id=channel_id, error=str(e))
            return {
                "has_access": False,
                "error_message": str(e)
            }
    
    async def get_channel_posts(
        self,
        channel_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Post]:
        """Get posts for specific channel."""
        query = select(Post).where(Post.channel_id == channel_id)
        
        if status:
            try:
                post_status = PostStatus(status)
                query = query.where(Post.status == post_status)
            except ValueError:
                pass
        
        query = query.offset(skip).limit(limit).order_by(Post.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_channel_stats(self, channel_id: int) -> Optional[Dict[str, Any]]:
        """Get channel statistics."""
        channel = await self.get_channel(channel_id)
        if not channel:
            return None
        
        # Get post counts by status
        stats_query = select(
            Post.status,
            func.count(Post.id).label("count")
        ).where(
            Post.channel_id == channel_id
        ).group_by(Post.status)
        
        result = await self.db.execute(stats_query)
        status_counts = {row.status.value: row.count for row in result}
        
        # Get total posts
        total_query = select(func.count(Post.id)).where(Post.channel_id == channel_id)
        total_result = await self.db.execute(total_query)
        total_posts = total_result.scalar_one()
        
        # Get published posts count
        published_count = status_counts.get(PostStatus.PUBLISHED.value, 0)
        
        # Get scheduled posts count
        scheduled_count = status_counts.get(PostStatus.SCHEDULED.value, 0)
        
        # Get error posts count
        error_count = status_counts.get(PostStatus.ERROR.value, 0)
        
        return {
            "channel_id": channel_id,
            "channel_title": channel.title,
            "total_posts": total_posts,
            "published": published_count,
            "scheduled": scheduled_count,
            "draft": status_counts.get(PostStatus.DRAFT.value, 0),
            "error": error_count,
            "cancelled": status_counts.get(PostStatus.CANCELLED.value, 0),
            "last_checked": channel.last_checked.isoformat() if channel.last_checked else None
        }



