#!/usr/bin/env python3
"""
Скрипт для исправления схемы Supabase
Исправляет проблемы с полями users и subscriptions
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase connection URL
DATABASE_URL = "postgresql://postgres.jwjhpghmstskhxhhrjkm:5ZiZGRXVHjCzUIxS@aws-0-eu-west-1.pooler.supabase.com:6543/postgres"

def fix_supabase_schema():
    """Исправляет схему Supabase"""
    
    print("Исправляем схему Supabase...")
    
    conn = None
    cursor = None
    
    try:
        # Подключаемся к базе данных
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("Подключение к Supabase успешно!")
        
        # 1. Удаляем лишнее поле password_hash
        print("Удаляем лишнее поле password_hash...")
        try:
            cursor.execute("ALTER TABLE users DROP COLUMN password_hash;")
            print("Поле password_hash удалено!")
        except psycopg2.errors.UndefinedColumn:
            print("Поле password_hash уже отсутствует")
        except Exception as e:
            print(f"Ошибка при удалении password_hash: {e}")
        
        # 2. Добавляем недостающие поля для users
        print("Добавляем недостающие поля для users...")
        
        fields_to_add = [
            ("first_name", "VARCHAR(255)"),
            ("last_name", "VARCHAR(255)"),
            ("last_login", "TIMESTAMP WITH TIME ZONE"),
            ("timezone", "VARCHAR(255) DEFAULT 'Europe/Moscow'"),
            ("language", "VARCHAR(255) DEFAULT 'ru'")
        ]
        
        for field_name, field_type in fields_to_add:
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {field_name} {field_type};")
                print(f"Поле {field_name} добавлено!")
            except psycopg2.errors.DuplicateColumn:
                print(f"Поле {field_name} уже существует")
            except Exception as e:
                print(f"Ошибка при добавлении {field_name}: {e}")
        
        # 3. Проверяем текущую схему users
        print("\nТекущая схема таблицы users:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            ORDER BY ordinal_position;
        """)
        
        users_columns = cursor.fetchall()
        for col in users_columns:
            print(f"  - {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
        
        # 4. Проверяем схему subscriptions
        print("\nТекущая схема таблицы subscriptions:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'subscriptions' 
            ORDER BY ordinal_position;
        """)
        
        subscriptions_columns = cursor.fetchall()
        for col in subscriptions_columns:
            print(f"  - {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
        
        # 5. Проверяем данные
        print("\nСтатистика данных:")
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        print(f"  - Пользователей: {user_count}")
        
        cursor.execute("SELECT COUNT(*) FROM subscriptions;")
        subscription_count = cursor.fetchone()[0]
        print(f"  - Подписок: {subscription_count}")
        
        # Сохраняем изменения
        conn.commit()
        print("\nСхема Supabase исправлена успешно!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    fix_supabase_schema()
