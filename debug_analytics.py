#!/usr/bin/env python3
"""
Отладка аналитики - проверяем что именно вызывает ошибку 500
"""

import requests
import json
from datetime import date

# API endpoints
BASE_URL = "https://disciplined-cat-production.up.railway.app"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
ANALYTICS_URL = f"{BASE_URL}/api/v1/analytics/monthly"

def debug_analytics():
    """Отладка аналитики"""
    
    print("Отладка аналитики...")
    
    # 1. Входим в систему
    login_data = {
        "email": "test_subscription@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        if response.status_code == 200:
            user_data = response.json()
            access_token = user_data["access_token"]
            print("Вход успешен!")
        else:
            print(f"Ошибка входа: {response.text}")
            return
    except Exception as e:
        print(f"Ошибка при входе: {e}")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 2. Пробуем разные варианты запросов аналитики
    today = date.today()
    
    # Вариант 1: Текущий месяц
    print(f"\n1. Аналитика за {today.year}-{today.month:02d}")
    try:
        response = requests.get(f"{ANALYTICS_URL}?year={today.year}&month={today.month}", headers=headers)
        print(f"Статус: {response.status_code}")
        if response.status_code != 200:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # Вариант 2: Предыдущий месяц
    prev_month = today.month - 1 if today.month > 1 else 12
    prev_year = today.year if today.month > 1 else today.year - 1
    print(f"\n2. Аналитика за {prev_year}-{prev_month:02d}")
    try:
        response = requests.get(f"{ANALYTICS_URL}?year={prev_year}&month={prev_month}", headers=headers)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            analytics = response.json()
            print(f"Расходы: {analytics.get('total_spent', 0)} {analytics.get('currency', 'RUB')}")
            print(f"Подписок: {analytics.get('subscription_count', 0)}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # Вариант 3: Январь 2025
    print(f"\n3. Аналитика за 2025-01")
    try:
        response = requests.get(f"{ANALYTICS_URL}?year=2025&month=1", headers=headers)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            analytics = response.json()
            print(f"Расходы: {analytics.get('total_spent', 0)} {analytics.get('currency', 'RUB')}")
            print(f"Подписок: {analytics.get('subscription_count', 0)}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    debug_analytics()
