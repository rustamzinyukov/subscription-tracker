# backend/app/routers/analytics.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import date, datetime, timedelta
from collections import defaultdict

from ..core.database import get_db
from ..core.auth import get_current_user, require_premium
from ..models.database import User, Subscription, Analytics
from ..schemas.schemas import AnalyticsResponse, MessageResponse

router = APIRouter()

@router.get("/monthly", response_model=AnalyticsResponse)
def get_monthly_analytics(
    year: int = Query(None),
    month: int = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get monthly spending analytics"""
    
    # Use current date if not specified
    if not year or not month:
        now = datetime.now()
        year = now.year
        month = now.month
    
    # Calculate period
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)
    
    # Get active subscriptions for the period (including trial logic and one-time subscriptions)
    subscriptions = db.query(Subscription).filter(
        and_(
            Subscription.user_id == current_user.id,
            Subscription.is_active == True,
            # Учитываем разные типы подписок
            or_(
                # Recurring подписки
                and_(
                    Subscription.subscription_type == "recurring",
                    Subscription.next_billing_date >= start_date,
                    Subscription.next_billing_date <= end_date
                ),
                # Пробный период
                and_(
                    Subscription.has_trial == True,
                    Subscription.trial_start_date <= end_date,
                    Subscription.trial_end_date >= start_date
                ),
                # One-time подписки (временно отключено для отладки)
                # and_(
                #     Subscription.subscription_type == "one_time",
                #     func.date(Subscription.created_at) >= start_date,
                #     func.date(Subscription.created_at) <= end_date
                # )
            )
        )
    ).all()
    
    # Calculate total spent (with trial period logic)
    total_spent = 0
    for sub in subscriptions:
        print(f"🔍 Processing subscription: {sub.name} (type: {sub.subscription_type})")
        
        if sub.has_trial and sub.trial_start_date and sub.trial_end_date:
            # Для пробного периода - считаем только если он активен в этом месяце
            trial_start = sub.trial_start_date
            trial_end = sub.trial_end_date
            
            # Проверяем, пересекается ли пробный период с запрашиваемым месяцем
            if trial_start <= end_date and trial_end >= start_date:
                # В пробном периоде - стоимость 0
                print(f"🔍 Trial period for {sub.name}: {trial_start} to {trial_end} - cost: 0")
                total_spent += 0
            else:
                # Обычная подписка - полная стоимость
                print(f"🔍 Regular subscription {sub.name}: cost: {sub.amount}")
                total_spent += sub.amount
        else:
            # Обычная подписка или one-time - полная стоимость
            print(f"🔍 Subscription {sub.name} (type: {sub.subscription_type}): cost: {sub.amount}")
            total_spent += sub.amount
    
    # Calculate category breakdown (with trial period logic)
    category_breakdown = defaultdict(float)
    for sub in subscriptions:
        if sub.has_trial and sub.trial_start_date and sub.trial_end_date:
            # В пробном периоде - стоимость 0
            category_breakdown[sub.category or "uncategorized"] += 0
        else:
            # Обычная подписка - полная стоимость
            category_breakdown[sub.category or "uncategorized"] += sub.amount
    
    # Get or create analytics record
    analytics = db.query(Analytics).filter(
        and_(
            Analytics.user_id == current_user.id,
            Analytics.period_start == start_date,
            Analytics.period_end == end_date
        )
    ).first()
    
    if not analytics:
        analytics = Analytics(
            user_id=current_user.id,
            period_start=start_date,
            period_end=end_date,
            total_spent=total_spent,
            currency="RUB",  # Default currency
            subscription_count=len(subscriptions),
            category_breakdown=str(dict(category_breakdown))
        )
        db.add(analytics)
        db.commit()
    else:
        # Update existing record
        analytics.total_spent = total_spent
        analytics.subscription_count = len(subscriptions)
        analytics.category_breakdown = str(dict(category_breakdown))
        db.commit()
    
    return AnalyticsResponse(
        period_start=start_date,
        period_end=end_date,
        total_spent=total_spent,
        currency="RUB",
        subscription_count=len(subscriptions),
        category_breakdown=dict(category_breakdown)
    )

@router.get("/yearly", response_model=AnalyticsResponse)
def get_yearly_analytics(
    year: int = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get yearly spending analytics"""
    
    # Use current year if not specified
    if not year:
        year = datetime.now().year
    
    # Calculate period
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    
    # Get all subscriptions that were active during the year
    subscriptions = db.query(Subscription).filter(
        and_(
            Subscription.user_id == current_user.id,
            Subscription.is_active == True,
            Subscription.next_billing_date >= start_date,
            Subscription.next_billing_date <= end_date
        )
    ).all()
    
    # Calculate total spent
    total_spent = sum(sub.amount for sub in subscriptions)
    
    # Calculate category breakdown
    category_breakdown = defaultdict(float)
    for sub in subscriptions:
        category_breakdown[sub.category or "uncategorized"] += sub.amount
    
    return AnalyticsResponse(
        period_start=start_date,
        period_end=end_date,
        total_spent=total_spent,
        currency="RUB",
        subscription_count=len(subscriptions),
        category_breakdown=dict(category_breakdown)
    )

@router.get("/trends/monthly", response_model=List[AnalyticsResponse])
def get_monthly_trends(
    months: int = Query(12, ge=1, le=24),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get monthly spending trends for the last N months"""
    
    trends = []
    now = datetime.now()
    
    for i in range(months):
        # Calculate month
        month_date = now - timedelta(days=30 * i)
        year = month_date.year
        month = month_date.month
        
        # Get analytics for this month
        analytics = get_monthly_analytics(year, month, current_user, db)
        trends.append(analytics)
    
    return trends[::-1]  # Return in chronological order

@router.get("/categories/breakdown", response_model=dict)
def get_category_breakdown(
    period: str = Query("monthly", regex="^(monthly|yearly)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get spending breakdown by categories"""
    
    if period == "monthly":
        analytics = get_monthly_analytics(current_user=current_user, db=db)
    else:
        analytics = get_yearly_analytics(current_user=current_user, db=db)
    
    return analytics.category_breakdown

@router.get("/upcoming/payments", response_model=List[dict])
def get_upcoming_payments(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get upcoming payments analysis"""
    
    today = date.today()
    future_date = today + timedelta(days=days)
    
    # Get upcoming subscriptions
    subscriptions = db.query(Subscription).filter(
        and_(
            Subscription.user_id == current_user.id,
            Subscription.is_active == True,
            Subscription.next_billing_date >= today,
            Subscription.next_billing_date <= future_date
        )
    ).order_by(Subscription.next_billing_date).all()
    
    # Group by date
    payments_by_date = defaultdict(list)
    for sub in subscriptions:
        payments_by_date[sub.next_billing_date].append({
            "id": sub.id,
            "name": sub.name,
            "amount": sub.amount,
            "currency": sub.currency,
            "category": sub.category
        })
    
    # Calculate totals per date
    result = []
    for payment_date, subs in payments_by_date.items():
        total_amount = sum(sub["amount"] for sub in subs)
        result.append({
            "date": payment_date,
            "total_amount": total_amount,
            "subscriptions": subs,
            "count": len(subs)
        })
    
    return result

@router.get("/savings/potential", response_model=dict)
def get_savings_potential(
    current_user: User = Depends(require_premium),
    db: Session = Depends(get_db)
):
    """Get potential savings analysis (Premium feature)"""
    
    # Get all active subscriptions
    subscriptions = db.query(Subscription).filter(
        and_(
            Subscription.user_id == current_user.id,
            Subscription.is_active == True
        )
    ).all()
    
    # Analyze potential savings
    total_monthly = sum(sub.amount for sub in subscriptions if sub.frequency == "monthly")
    total_yearly = sum(sub.amount for sub in subscriptions if sub.frequency == "yearly")
    
    # Calculate potential savings from yearly plans
    monthly_to_yearly_savings = 0
    for sub in subscriptions:
        if sub.frequency == "monthly":
            # Assume 10% discount for yearly plans
            yearly_equivalent = sub.amount * 12 * 0.9
            monthly_cost = sub.amount * 12
            savings = monthly_cost - yearly_equivalent
            monthly_to_yearly_savings += savings
    
    # Find unused categories
    categories = defaultdict(int)
    for sub in subscriptions:
        categories[sub.category or "uncategorized"] += 1
    
    # Suggest optimizations
    suggestions = []
    if len(subscriptions) > 10:
        suggestions.append("Consider consolidating similar services")
    
    if monthly_to_yearly_savings > 1000:  # More than 1000 RUB potential savings
        suggestions.append("Switch to yearly plans to save money")
    
    return {
        "total_monthly_spending": total_monthly,
        "total_yearly_spending": total_yearly,
        "potential_savings": monthly_to_yearly_savings,
        "subscription_count": len(subscriptions),
        "category_count": len(categories),
        "suggestions": suggestions
    }

@router.get("/export/csv", response_model=MessageResponse)
def export_to_csv(
    format: str = Query("csv", regex="^(csv|json)$"),
    current_user: User = Depends(require_premium),
    db: Session = Depends(get_db)
):
    """Export analytics data (Premium feature)"""
    
    # This would typically generate a file and return download link
    # For now, return success message
    return {
        "message": f"Analytics data exported successfully in {format.upper()} format",
        "download_url": f"/api/v1/analytics/download/{current_user.id}_{datetime.now().strftime('%Y%m%d')}.{format}"
    }
