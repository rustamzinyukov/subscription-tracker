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

@router.get("/monthly")
def get_monthly_analytics(
    year: int = Query(None, description="Year for monthly analytics"),
    month: int = Query(None, description="Month for monthly analytics"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get monthly analytics for subscriptions - ULTRA SIMPLE VERSION"""
    
    # Используем текущую дату, если параметры не указаны
    if year is None or month is None:
        now = datetime.now()
        year = now.year
        month = now.month
    
    print(f"🔍 Analytics request for {year}-{month:02d} by user {current_user.id}")
    
    try:
        # Рассчитываем период
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        print(f"🔍 Period: {start_date} to {end_date}")
        
        # Подсчитываем подписки за период
        total_subscriptions = db.query(Subscription).filter(
            and_(
                Subscription.user_id == current_user.id,
                Subscription.is_active == True,
                or_(
                    # Recurring подписки с next_billing_date в периоде
                    and_(
                        Subscription.subscription_type == "recurring",
                        Subscription.next_billing_date >= start_date,
                        Subscription.next_billing_date <= end_date
                    ),
                    # One-time подписки созданные в периоде
                    and_(
                        Subscription.subscription_type == "one_time",
                        func.date(Subscription.created_at) >= start_date,
                        func.date(Subscription.created_at) <= end_date
                    )
                )
            )
        ).count()
        
        print(f"🔍 Subscriptions in period: {total_subscriptions}")
        
        # Расчет расходов за период
        total_spent = 0.0
        subscriptions = db.query(Subscription).filter(
            and_(
                Subscription.user_id == current_user.id,
                Subscription.is_active == True,
                or_(
                    # Recurring подписки с next_billing_date в периоде
                    and_(
                        Subscription.subscription_type == "recurring",
                        Subscription.next_billing_date >= start_date,
                        Subscription.next_billing_date <= end_date
                    ),
                    # One-time подписки созданные в периоде
                    and_(
                        Subscription.subscription_type == "one_time",
                        func.date(Subscription.created_at) >= start_date,
                        func.date(Subscription.created_at) <= end_date
                    )
                )
            )
        ).all()
        
        for sub in subscriptions:
            print(f"🔍 Subscription: {sub.name} ({sub.subscription_type}) - {sub.amount} {sub.currency}")
            total_spent += sub.amount
        
        print(f"🔍 Total spent in period: {total_spent}")
        
        return {
            "user_id": current_user.id,
            "period_start": f"{year}-{month:02d}-01",
            "period_end": f"{year}-{month:02d}-28",
            "total_spent": total_spent,
            "currency": "RUB",
            "subscription_count": total_subscriptions,
            "category_breakdown": "{}"
        }
        
    except Exception as e:
        print(f"❌ Error in analytics: {e}")
        return {"error": str(e)}

@router.get("/yearly", response_model=AnalyticsResponse)
def get_yearly_analytics(
    year: int = Query(..., description="Year for yearly analytics"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get yearly analytics for subscriptions"""
    
    # Простая реализация
    return get_monthly_analytics(year, 1, current_user, db)
