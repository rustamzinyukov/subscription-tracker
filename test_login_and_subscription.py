#!/usr/bin/env python3
"""
Тест входа и создания подписки
"""

import requests
import json
from datetime import date, timedelta

# API endpoints
BASE_URL = "https://disciplined-cat-production.up.railway.app"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
SUBSCRIPTION_URL = f"{BASE_URL}/api/v1/subscriptions"

def test_login_and_subscription():
    """Тестируем вход и создание подписки"""
    
    print("Тестируем вход и создание подписки...")
    
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
    
    # 2. Создаем одноразовую подписку
    print("\n2. Создание одноразовой подписки...")
    
    today = date.today()
    
    one_time_subscription_data = {
        "name": "Adobe Creative Suite",
        "description": "Одноразовая покупка лицензии",
        "amount": 5999.99,
        "currency": "RUB",
        "next_billing_date": today.isoformat(),
        "frequency": "one_time",  # Теперь должно работать!
        "subscription_type": "one_time",
        "start_date": today.isoformat(),
        "duration_type": "indefinite",
        "category": "Software",
        "provider": "Adobe",
        "logo_url": "https://adobe.com/logo.png",
        "website_url": "https://adobe.com"
    }
    
    print(f"Данные одноразовой подписки: {json.dumps(one_time_subscription_data, indent=2, ensure_ascii=False)}")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(SUBSCRIPTION_URL, json=one_time_subscription_data, headers=headers)
        print(f"Статус создания одноразовой подписки: {response.status_code}")
        
        if response.status_code == 200:
            print("Одноразовая подписка создана успешно!")
            subscription = response.json()
            print(f"ID подписки: {subscription['id']}")
            print(f"Название: {subscription['name']}")
            print(f"Тип: {subscription['subscription_type']}")
            print(f"Частота: {subscription['frequency']}")
            print(f"Дата начала: {subscription['start_date']}")
            print(f"Тип продолжительности: {subscription['duration_type']}")
        else:
            print(f"Ошибка создания одноразовой подписки: {response.text}")
    except Exception as e:
        print(f"Ошибка при создании одноразовой подписки: {e}")
    
    # 3. Получаем список подписок
    print("\n3. Получение списка подписок...")
    
    try:
        response = requests.get(SUBSCRIPTION_URL, headers=headers)
        print(f"Статус получения подписок: {response.status_code}")
        
        if response.status_code == 200:
            subscriptions = response.json()
            print(f"Найдено подписок: {len(subscriptions.get('items', []))}")
            
            for sub in subscriptions.get('items', []):
                print(f"  - {sub['name']} ({sub['subscription_type']}) - {sub['frequency']}")
        else:
            print(f"Ошибка получения подписок: {response.text}")
    except Exception as e:
        print(f"Ошибка при получении подписок: {e}")

if __name__ == "__main__":
    test_login_and_subscription()
