from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """Verify JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != token_type:
            return None
        return payload
    except JWTError:
        return None


# Password functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password."""
    return pwd_context.hash(password)


# Encryption functions for sensitive data
class EncryptionService:
    """Service for encrypting/decrypting sensitive data."""
    
    def __init__(self, key: str):
        """Initialize encryption service with key."""
        # Ensure key is 32 bytes for Fernet
        key_bytes = key.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'tpms_salt_2025',  # In production, use random salt
            iterations=100000,
            backend=default_backend()
        )
        key_derived = base64.urlsafe_b64encode(kdf.derive(key_bytes))
        self.cipher = Fernet(key_derived)
    
    def encrypt(self, data: str) -> str:
        """Encrypt data."""
        return self.cipher.encrypt(data.encode('utf-8')).decode('utf-8')
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data."""
        return self.cipher.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')


# Initialize encryption service
encryption_service = EncryptionService(settings.ENCRYPTION_KEY)


def encrypt_sensitive_data(data: str) -> str:
    """Encrypt sensitive data like bot tokens."""
    return encryption_service.encrypt(data)


def decrypt_sensitive_data(encrypted_data: str) -> str:
    """Decrypt sensitive data."""
    return encryption_service.decrypt(encrypted_data)


# Telegram login widget verification
def verify_telegram_login(hash_str: str, data: dict, bot_token: str) -> bool:
    """Verify Telegram login widget data."""
    try:
        from telegram import LoginWidget
        widget = LoginWidget(bot_token)
        return widget.verify_login_data(hash_str, data)
    except Exception:
        return False


# CSRF token functions
def generate_csrf_token(user_id: int) -> str:
    """Generate CSRF token."""
    data = {
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "csrf": True
    }
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_csrf_token(token: str, user_id: int) -> bool:
    """Verify CSRF token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("user_id") == user_id and payload.get("csrf") is True
    except JWTError:
        return False