#!/usr/bin/env python3
"""
Отладка создания подписки через фронтенд
Проверяем, какие именно данные отправляет фронтенд
"""

import requests
import json
from datetime import date, timedelta

# API endpoints
BASE_URL = "https://disciplined-cat-production.up.railway.app"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
SUBSCRIPTION_URL = f"{BASE_URL}/api/v1/subscriptions"

def debug_frontend_subscription():
    """Отладка создания подписки как фронтенд"""
    
    print("Отладка создания подписки через фронтенд...")
    
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
    
    # 2. Тестируем разные варианты данных подписки
    print("\n2. Тестируем разные варианты данных...")
    
    today = date.today()
    next_month = today + timedelta(days=30)
    
    # Вариант 1: Минимальные данные (как в простой форме)
    print("\n--- Вариант 1: Минимальные данные ---")
    minimal_data = {
        "name": "Spotify Premium",
        "amount": 499.99,
        "currency": "RUB",
        "next_billing_date": next_month.isoformat(),
        "frequency": "monthly"
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(SUBSCRIPTION_URL, json=minimal_data, headers=headers)
        print(f"Статус минимальных данных: {response.status_code}")
        if response.status_code != 200:
            print(f"Ошибка: {response.text}")
        else:
            print("Минимальные данные работают!")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # Вариант 2: Продвинутые данные (как в AdvancedSubscriptionForm)
    print("\n--- Вариант 2: Продвинутые данные ---")
    advanced_data = {
        "name": "Netflix Premium Advanced",
        "description": "Продвинутая подписка с пробным периодом",
        "amount": 999.99,
        "currency": "RUB",
        "next_billing_date": next_month.isoformat(),
        "frequency": "monthly",
        "subscription_type": "recurring",
        "interval_unit": "month",
        "interval_count": 1,
        "has_trial": True,
        "trial_start_date": today.isoformat(),
        "trial_end_date": (today + timedelta(days=7)).isoformat(),
        "category": "Entertainment",
        "provider": "Netflix",
        "logo_url": "https://netflix.com/logo.png",
        "website_url": "https://netflix.com"
    }
    
    try:
        response = requests.post(SUBSCRIPTION_URL, json=advanced_data, headers=headers)
        print(f"Статус продвинутых данных: {response.status_code}")
        if response.status_code != 200:
            print(f"Ошибка: {response.text}")
        else:
            print("Продвинутые данные работают!")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # Вариант 3: Одноразовая подписка
    print("\n--- Вариант 3: Одноразовая подписка ---")
    one_time_data = {
        "name": "Adobe Creative Suite One Time",
        "description": "Одноразовая покупка лицензии",
        "amount": 5999.99,
        "currency": "RUB",
        "next_billing_date": today.isoformat(),
        "frequency": "one_time",
        "subscription_type": "one_time",
        "start_date": today.isoformat(),
        "duration_type": "indefinite",
        "category": "Software",
        "provider": "Adobe"
    }
    
    try:
        response = requests.post(SUBSCRIPTION_URL, json=one_time_data, headers=headers)
        print(f"Статус одноразовой подписки: {response.status_code}")
        if response.status_code != 200:
            print(f"Ошибка: {response.text}")
        else:
            print("Одноразовая подписка работает!")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # Вариант 4: Проверим, что именно требует схема
    print("\n--- Вариант 4: Проверка схемы ---")
    
    # Получаем OpenAPI схему
    try:
        schema_response = requests.get(f"{BASE_URL}/docs")
        print(f"Статус получения схемы: {schema_response.status_code}")
    except Exception as e:
        print(f"Ошибка получения схемы: {e}")

if __name__ == "__main__":
    debug_frontend_subscription()
