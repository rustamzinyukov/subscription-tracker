#!/usr/bin/env python3
"""
Тест исправленной аналитики
"""

import requests
import json
from datetime import date

# API endpoints
BASE_URL = "https://disciplined-cat-production.up.railway.app"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
ANALYTICS_URL = f"{BASE_URL}/api/v1/analytics/monthly"

def test_fixed_analytics():
    """Тестируем исправленную аналитику"""
    
    print("Тестируем исправленную аналитику...")
    
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
    
    # 2. Получаем аналитику за текущий месяц
    today = date.today()
    print(f"\nАналитика за {today.year}-{today.month:02d}")
    
    try:
        response = requests.get(ANALYTICS_URL, headers=headers)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            analytics = response.json()
            print("✅ Аналитика получена успешно!")
            print(f"Общие расходы: {analytics.get('total_spent', 0)} {analytics.get('currency', 'RUB')}")
            print(f"Количество подписок: {analytics.get('subscription_count', 0)}")
            print(f"Период: {analytics.get('period_start')} - {analytics.get('period_end')}")
            
            # Показываем разбивку по категориям
            category_breakdown = analytics.get('category_breakdown', '{}')
            if category_breakdown and category_breakdown != '{}':
                try:
                    categories = json.loads(category_breakdown)
                    print("\nРазбивка по категориям:")
                    for category, amount in categories.items():
                        print(f"  - {category}: {amount} {analytics.get('currency', 'RUB')}")
                except:
                    print(f"Разбивка по категориям: {category_breakdown}")
            else:
                print("Разбивка по категориям: нет данных")
                
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_fixed_analytics()
