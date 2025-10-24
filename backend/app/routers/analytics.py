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
        
        # Расчет расходов с учетом пробных периодов и группировкой по категориям
        category_breakdown = defaultdict(float)
        
        for sub in subscriptions:
            print(f"🔍 Subscription: {sub.name} ({sub.subscription_type}) - {sub.amount} {sub.currency}")
            
            # Проверяем пробный период
            if sub.has_trial and sub.trial_start_date and sub.trial_end_date:
                # Если подписка в пробном периоде в этом месяце
                if (sub.trial_start_date <= end_date and 
                    sub.trial_end_date >= start_date):
                    print(f"🔍 Trial period for {sub.name}: cost = 0")
                    category_breakdown[sub.category or "uncategorized"] += 0
                else:
                    # Обычная подписка
                    total_spent += sub.amount
                    category_breakdown[sub.category or "uncategorized"] += sub.amount
            else:
                # Обычная подписка без пробного периода
                total_spent += sub.amount
                category_breakdown[sub.category or "uncategorized"] += sub.amount
        
        print(f"🔍 Total spent in period: {total_spent}")
        print(f"🔍 Category breakdown: {dict(category_breakdown)}")
        
        return {
            "user_id": current_user.id,
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "total_spent": total_spent,
            "currency": "RUB",
            "subscription_count": total_subscriptions,
            "category_breakdown": json.dumps(dict(category_breakdown))
        }
        
    except Exception as e:
        print(f"❌ Error in analytics: {e}")
        return {"error": str(e)}

@router.get("/yearly")
def get_yearly_analytics(
    year: int = Query(None, description="Year for yearly analytics"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get yearly analytics for subscriptions"""
    
    # Используем текущий год, если не указан
    if year is None:
        year = datetime.now().year
    
    print(f"🔍 Yearly analytics request for {year} by user {current_user.id}")
    
    try:
        # Рассчитываем период (весь год)
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        
        print(f"🔍 Year period: {start_date} to {end_date}")
        
        # Подсчитываем подписки за год
        total_subscriptions = db.query(Subscription).filter(
            and_(
                Subscription.user_id == current_user.id,
                Subscription.is_active == True,
                or_(
                    # Recurring подписки с next_billing_date в году
                    and_(
                        Subscription.subscription_type == "recurring",
                        Subscription.next_billing_date >= start_date,
                        Subscription.next_billing_date <= end_date
                    ),
                    # One-time подписки созданные в году
                    and_(
                        Subscription.subscription_type == "one_time",
                        func.date(Subscription.created_at) >= start_date,
                        func.date(Subscription.created_at) <= end_date
                    )
                )
            )
        ).count()
        
        print(f"🔍 Subscriptions in year: {total_subscriptions}")
        
        # Расчет расходов за год
        total_spent = 0.0
        subscriptions = db.query(Subscription).filter(
            and_(
                Subscription.user_id == current_user.id,
                Subscription.is_active == True,
                or_(
                    # Recurring подписки с next_billing_date в году
                    and_(
                        Subscription.subscription_type == "recurring",
                        Subscription.next_billing_date >= start_date,
                        Subscription.next_billing_date <= end_date
                    ),
                    # One-time подписки созданные в году
                    and_(
                        Subscription.subscription_type == "one_time",
                        func.date(Subscription.created_at) >= start_date,
                        func.date(Subscription.created_at) <= end_date
                    )
                )
            )
        ).all()
        
        # Расчет расходов с учетом пробных периодов и группировкой по категориям
        category_breakdown = defaultdict(float)
        
        for sub in subscriptions:
            print(f"🔍 Yearly subscription: {sub.name} ({sub.subscription_type}) - {sub.amount} {sub.currency}")
            
            # Проверяем пробный период
            if sub.has_trial and sub.trial_start_date and sub.trial_end_date:
                # Если подписка в пробном периоде в этом году
                if (sub.trial_start_date <= end_date and 
                    sub.trial_end_date >= start_date):
                    print(f"🔍 Trial period for {sub.name}: cost = 0")
                    category_breakdown[sub.category or "uncategorized"] += 0
                else:
                    # Обычная подписка
                    total_spent += sub.amount
                    category_breakdown[sub.category or "uncategorized"] += sub.amount
            else:
                # Обычная подписка без пробного периода
                total_spent += sub.amount
                category_breakdown[sub.category or "uncategorized"] += sub.amount
        
        print(f"🔍 Total spent in year: {total_spent}")
        print(f"🔍 Yearly category breakdown: {dict(category_breakdown)}")
        
        return {
            "user_id": current_user.id,
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "total_spent": total_spent,
            "currency": "RUB",
            "subscription_count": total_subscriptions,
            "category_breakdown": json.dumps(dict(category_breakdown))
        }
        
    except Exception as e:
        print(f"❌ Error in yearly analytics: {e}")
        return {"error": str(e)}
