#!/usr/bin/env python3
"""
Тест аналитики с one-time подписками
"""

import requests
import json
from datetime import date

# API endpoints
BASE_URL = "https://disciplined-cat-production.up.railway.app"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
ANALYTICS_URL = f"{BASE_URL}/api/v1/analytics/monthly"

def test_analytics():
    """Тестируем аналитику"""
    
    print("Тестируем аналитику с one-time подписками...")
    
    # 1. Входим в систему
    print("\n1. Вход в систему...")
    login_data = {
        "email": "test_subscription@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        print(f"Статус входа: {response.status_code}")
        
        if response.status_code == 200:
            print("Вход успешен!")
            user_data = response.json()
            access_token = user_data["access_token"]
            print(f"Получен токен: {access_token[:20]}...")
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
    
    # 2. Получаем аналитику за текущий месяц
    print("\n2. Получение аналитики за текущий месяц...")
    
    today = date.today()
    year = today.year
    month = today.month
    
    print(f"Запрашиваем аналитику за {year}-{month:02d}")
    
    try:
        response = requests.get(f"{ANALYTICS_URL}?year={year}&month={month}", headers=headers)
        print(f"Статус аналитики: {response.status_code}")
        
        if response.status_code == 200:
            analytics = response.json()
            print("Аналитика получена успешно!")
            print(f"Общие расходы: {analytics.get('total_spent', 0)} {analytics.get('currency', 'RUB')}")
            print(f"Количество подписок: {analytics.get('subscription_count', 0)}")
            
            # Показываем разбивку по категориям
            category_breakdown = analytics.get('category_breakdown', {})
            if category_breakdown:
                print("\nРазбивка по категориям:")
                for category, amount in category_breakdown.items():
                    print(f"  - {category}: {amount} {analytics.get('currency', 'RUB')}")
            else:
                print("Разбивка по категориям не найдена")
                
        else:
            print(f"Ошибка получения аналитики: {response.text}")
    except Exception as e:
        print(f"Ошибка при получении аналитики: {e}")
    
    # 3. Получаем аналитику за предыдущий месяц (если есть подписки)
    print("\n3. Получение аналитики за предыдущий месяц...")
    
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    
    print(f"Запрашиваем аналитику за {prev_year}-{prev_month:02d}")
    
    try:
        response = requests.get(f"{ANALYTICS_URL}?year={prev_year}&month={prev_month}", headers=headers)
        print(f"Статус аналитики: {response.status_code}")
        
        if response.status_code == 200:
            analytics = response.json()
            print("Аналитика за предыдущий месяц получена!")
            print(f"Общие расходы: {analytics.get('total_spent', 0)} {analytics.get('currency', 'RUB')}")
            print(f"Количество подписок: {analytics.get('subscription_count', 0)}")
        else:
            print(f"Ошибка получения аналитики: {response.text}")
    except Exception as e:
        print(f"Ошибка при получении аналитики: {e}")

if __name__ == "__main__":
    test_analytics()
