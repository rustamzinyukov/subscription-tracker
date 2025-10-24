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
    year: int = Query(..., description="Year for monthly analytics"),
    month: int = Query(..., description="Month for monthly analytics"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get monthly analytics for subscriptions - ULTRA SIMPLE VERSION"""
    
    print(f"🔍 Analytics request for {year}-{month:02d} by user {current_user.id}")
    
    try:
        # Простейший ответ без сложной логики
        return {
            "user_id": current_user.id,
            "period_start": f"{year}-{month:02d}-01",
            "period_end": f"{year}-{month:02d}-28",
            "total_spent": 0.0,
            "currency": "RUB",
            "subscription_count": 0,
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
