from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: UserRole = UserRole.EDITOR
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating users."""
    telegram_id: Optional[int] = None
    password: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating users."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """Schema for user in database."""
    id: int
    telegram_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class User(UserInDB):
    """Schema for user response."""
    pass


class UserLogin(BaseModel):
    """Schema for user login."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    telegram_hash: Optional[str] = None


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Schema for token data."""
    user_id: Optional[int] = None
    username: Optional[str] = None