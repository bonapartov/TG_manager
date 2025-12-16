from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core import security
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


class UserService:
    """Service for user management."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Create new user."""
        # Check if user already exists
        existing_user = await self.get_user_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        if user_data.email:
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
        
        # Hash password if provided
        password_hash = None
        if user_data.password:
            password_hash = security.get_password_hash(user_data.password)
        
        # Create user
        user = User(
            telegram_id=user_data.telegram_id,
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash,
            role=user_data.role
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID."""
        result = await self.db.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of users."""
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """Update user."""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields
        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def delete_user(self, user_id: int) -> None:
        """Delete user."""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        await self.db.delete(user)
        await self.db.commit()
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password."""
        user = await self.get_user_by_username(username)
        if not user:
            return None
        
        if not user.password_hash:
            return None
        
        if not security.verify_password(password, user.password_hash):
            return None
        
        return user
    
    async def authenticate_telegram(self, telegram_hash: str) -> Optional[User]:
        """Authenticate user with Telegram hash."""
        # In a real implementation, you would verify the Telegram hash
        # and extract user information from it
        # For now, we'll use a simplified version
        
        # This is a placeholder - implement actual Telegram hash verification
        # based on your bot token and the hash validation algorithm
        
        # For demo purposes, we'll assume the hash contains the user ID
        try:
            # Extract user ID from hash (simplified)
            user_id = int(telegram_hash.split(':')[0])
            user = await self.get_user_by_id(user_id)
            return user
        except (ValueError, IndexError):
            return None
    
    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        """Get current authenticated user."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        # Verify token
        payload = security.verify_token(token)
        if not payload:
            raise credentials_exception
        
        # Get user ID from token
        user_id = int(payload.get("sub"))
        
        # Get user from database
        user_service = UserService(db)
        user = await user_service.get_user_by_id(user_id)
        
        if user is None:
            raise credentials_exception
        
        return user
    
    @staticmethod
    async def get_current_active_user(
        current_user: User = Depends(get_current_user)
    ) -> User:
        """Get current active user."""
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return current_user