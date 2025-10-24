#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Прямая миграция на Supabase с готовым URL
"""

import os
import sys
from sqlalchemy import create_engine, text

def migrate_to_supabase():
    """Миграция на Supabase"""
    
    # Готовый URL от Supabase
    supabase_url = "postgresql://postgres:5ZiZGRXVHjCzUIxS@db.jwjhpghmstskhxhhrjkm.supabase.co:5432/postgres"
    
    print(f"Подключаемся к Supabase...")
    
    try:
        # Создаем подключение
        engine = create_engine(supabase_url)
        
        # Тестируем подключение
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Подключение к Supabase успешно!")
        
        # Создаем таблицы
        print("Создаем таблицы...")
        
        # SQL для создания всех таблиц
        create_tables_sql = """
        -- Создаем таблицу users
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            is_premium BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Создаем таблицу subscriptions с продвинутыми полями
        CREATE TABLE IF NOT EXISTS subscriptions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) NOT NULL,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            amount DECIMAL(10,2) NOT NULL,
            currency VARCHAR(10) DEFAULT 'RUB',
            next_billing_date DATE NOT NULL,
            frequency VARCHAR(20) NOT NULL,
            subscription_type VARCHAR(20) DEFAULT 'recurring',
            interval_unit VARCHAR(20),
            interval_count INTEGER DEFAULT 1,
            has_trial BOOLEAN DEFAULT FALSE,
            trial_start_date DATE,
            trial_end_date DATE,
            start_date DATE,
            duration_type VARCHAR(20),
            duration_value INTEGER,
            end_date DATE,
            is_active BOOLEAN DEFAULT TRUE,
            category VARCHAR(100),
            provider VARCHAR(100),
            logo_url TEXT,
            website_url TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            cancelled_at TIMESTAMP WITH TIME ZONE
        );
        
        -- Создаем таблицу analytics
        CREATE TABLE IF NOT EXISTS analytics (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) NOT NULL,
            period_start DATE NOT NULL,
            period_end DATE NOT NULL,
            total_spent DECIMAL(10,2) NOT NULL,
            currency VARCHAR(10) DEFAULT 'RUB',
            subscription_count INTEGER DEFAULT 0,
            category_breakdown JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Создаем таблицу notifications
        CREATE TABLE IF NOT EXISTS notifications (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) NOT NULL,
            subscription_id INTEGER REFERENCES subscriptions(id),
            message TEXT NOT NULL,
            notification_type VARCHAR(50) NOT NULL,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Создаем индексы для производительности
        CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
        CREATE INDEX IF NOT EXISTS idx_subscriptions_is_active ON subscriptions(is_active);
        CREATE INDEX IF NOT EXISTS idx_subscriptions_next_billing_date ON subscriptions(next_billing_date);
        CREATE INDEX IF NOT EXISTS idx_subscriptions_category ON subscriptions(category);
        CREATE INDEX IF NOT EXISTS idx_analytics_user_id ON analytics(user_id);
        CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
        
        -- Создаем функцию для обновления updated_at
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        
        -- Создаем триггеры для автоматического обновления updated_at
        DROP TRIGGER IF EXISTS update_users_updated_at ON users;
        CREATE TRIGGER update_users_updated_at
            BEFORE UPDATE ON users
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
            
        DROP TRIGGER IF EXISTS update_subscriptions_updated_at ON subscriptions;
        CREATE TRIGGER update_subscriptions_updated_at
            BEFORE UPDATE ON subscriptions
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
            
        DROP TRIGGER IF EXISTS update_analytics_updated_at ON analytics;
        CREATE TRIGGER update_analytics_updated_at
            BEFORE UPDATE ON analytics
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
        """
        
        # Выполняем SQL
        with engine.connect() as conn:
            conn.execute(text(create_tables_sql))
            conn.commit()
        
        print("Все таблицы созданы успешно!")
        print("Продвинутые поля добавлены!")
        print("Индексы созданы для производительности!")
        print("Триггеры настроены для автоматического обновления!")
        
        # Проверяем созданные таблицы
        print("\nПроверяем созданные таблицы...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"Созданные таблицы: {tables}")
            
            # Проверяем колонки subscriptions
            result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'subscriptions' 
                ORDER BY ordinal_position
            """))
            columns = [(row[0], row[1]) for row in result.fetchall()]
            print(f"Колонки subscriptions: {len(columns)}")
            for col_name, col_type in columns:
                print(f"  - {col_name}: {col_type}")
        
        print("\nМиграция на Supabase завершена!")
        print("Теперь обновите DATABASE_URL в Railway на новый URL от Supabase")
        
    except Exception as e:
        print(f"Ошибка миграции: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Миграция на Supabase")
    print("=" * 50)
    migrate_to_supabase()
