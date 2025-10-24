# backend/app/routers/subscriptions.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import date, datetime, timedelta

from ..core.database import get_db
from ..core.auth import get_current_user, require_premium
from ..models.database import User, Subscription, FrequencyEnum
from ..schemas.schemas import (
    SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse,
    PaginationParams, PaginatedResponse, MessageResponse
)

router = APIRouter()

@router.get("", response_model=PaginatedResponse)
def get_subscriptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None
):
    """Get user's subscriptions with pagination and filtering"""
    
    # Check free tier limit (temporarily disabled for testing)
    # if not current_user.is_premium:
    #     total_subs = db.query(Subscription).filter(Subscription.user_id == current_user.id).count()
    #     if total_subs >= 5:  # Free tier limit
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="Free tier limit reached. Upgrade to premium for unlimited subscriptions."
    #         )
    
    # Build query
    query = db.query(Subscription).filter(Subscription.user_id == current_user.id)
    
    # Apply filters
    if category:
        query = query.filter(Subscription.category == category)
    
    if is_active is not None:
        query = query.filter(Subscription.is_active == is_active)
    
    if search:
        query = query.filter(
            or_(
                Subscription.name.ilike(f"%{search}%"),
                Subscription.description.ilike(f"%{search}%"),
                Subscription.provider.ilike(f"%{search}%")
            )
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    subscriptions = query.offset(offset).limit(size).all()
    
    # Calculate pages
    pages = (total + size - 1) // size
    
    # Debug logging
    print(f"🔍 Returning {len(subscriptions)} subscriptions for user {current_user.id}")
    for sub in subscriptions:
        print(f"🔍 Subscription: name='{sub.name}', amount={sub.amount}, next_billing_date={sub.next_billing_date}")
    
    # Convert subscriptions to response format
    subscription_responses = []
    for sub in subscriptions:
        try:
            response = SubscriptionResponse.from_orm(sub).dict()
            subscription_responses.append(response)
            print(f"🔍 Converted subscription: {response}")
        except Exception as e:
            print(f"❌ Error converting subscription {sub.id}: {e}")
            # Fallback: create response manually
            subscription_responses.append({
                "id": sub.id,
                "name": sub.name,
                "description": sub.description,
                "amount": sub.amount,
                "currency": sub.currency,
                "frequency": sub.frequency,
                "next_billing_date": sub.next_billing_date.isoformat() if sub.next_billing_date else None,
                "is_active": sub.is_active,
                "category": sub.category,
                "provider": sub.provider,
                "logo_url": sub.logo_url,
                "website_url": sub.website_url,
                "created_at": sub.created_at.isoformat() if sub.created_at else None,
                "updated_at": sub.updated_at.isoformat() if sub.updated_at else None
            })
    
    print(f"🔍 Final subscription_responses: {len(subscription_responses)} items")
    
    return PaginatedResponse(
        items=subscription_responses,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific subscription by ID"""
    
    subscription = db.query(Subscription).filter(
        and_(
            Subscription.id == subscription_id,
            Subscription.user_id == current_user.id
        )
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    return subscription

@router.post("", response_model=SubscriptionResponse)
def create_subscription(
    subscription_data: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new subscription"""
    
    # Debug logging
    print(f"🔍 Creating subscription for user {current_user.id}")
    print(f"🔍 Subscription data received: {subscription_data.dict()}")
    
    # Check free tier limit (temporarily disabled for testing)
    # if not current_user.is_premium:
    #     total_subs = db.query(Subscription).filter(Subscription.user_id == current_user.id).count()
    #     if total_subs >= 5:  # Free tier limit
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="Free tier limit reached. Upgrade to premium for unlimited subscriptions."
    #         )
    
    # Create subscription
    subscription = Subscription(
        user_id=current_user.id,
        name=subscription_data.name,
        description=subscription_data.description,
        amount=subscription_data.amount,
        currency=subscription_data.currency,
        next_billing_date=subscription_data.next_billing_date,
        frequency=subscription_data.frequency,
        category=subscription_data.category,
        provider=subscription_data.provider,
        logo_url=subscription_data.logo_url,
        website_url=subscription_data.website_url,
    )
    
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    
    print(f"🔍 Created subscription: {subscription.name}, amount: {subscription.amount}")
    print(f"🔍 Subscription type: {subscription.subscription_type}")
    print(f"🔍 Subscription object: {subscription}")
    
    return subscription

@router.put("/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(
    subscription_id: int,
    subscription_update: SubscriptionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a subscription"""
    
    subscription = db.query(Subscription).filter(
        and_(
            Subscription.id == subscription_id,
            Subscription.user_id == current_user.id
        )
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    # Update fields
    for field, value in subscription_update.dict(exclude_unset=True).items():
        setattr(subscription, field, value)
    
    db.commit()
    db.refresh(subscription)
    
    return subscription

@router.delete("/{subscription_id}", response_model=MessageResponse)
def delete_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a subscription"""
    
    subscription = db.query(Subscription).filter(
        and_(
            Subscription.id == subscription_id,
            Subscription.user_id == current_user.id
        )
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    # Hard delete - actually remove from database
    print(f"🗑️ Deleting subscription {subscription_id} from database")
    print(f"🗑️ Subscription name: {subscription.name}")
    
    db.delete(subscription)
    db.commit()
    
    print(f"✅ Subscription {subscription_id} successfully deleted from database")
    
    return {"message": "Subscription successfully deleted"}

@router.post("/{subscription_id}/activate", response_model=SubscriptionResponse)
def activate_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Activate a cancelled subscription"""
    
    subscription = db.query(Subscription).filter(
        and_(
            Subscription.id == subscription_id,
            Subscription.user_id == current_user.id
        )
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    subscription.is_active = True
    subscription.cancelled_at = None
    
    db.commit()
    db.refresh(subscription)
    
    return subscription

@router.post("/{subscription_id}/cancel", response_model=SubscriptionResponse)
def cancel_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a subscription"""
    
    subscription = db.query(Subscription).filter(
        and_(
            Subscription.id == subscription_id,
            Subscription.user_id == current_user.id
        )
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    subscription.is_active = False
    subscription.cancelled_at = datetime.utcnow()
    
    db.commit()
    db.refresh(subscription)
    
    return subscription

@router.get("/upcoming/billing", response_model=List[SubscriptionResponse])
def get_upcoming_billing(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get subscriptions with upcoming billing dates"""
    
    today = date.today()
    future_date = today + timedelta(days=days)
    
    subscriptions = db.query(Subscription).filter(
        and_(
            Subscription.user_id == current_user.id,
            Subscription.is_active == True,
            Subscription.next_billing_date >= today,
            Subscription.next_billing_date <= future_date
        )
    ).order_by(Subscription.next_billing_date).all()
    
    return subscriptions

@router.get("/categories/list", response_model=List[str])
def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of categories used by user"""
    
    categories = db.query(Subscription.category).filter(
        and_(
            Subscription.user_id == current_user.id,
            Subscription.category.isnot(None)
        )
    ).distinct().all()
    
    return [cat[0] for cat in categories if cat[0]]

@router.get("/templates/popular", response_model=List[dict])
def get_popular_templates():
    """Get popular subscription templates for Russian market"""
    
    templates = [
        {
            "name": "Яндекс Плюс",
            "provider": "Яндекс",
            "category": "streaming",
            "logo_url": "https://yastatic.net/s3/home/plus/plus-logo.svg",
            "website_url": "https://plus.yandex.ru",
            "common_amounts": [199, 299, 399],
            "common_frequencies": ["monthly", "yearly"]
        },
        {
            "name": "СберПрайм",
            "provider": "Сбер",
            "category": "shopping",
            "logo_url": "https://sberprime.ru/static/images/logo.svg",
            "website_url": "https://sberprime.ru",
            "common_amounts": [199, 299],
            "common_frequencies": ["monthly", "yearly"]
        },
        {
            "name": "Netflix",
            "provider": "Netflix",
            "category": "streaming",
            "logo_url": "https://upload.wikimedia.org/wikipedia/commons/7/77/Netflix_2015_logo.svg",
            "website_url": "https://netflix.com",
            "common_amounts": [599, 799, 999],
            "common_frequencies": ["monthly"]
        },
        {
            "name": "Spotify",
            "provider": "Spotify",
            "category": "music",
            "logo_url": "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg",
            "website_url": "https://spotify.com",
            "common_amounts": [199, 299],
            "common_frequencies": ["monthly", "yearly"]
        },
        {
            "name": "Okko",
            "provider": "Okko",
            "category": "streaming",
            "logo_url": "https://okko.tv/static/images/logo.svg",
            "website_url": "https://okko.tv",
            "common_amounts": [199, 299, 399],
            "common_frequencies": ["monthly", "yearly"]
        }
    ]
    
    return templates
