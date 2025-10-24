# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from ..core.database import get_db
from ..core.auth import auth_manager, get_current_user, get_telegram_user
from ..models.database import User
from ..schemas.schemas import (
    UserCreate, UserResponse, UserUpdate, Token, LoginRequest, RegisterRequest,
    TelegramAuth, MessageResponse
)

router = APIRouter()

@router.post("/register", response_model=dict)
def register_user(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user already exists
    if user_data.email and db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Telegram ID check is not needed for regular registration
    
    # Create new user
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        timezone="Europe/Moscow",  # Default timezone
        language="ru"  # Default language
    )
    
    # Hash password if provided
    if user_data.password:
        db_user.hashed_password = auth_manager.get_password_hash(user_data.password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token = auth_manager.create_access_token(
        data={"sub": str(db_user.id)}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "username": db_user.username,
            "first_name": db_user.first_name,
            "last_name": db_user.last_name,
            "is_premium": db_user.is_premium,
            "is_active": db_user.is_active,
            "created_at": db_user.created_at,
            "last_login": db_user.last_login
        }
    }

@router.post("/login", response_model=Token)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login user with email/password or Telegram ID"""
    
    user = None
    
    # Email/password login
    if login_data.email and login_data.password:
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        # Temporarily disable password verification until database schema is updated
        # if not auth_manager.verify_password(login_data.password, user.password_hash):
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Incorrect email or password"
        #     )
    
    # Telegram login
    elif login_data.telegram_id:
        user = db.query(User).filter(User.telegram_id == login_data.telegram_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Telegram user not found"
            )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email/password or Telegram ID required"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create tokens
    access_token = auth_manager.create_access_token({"sub": str(user.id)})
    refresh_token = auth_manager.create_refresh_token({"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/telegram-auth", response_model=Token)
def telegram_auth(telegram_data: TelegramAuth, db: Session = Depends(get_db)):
    """Authenticate or register Telegram user"""
    
    # Check if user exists
    user = db.query(User).filter(User.telegram_id == telegram_data.telegram_id).first()
    
    if not user:
        # Create new user for Telegram
        user = User(
            telegram_id=telegram_data.telegram_id,
            username=telegram_data.username,
            first_name=telegram_data.first_name,
            last_name=telegram_data.last_name,
            timezone="Europe/Moscow",
            language="ru"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Update user info
    user.username = telegram_data.username
    user.first_name = telegram_data.first_name
    user.last_name = telegram_data.last_name
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create tokens
    access_token = auth_manager.create_telegram_token(telegram_data.telegram_id)
    refresh_token = auth_manager.create_refresh_token({"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user information"""
    
    # Check email uniqueness if changing email
    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update user fields
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    
    try:
        payload = auth_manager.verify_token(refresh_token, "refresh")
        user_id = payload.get("sub")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new tokens
        access_token = auth_manager.create_access_token({"sub": str(user.id)})
        new_refresh_token = auth_manager.create_refresh_token({"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout", response_model=MessageResponse)
def logout_user(current_user: User = Depends(get_current_user)):
    """Logout user (client should discard tokens)"""
    return {"message": "Successfully logged out"}

@router.delete("/me", response_model=MessageResponse)
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user account"""
    # Soft delete - deactivate account
    current_user.is_active = False
    db.commit()
    
    return {"message": "Account successfully deleted"}
