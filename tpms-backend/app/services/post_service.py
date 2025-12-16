from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import os
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_
from fastapi import UploadFile, HTTPException, status

from app.models.post import Post, PostStatus, PostHistory, ParseMode
from app.models.channel import Channel
from app.schemas.post import PostCreate, PostUpdate, PostFilter, MediaItem, ButtonItem
from app.services.telegram_service import telegram_service
from app.core.logging import get_logger

logger = get_logger(__name__)


class PostService:
    """Service for post management."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_post(self, post_data: PostCreate, current_user) -> Post:
        """Create new post."""
        # Check if channel exists and user has access
        channel = await self.db.get(Channel, post_data.channel_id)
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found"
            )
        
        # Create post
        post = Post(
            channel_id=post_data.channel_id,
            content=post_data.content,
            parse_mode=post_data.parse_mode,
            media=[item.model_dump() for item in post_data.media] if post_data.media else None,
            buttons=[[btn.model_dump() for btn in row] for row in post_data.buttons] if post_data.buttons else None,
            status=post_data.status,
            publish_at=post_data.publish_at,
            created_by=current_user.id,
            disable_notification=post_data.disable_notification,
            protect_content=post_data.protect_content,
            has_spoiler=post_data.has_spoiler
        )
        
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        
        # Create history entry
        await self._create_history_entry(post, current_user.id, "created")
        
        logger.info(
            "Post created",
            post_id=post.id,
            channel_id=post.channel_id,
            user_id=current_user.id
        )
        
        return post
    
    async def get_posts(
        self,
        skip: int,
        limit: int,
        filter_obj: PostFilter,
        current_user
    ) -> List[Post]:
        """Get posts with filtering and pagination."""
        query = select(Post).join(Channel).where(Channel.is_active == True)
        
        # Apply filters
        if filter_obj.channel_id:
            query = query.where(Post.channel_id == filter_obj.channel_id)
        
        if filter_obj.status:
            query = query.where(Post.status == filter_obj.status)
        
        if filter_obj.date_from:
            query = query.where(Post.created_at >= filter_obj.date_from)
        
        if filter_obj.date_to:
            query = query.where(Post.created_at <= filter_obj.date_to)
        
        if filter_obj.created_by:
            query = query.where(Post.created_by == filter_obj.created_by)
        elif not current_user.is_admin:
            # Non-admin users can only see their own posts or published posts
            query = query.where(
                (Post.created_by == current_user.id) | (Post.status == PostStatus.PUBLISHED)
            )
        
        if filter_obj.search:
            search_term = f"%{filter_obj.search}%"
            query = query.where(Post.content.ilike(search_term))
        
        # Order by creation date descending
        query = query.order_by(Post.created_at.desc())
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_posts_count(self, filter_obj: PostFilter, current_user) -> int:
        """Get total count of posts."""
        query = select(func.count(Post.id)).join(Channel).where(Channel.is_active == True)
        
        # Apply same filters as in get_posts
        if filter_obj.channel_id:
            query = query.where(Post.channel_id == filter_obj.channel_id)
        
        if filter_obj.status:
            query = query.where(Post.status == filter_obj.status)
        
        if filter_obj.date_from:
            query = query.where(Post.created_at >= filter_obj.date_from)
        
        if filter_obj.date_to:
            query = query.where(Post.created_at <= filter_obj.date_to)
        
        if filter_obj.created_by:
            query = query.where(Post.created_by == filter_obj.created_by)
        elif not current_user.is_admin:
            query = query.where(
                (Post.created_by == current_user.id) | (Post.status == PostStatus.PUBLISHED)
            )
        
        if filter_obj.search:
            search_term = f"%{filter_obj.search}%"
            query = query.where(Post.content.ilike(search_term))
        
        result = await self.db.execute(query)
        return result.scalar()
    
    async def get_post(self, post_id: int, current_user) -> Optional[Post]:
        """Get post by ID."""
        query = select(Post).where(Post.id == post_id)
        
        # Check access permissions
        if not current_user.is_admin:
            query = query.join(Channel).where(
                (Post.created_by == current_user.id) | (Post.status == PostStatus.PUBLISHED),
                Channel.is_active == True
            )
        
        result = await self.db.execute(query)
        post = result.scalar_one_or_none()
        
        if not post:
            return None
        
        # Load relationships
        await self.db.refresh(post, ['channel', 'created_by_user'])
        
        return post
    
    async def update_post(
        self,
        post_id: int,
        post_data: PostUpdate,
        current_user
    ) -> Optional[Post]:
        """Update post."""
        post = await self.get_post(post_id, current_user)
        if not post:
            return None
        
        # Check if post can be edited
        if post.status == PostStatus.PUBLISHED and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot edit published post"
            )
        
        # Store old values for history
        old_values = {
            "content": post.content,
            "parse_mode": post.parse_mode,
            "media": post.media,
            "buttons": post.buttons,
            "publish_at": post.publish_at,
            "disable_notification": post.disable_notification,
            "protect_content": post.protect_content,
            "has_spoiler": post.has_spoiler
        }
        
        # Update fields
        update_data = post_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if field == "media" and value:
                post.media = [item.model_dump() for item in value]
            elif field == "buttons" and value:
                post.buttons = [[btn.model_dump() for btn in row] for row in value]
            else:
                setattr(post, field, value)
        
        await self.db.commit()
        await self.db.refresh(post)
        
        # Create history entry
        await self._create_history_entry(post, current_user.id, "updated", old_values)
        
        logger.info(
            "Post updated",
            post_id=post.id,
            user_id=current_user.id
        )
        
        return post
    
    async def delete_post(self, post_id: int, current_user) -> bool:
        """Delete post."""
        post = await self.get_post(post_id, current_user)
        if not post:
            return False
        
        # Check permissions
        if not current_user.is_admin and post.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # Check if post is published
        if post.status == PostStatus.PUBLISHED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete published post"
            )
        
        await self.db.delete(post)
        await self.db.commit()
        
        logger.info(
            "Post deleted",
            post_id=post_id,
            user_id=current_user.id
        )
        
        return True
    
    async def publish_post_now(self, post_id: int, current_user) -> bool:
        """Publish post immediately."""
        post = await self.get_post(post_id, current_user)
        if not post:
            return False
        
        # Check if post can be published
        if not post.can_be_published:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Post cannot be published"
            )
        
        # Get channel
        channel = await self.db.get(Channel, post.channel_id)
        if not channel or not channel.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Channel not available"
            )
        
        # Publish to Telegram
        success = await telegram_service.publish_post(post, channel)
        
        if success:
            await self.db.commit()
            
            # Create history entry
            await self._create_history_entry(post, current_user.id, "published")
            
            logger.info(
                "Post published immediately",
                post_id=post.id,
                user_id=current_user.id
            )
        
        return success
    
    async def cancel_post(self, post_id: int, current_user) -> bool:
        """Cancel scheduled post."""
        post = await self.get_post(post_id, current_user)
        if not post:
            return False
        
        if post.status != PostStatus.SCHEDULED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Post is not scheduled"
            )
        
        post.status = PostStatus.CANCELLED
        post.publish_at = None
        
        await self.db.commit()
        
        # Create history entry
        await self._create_history_entry(post, current_user.id, "cancelled")
        
        logger.info(
            "Post cancelled",
            post_id=post.id,
            user_id=current_user.id
        )
        
        return True
    
    async def retry_post(self, post_id: int, current_user) -> bool:
        """Retry failed post."""
        post = await self.get_post(post_id, current_user)
        if not post:
            return False
        
        if post.status != PostStatus.ERROR:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Post is not in error state"
            )
        
        # Reset error state
        post.status = PostStatus.DRAFT
        post.error_message = None
        post.retry_count += 1
        
        await self.db.commit()
        
        logger.info(
            "Post retry initiated",
            post_id=post.id,
            user_id=current_user.id,
            retry_count=post.retry_count
        )
        
        return True
    
    async def upload_media(
        self,
        post_id: int,
        file: UploadFile,
        current_user
    ) -> Optional[str]:
        """Upload media file for post."""
        post = await self.get_post(post_id, current_user)
        if not post:
            return None
        
        # Check file size
        file_size = 0
        content = await file.read()
        file_size = len(content)
        
        # Check file type and size limits
        if file.content_type.startswith('image/'):
            max_size = 10 * 1024 * 1024  # 10MB
            if file_size > max_size:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Image file too large (max 10MB)"
                )
        elif file.content_type.startswith('video/'):
            max_size = 50 * 1024 * 1024  # 50MB
            if file_size > max_size:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Video file too large (max 50MB)"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type"
            )
        
        # Generate unique filename
        file_ext = file.filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(content)
        
        logger.info(
            "Media uploaded",
            post_id=post.id,
            user_id=current_user.id,
            file_path=file_path,
            file_size=file_size
        )
        
        return file_path
    
    async def get_dashboard_stats(self, current_user) -> Dict[str, Any]:
        """Get dashboard statistics."""
        # Base query
        query = select(func.count(Post.id)).join(Channel).where(Channel.is_active == True)
        
        if not current_user.is_admin:
            query = query.where(
                (Post.created_by == current_user.id) | (Post.status == PostStatus.PUBLISHED)
            )
        
        # Count by status
        stats = {}
        for status in PostStatus:
            status_query = query.where(Post.status == status)
            result = await self.db.execute(status_query)
            stats[status.value] = result.scalar()
        
        # Today's posts
        today = datetime.utcnow().date()
        today_query = query.where(
            func.date(Post.created_at) == today
        )
        result = await self.db.execute(today_query)
        stats['today_total'] = result.scalar()
        
        return stats
    
    async def get_publication_stats(self, days: int, current_user) -> List[Dict[str, Any]]:
        """Get publication statistics for specified number of days."""
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days - 1)
        
        # Query for daily publication counts
        query = select(
            func.date(Post.created_at).label('date'),
            func.count(Post.id).label('count'),
            Post.status
        ).join(Channel).where(
            Channel.is_active == True,
            func.date(Post.created_at) >= start_date,
            func.date(Post.created_at) <= end_date
        )
        
        if not current_user.is_admin:
            query = query.where(
                (Post.created_by == current_user.id) | (Post.status == PostStatus.PUBLISHED)
            )
        
        query = query.group_by(
            func.date(Post.created_at),
            Post.status
        ).order_by(func.date(Post.created_at))
        
        result = await self.db.execute(query)
        rows = result.fetchall()
        
        # Organize data by date
        stats = []
        current_date = start_date
        
        while current_date <= end_date:
            date_stats = {
                'date': current_date.isoformat(),
                'published': 0,
                'scheduled': 0,
                'draft': 0,
                'error': 0
            }
            
            for row in rows:
                if row.date == current_date:
                    if row.status == PostStatus.PUBLISHED:
                        date_stats['published'] = row.count
                    elif row.status == PostStatus.SCHEDULED:
                        date_stats['scheduled'] = row.count
                    elif row.status == PostStatus.DRAFT:
                        date_stats['draft'] = row.count
                    elif row.status == PostStatus.ERROR:
                        date_stats['error'] = row.count
            
            stats.append(date_stats)
            current_date += timedelta(days=1)
        
        return stats
    
    async def _create_history_entry(
        self,
        post: Post,
        user_id: int,
        action: str,
        old_values: Optional[Dict[str, Any]] = None
    ):
        """Create history entry for post."""
        diff = {}
        
        if old_values:
            for field, old_value in old_values.items():
                new_value = getattr(post, field)
                if old_value != new_value:
                    diff[field] = {"old": old_value, "new": new_value}
        
        history_entry = PostHistory(
            post_id=post.id,
            diff=diff,
            changed_by=user_id,
            action=action
        )
        
        self.db.add(history_entry)
        await self.db.commit()