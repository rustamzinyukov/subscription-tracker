#!/usr/bin/env python3
"""
Database initialization script for Subscription Tracker
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_database():
    """Initialize database with tables and sample data"""
    
    print("🗄️ Initializing database...")
    
    try:
        # Import database modules
        from backenddatabase import engine, create_tables
        from backendappmodels import Base
        
        # Create all tables
        print("📋 Creating database tables...")
        create_tables()
        print("✅ Database tables created successfully!")
        
        # Add sample data if in development
        if os.getenv("ENVIRONMENT", "development") == "development":
            print("🌱 Adding sample data...")
            add_sample_data()
            print("✅ Sample data added successfully!")
        
        print("🎉 Database initialization completed!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

def add_sample_data():
    """Add sample data for development"""
    
    from backenddatabase import SessionLocal
    from backendappmodels import User, Subscription, FrequencyEnum
    from datetime import date, timedelta
    
    db = SessionLocal()
    
    try:
        # Create sample user
        sample_user = User(
            telegram_id="123456789",
            username="sample_user",
            first_name="Sample",
            last_name="User",
            email="sample@example.com",
            is_premium=False,
            timezone="Europe/Moscow",
            language="ru"
        )
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.telegram_id == "123456789").first()
        if existing_user:
            print("📝 Sample user already exists, skipping...")
            return
        
        db.add(sample_user)
        db.commit()
        db.refresh(sample_user)
        
        # Create sample subscriptions
        sample_subscriptions = [
            {
                "name": "Netflix",
                "amount": 599.0,
                "currency": "RUB",
                "next_billing_date": date.today() + timedelta(days=15),
                "frequency": FrequencyEnum.MONTHLY,
                "category": "streaming",
                "provider": "Netflix"
            },
            {
                "name": "Spotify Premium",
                "amount": 299.0,
                "currency": "RUB",
                "next_billing_date": date.today() + timedelta(days=7),
                "frequency": FrequencyEnum.MONTHLY,
                "category": "music",
                "provider": "Spotify"
            },
            {
                "name": "Яндекс Плюс",
                "amount": 199.0,
                "currency": "RUB",
                "next_billing_date": date.today() + timedelta(days=20),
                "frequency": FrequencyEnum.MONTHLY,
                "category": "streaming",
                "provider": "Яндекс"
            }
        ]
        
        for sub_data in sample_subscriptions:
            subscription = Subscription(
                user_id=sample_user.id,
                **sub_data
            )
            db.add(subscription)
        
        db.commit()
        print(f"✅ Added {len(sample_subscriptions)} sample subscriptions")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
