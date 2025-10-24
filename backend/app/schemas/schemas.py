# backend/app/schemas.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

# Enums
class FrequencyEnum(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class NotificationChannelEnum(str, Enum):
    TELEGRAM = "telegram"
    EMAIL = "email"
    PUSH = "push"

# User Schemas
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    timezone: str = "Europe/Moscow"
    language: str = "ru"

class UserCreate(UserBase):
    password: Optional[str] = None
    telegram_id: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_premium: bool
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

# Auth Schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def validate_password_length(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password too long (max 72 bytes)')
        if len(v) < 6:
            raise ValueError('Password too short (min 6 characters)')
        return v

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @validator('password')
    def validate_password_length(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password too long (max 72 bytes)')
        if len(v) < 6:
            raise ValueError('Password too short (min 6 characters)')
        return v

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Subscription Schemas
class SubscriptionBase(BaseModel):
    name: str
    description: Optional[str] = None
    amount: float
    currency: str = "RUB"
    
    # Тип подписки
    subscription_type: str = "recurring"  # recurring, one_time
    
    # Поля для recurring подписок
    next_billing_date: Optional[date] = None
    frequency: Optional[FrequencyEnum] = None
    interval_unit: Optional[str] = None  # day, week, month, year
    interval_count: Optional[int] = 1
    
    # Поля для пробного периода
    has_trial: Optional[bool] = False
    trial_start_date: Optional[date] = None
    trial_end_date: Optional[date] = None
    
    # Поля для one_time подписок
    start_date: Optional[date] = None
    duration_type: Optional[str] = None  # days, weeks, months, years, indefinite
    duration_value: Optional[int] = None
    end_date: Optional[date] = None
    
    # Общие поля
    category: Optional[str] = None
    provider: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v

    @validator('currency')
    def validate_currency(cls, v):
        allowed_currencies = ['RUB', 'USD', 'EUR', 'GBP', 'CNY']
        if v not in allowed_currencies:
            raise ValueError(f'Currency must be one of: {allowed_currencies}')
        return v

    @validator('subscription_type')
    def validate_subscription_type(cls, v):
        allowed_types = ['recurring', 'one_time']
        if v not in allowed_types:
            raise ValueError(f'Subscription type must be one of: {allowed_types}')
        return v

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    
    # Тип подписки
    subscription_type: Optional[str] = None
    
    # Поля для recurring подписок
    next_billing_date: Optional[date] = None
    frequency: Optional[FrequencyEnum] = None
    interval_unit: Optional[str] = None
    interval_count: Optional[int] = None
    
    # Поля для пробного периода
    has_trial: Optional[bool] = None
    trial_start_date: Optional[date] = None
    trial_end_date: Optional[date] = None
    
    # Поля для one_time подписок
    start_date: Optional[date] = None
    duration_type: Optional[str] = None
    duration_value: Optional[int] = None
    end_date: Optional[date] = None
    
    # Общие поля
    is_active: Optional[bool] = None
    category: Optional[str] = None
    provider: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None

    @validator('amount')
    def validate_amount(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Amount must be positive')
        return v

    @validator('subscription_type')
    def validate_subscription_type(cls, v):
        if v is not None:
            allowed_types = ['recurring', 'one_time']
            if v not in allowed_types:
                raise ValueError(f'Subscription type must be one of: {allowed_types}')
        return v

class SubscriptionResponse(SubscriptionBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Notification Schemas
class NotificationBase(BaseModel):
    scheduled_at: datetime
    channel: NotificationChannelEnum
    message: Optional[str] = None
    reminder_days: Optional[int] = None

class NotificationCreate(NotificationBase):
    subscription_id: Optional[int] = None

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    subscription_id: Optional[int] = None
    sent: bool
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Analytics Schemas
class AnalyticsResponse(BaseModel):
    period_start: date
    period_end: date
    total_spent: float
    currency: str
    subscription_count: int
    category_breakdown: Optional[dict] = None

    class Config:
        from_attributes = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
    telegram_id: Optional[str] = None

class LoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    telegram_id: Optional[str] = None

class TelegramAuth(BaseModel):
    telegram_id: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

# API Response Schemas
class MessageResponse(BaseModel):
    message: str
    success: bool = True

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    success: bool = False

# Pagination Schemas
class PaginationParams(BaseModel):
    page: int = 1
    size: int = 20
    
    @validator('page')
    def validate_page(cls, v):
        if v < 1:
            raise ValueError('Page must be >= 1')
        return v
    
    @validator('size')
    def validate_size(cls, v):
        if v < 1 or v > 100:
            raise ValueError('Size must be between 1 and 100')
        return v

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    size: int
    pages: int

# Telegram Bot Schemas
class TelegramWebhook(BaseModel):
    update_id: int
    message: Optional[dict] = None
    callback_query: Optional[dict] = None

class TelegramCommand(BaseModel):
    command: str
    args: Optional[str] = None

# Subscription Templates
class SubscriptionTemplate(BaseModel):
    name: str
    provider: str
    category: str
    logo_url: str
    website_url: str
    common_amounts: List[float]
    common_frequencies: List[FrequencyEnum]

# Settings Schemas
class UserSettings(BaseModel):
    timezone: str = "Europe/Moscow"
    language: str = "ru"
    notification_enabled: bool = True
    reminder_days: List[int] = [1, 3, 7]
    default_currency: str = "RUB"
    theme: str = "light"

class SettingsUpdate(BaseModel):
    timezone: Optional[str] = None
    language: Optional[str] = None
    notification_enabled: Optional[bool] = None
    reminder_days: Optional[List[int]] = None
    default_currency: Optional[str] = None
    theme: Optional[str] = None
