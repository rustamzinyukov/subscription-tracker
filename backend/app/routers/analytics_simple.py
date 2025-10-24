# backend/app/routers/analytics_simple.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import date, datetime, timedelta
from collections import defaultdict
import json

from ..core.database import get_db
from ..core.auth import get_current_user, require_premium
from ..models.database import User, Subscription, Analytics
from ..schemas.schemas import AnalyticsResponse

router = APIRouter()

@router.get("/monthly", response_model=AnalyticsResponse)
def get_monthly_analytics(
    year: int = Query(..., description="Year for monthly analytics"),
    month: int = Query(..., description="Month for monthly analytics"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get monthly analytics for subscriptions - SIMPLIFIED VERSION"""
    
    print(f"🔍 Analytics request for {year}-{month:02d} by user {current_user.id}")
    
    try:
        # Простой подсчет подписок
        total_subscriptions = db.query(Subscription).filter(
            and_(
                Subscription.user_id == current_user.id,
                Subscription.is_active == True
            )
        ).count()
        
        print(f"🔍 Total active subscriptions: {total_subscriptions}")
        
        # Простой расчет расходов
        total_spent = 0.0
        subscriptions = db.query(Subscription).filter(
            and_(
                Subscription.user_id == current_user.id,
                Subscription.is_active == True
            )
        ).all()
        
        for sub in subscriptions:
            print(f"🔍 Subscription: {sub.name} - {sub.amount} {sub.currency}")
            total_spent += sub.amount
        
        print(f"🔍 Total spent: {total_spent}")
        
        # Создаем простой ответ
        analytics = Analytics(
            user_id=current_user.id,
            period_start=date(year, month, 1),
            period_end=date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year + 1, 1, 1) - timedelta(days=1),
            total_spent=total_spent,
            currency="RUB",
            subscription_count=total_subscriptions,
            category_breakdown=json.dumps({"uncategorized": total_spent})
        )
        
        print(f"🔍 Analytics created successfully")
        return analytics
        
    except Exception as e:
        print(f"❌ Error in analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

@router.get("/yearly", response_model=AnalyticsResponse)
def get_yearly_analytics(
    year: int = Query(..., description="Year for yearly analytics"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get yearly analytics for subscriptions"""
    
    # Простая реализация
    return get_monthly_analytics(year, 1, current_user, db)
