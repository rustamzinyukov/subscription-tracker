#!/usr/bin/env python3
"""
Тест nullable next_billing_date для one_time подписок
"""

import requests
import json
from datetime import date, timedelta

# API endpoints
BASE_URL = "https://disciplined-cat-production.up.railway.app"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
SUBSCRIPTION_URL = f"{BASE_URL}/api/v1/subscriptions"

def test_nullable_billing_date():
    """Тестируем nullable next_billing_date"""
    
    print("Тестируем nullable next_billing_date для one_time подписок...")
    
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
    
    # 2. Создаем one_time подписку БЕЗ next_billing_date
    print("\n2. Создание one_time подписки БЕЗ next_billing_date...")
    
    today = date.today()
    
    one_time_data = {
        "name": "Microsoft Office License",
        "description": "Одноразовая покупка лицензии Office",
        "amount": 8999.99,
        "currency": "RUB",
        "frequency": "one_time",
        "subscription_type": "one_time",
        "start_date": today.isoformat(),
        "duration_type": "indefinite",
        "category": "Software",
        "provider": "Microsoft"
        # НЕ включаем next_billing_date!
    }
    
    print(f"Данные one_time подписки (БЕЗ next_billing_date):")
    print(json.dumps(one_time_data, indent=2, ensure_ascii=False))
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(SUBSCRIPTION_URL, json=one_time_data, headers=headers)
        print(f"Статус создания one_time подписки: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ One_time подписка создана успешно!")
            subscription = response.json()
            print(f"ID подписки: {subscription['id']}")
            print(f"Название: {subscription['name']}")
            print(f"Тип: {subscription['subscription_type']}")
            print(f"Частота: {subscription['frequency']}")
            print(f"Дата начала: {subscription['start_date']}")
            print(f"Следующий платеж: {subscription.get('next_billing_date', 'NULL')}")
            print(f"Тип продолжительности: {subscription.get('duration_type', 'N/A')}")
        else:
            print(f"❌ Ошибка создания one_time подписки: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка при создании one_time подписки: {e}")
    
    # 3. Создаем recurring подписку С next_billing_date
    print("\n3. Создание recurring подписки С next_billing_date...")
    
    next_month = today + timedelta(days=30)
    
    recurring_data = {
        "name": "Spotify Premium",
        "description": "Ежемесячная подписка на музыку",
        "amount": 499.99,
        "currency": "RUB",
        "next_billing_date": next_month.isoformat(),
        "frequency": "monthly",
        "subscription_type": "recurring",
        "interval_unit": "month",
        "interval_count": 1,
        "category": "Entertainment",
        "provider": "Spotify"
    }
    
    print(f"Данные recurring подписки (С next_billing_date):")
    print(json.dumps(recurring_data, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(SUBSCRIPTION_URL, json=recurring_data, headers=headers)
        print(f"Статус создания recurring подписки: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Recurring подписка создана успешно!")
            subscription = response.json()
            print(f"ID подписки: {subscription['id']}")
            print(f"Название: {subscription['name']}")
            print(f"Тип: {subscription['subscription_type']}")
            print(f"Частота: {subscription['frequency']}")
            print(f"Следующий платеж: {subscription.get('next_billing_date', 'NULL')}")
        else:
            print(f"❌ Ошибка создания recurring подписки: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка при создании recurring подписки: {e}")
    
    # 4. Получаем все подписки для проверки
    print("\n4. Получение всех подписок...")
    
    try:
        response = requests.get(SUBSCRIPTION_URL, headers=headers)
        print(f"Статус получения подписок: {response.status_code}")
        
        if response.status_code == 200:
            subscriptions = response.json()
            print(f"Найдено подписок: {len(subscriptions.get('items', []))}")
            
            for sub in subscriptions.get('items', []):
                next_billing = sub.get('next_billing_date', 'NULL')
                print(f"  - {sub['name']} ({sub['subscription_type']}) - next_billing: {next_billing}")
        else:
            print(f"Ошибка получения подписок: {response.text}")
    except Exception as e:
        print(f"Ошибка при получении подписок: {e}")

if __name__ == "__main__":
    test_nullable_billing_date()
