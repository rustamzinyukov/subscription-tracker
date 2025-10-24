#!/usr/bin/env python3
"""
Тест создания подписки через API
Проверяем, что все поля соответствуют схеме
"""

import requests
import json
from datetime import date, timedelta

# API endpoints
BASE_URL = "https://disciplined-cat-production.up.railway.app"
REGISTER_URL = f"{BASE_URL}/api/v1/auth/register"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
SUBSCRIPTION_URL = f"{BASE_URL}/api/v1/subscriptions"

def test_subscription_creation():
    """Тестируем создание подписки"""
    
    print("Тестируем создание подписки...")
    
    # 1. Регистрируем пользователя
    print("\n1. Регистрация пользователя...")
    register_data = {
        "email": "test_subscription@example.com",
        "password": "testpassword123",
        "username": "testuser_subscription",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(REGISTER_URL, json=register_data)
        print(f"Статус регистрации: {response.status_code}")
        
        if response.status_code == 200:
            print("Регистрация успешна!")
            user_data = response.json()
            access_token = user_data["access_token"]
            print(f"Получен токен: {access_token[:20]}...")
        else:
            print(f"Ошибка регистрации: {response.text}")
            return
    except Exception as e:
        print(f"Ошибка при регистрации: {e}")
        return
    
    # 2. Создаем подписку с продвинутыми полями
    print("\n2. Создание подписки с продвинутыми полями...")
    
    # Подготавливаем даты
    today = date.today()
    next_month = today + timedelta(days=30)
    trial_start = today
    trial_end = today + timedelta(days=7)
    
    subscription_data = {
        "name": "Netflix Premium",
        "description": "Продвинутая подписка с пробным периодом",
        "amount": 999.99,
        "currency": "RUB",
        "next_billing_date": next_month.isoformat(),
        "frequency": "monthly",
        "subscription_type": "recurring",
        "interval_unit": "month",
        "interval_count": 1,
        "has_trial": True,
        "trial_start_date": trial_start.isoformat(),
        "trial_end_date": trial_end.isoformat(),
        "category": "Entertainment",
        "provider": "Netflix",
        "logo_url": "https://netflix.com/logo.png",
        "website_url": "https://netflix.com"
    }
    
    print(f"Данные подписки: {json.dumps(subscription_data, indent=2, ensure_ascii=False)}")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(SUBSCRIPTION_URL, json=subscription_data, headers=headers)
        print(f"Статус создания подписки: {response.status_code}")
        
        if response.status_code == 200:
            print("Подписка создана успешно!")
            subscription = response.json()
            print(f"ID подписки: {subscription['id']}")
            print(f"Название: {subscription['name']}")
            print(f"Тип: {subscription['subscription_type']}")
            print(f"Пробный период: {subscription['has_trial']}")
            print(f"Дата начала пробного периода: {subscription['trial_start_date']}")
            print(f"Дата окончания пробного периода: {subscription['trial_end_date']}")
            print(f"Следующий платеж: {subscription['next_billing_date']}")
        else:
            print(f"Ошибка создания подписки: {response.text}")
    except Exception as e:
        print(f"Ошибка при создании подписки: {e}")
    
    # 3. Создаем одноразовую подписку
    print("\n3. Создание одноразовой подписки...")
    
    one_time_subscription_data = {
        "name": "Adobe Creative Suite",
        "description": "Одноразовая покупка лицензии",
        "amount": 5999.99,
        "currency": "RUB",
        "next_billing_date": today.isoformat(),  # Для одноразовых тоже нужен next_billing_date
        "frequency": "one_time",
        "subscription_type": "one_time",
        "start_date": today.isoformat(),
        "duration_type": "indefinite",
        "category": "Software",
        "provider": "Adobe",
        "logo_url": "https://adobe.com/logo.png",
        "website_url": "https://adobe.com"
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
            print(f"Дата начала: {subscription['start_date']}")
            print(f"Тип продолжительности: {subscription['duration_type']}")
        else:
            print(f"Ошибка создания одноразовой подписки: {response.text}")
    except Exception as e:
        print(f"Ошибка при создании одноразовой подписки: {e}")

if __name__ == "__main__":
    test_subscription_creation()
