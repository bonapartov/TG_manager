from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.post import Post, PostStatus, ParseMode
from app.schemas.post import Post as PostSchema, PostCreate, PostUpdate, PostList, PostAction, PostFilter
from app.services.post_service import PostService
from app.services.user_service import UserService
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=PostList)
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(25, ge=1, le=100),
    channel_id: Optional[int] = Query(None),
    status: Optional[PostStatus] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    created_by: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Get list of posts with filtering and pagination."""
    post_service = PostService(db)
    
    # Create filter object
    filter_obj = PostFilter(
        channel_id=channel_id,
        status=status,
        date_from=date_from,
        date_to=date_to,
        created_by=created_by,
        search=search
    )
    
    posts = await post_service.get_posts(
        skip=skip,
        limit=limit,
        filter_obj=filter_obj,
        current_user=current_user
    )
    
    total = await post_service.get_posts_count(filter_obj, current_user)
    
    return PostList(
        items=posts,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.post("/", response_model=PostSchema)
async def create_post(
    post_data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Create new post."""
    post_service = PostService(db)
    post = await post_service.create_post(post_data, current_user)
    return post


@router.get("/{post_id}", response_model=PostSchema)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Get post by ID."""
    post_service = PostService(db)
    post = await post_service.get_post(post_id, current_user)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return post


@router.put("/{post_id}", response_model=PostSchema)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Update post."""
    post_service = PostService(db)
    post = await post_service.update_post(post_id, post_data, current_user)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return post


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Delete post."""
    post_service = PostService(db)
    success = await post_service.delete_post(post_id, current_user)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return {"message": "Post deleted successfully"}


@router.post("/{post_id}/publish_now")
async def publish_post_now(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Publish post immediately."""
    post_service = PostService(db)
    result = await post_service.publish_post_now(post_id, current_user)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot publish post"
        )
    
    return {"message": "Post published successfully"}


@router.post("/{post_id}/cancel")
async def cancel_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Cancel scheduled post."""
    post_service = PostService(db)
    result = await post_service.cancel_post(post_id, current_user)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel post"
        )
    
    return {"message": "Post cancelled successfully"}


@router.post("/{post_id}/retry")
async def retry_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Retry failed post."""
    post_service = PostService(db)
    result = await post_service.retry_post(post_id, current_user)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot retry post"
        )
    
    return {"message": "Post retry initiated"}


@router.post("/{post_id}/upload")
async def upload_media(
    post_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Upload media file for post."""
    post_service = PostService(db)
    result = await post_service.upload_media(post_id, file, current_user)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to upload media"
        )
    
    return {"message": "Media uploaded successfully", "file_path": result}


@router.get("/stats/dashboard")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Get dashboard statistics."""
    post_service = PostService(db)
    stats = await post_service.get_dashboard_stats(current_user)
    return stats


@router.get("/stats/publications")
async def get_publication_stats(
    days: int = Query(7, ge=1, le=30),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(UserService.get_current_active_user)
):
    """Get publication statistics for specified number of days."""
    post_service = PostService(db)
    stats = await post_service.get_publication_stats(days, current_user)
    return stats