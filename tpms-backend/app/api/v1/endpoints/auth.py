from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import Token, User as UserSchema, UserLogin
from app.services.user_service import UserService

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login with username/password."""
    user_service = UserService(db)
    
    # Try to authenticate user
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=access_token_expires
    )
    
    refresh_token = security.create_refresh_token(
        data={"sub": str(user.id), "username": user.username}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/login/telegram")
async def login_telegram(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login with Telegram widget."""
    if not login_data.telegram_hash:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Telegram hash required"
        )
    
    user_service = UserService(db)
    user = await user_service.authenticate_telegram(login_data.telegram_hash)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram login"
        )
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=access_token_expires
    )
    
    refresh_token = security.create_refresh_token(
        data={"sub": str(user.id), "username": user.username}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token."""
    # Verify refresh token
    payload = security.verify_token(refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = int(payload.get("sub"))
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=access_token_expires
    )
    
    # Create new refresh token
    new_refresh_token = security.create_refresh_token(
        data={"sub": str(user.id), "username": user.username}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.get("/me", response_model=UserSchema)
async def get_current_user(
    current_user: User = Depends(UserService.get_current_user)
):
    """Get current user information."""
    return current_user


@router.post("/logout")
async def logout(
    current_user: User = Depends(UserService.get_current_user)
):
    """Logout current user."""
    # In a real application, you might want to:
    # 1. Add token to blacklist
    # 2. Update user's last logout time
    # 3. Log the logout action
    
    return {"message": "Successfully logged out"}