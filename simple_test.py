#!/usr/bin/env python3
"""
Простой тест без эмодзи
"""

import requests
import json

# API endpoints
BASE_URL = "https://disciplined-cat-production.up.railway.app"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
SUBSCRIPTION_URL = f"{BASE_URL}/api/v1/subscriptions"

def simple_test():
    """Простой тест"""
    
    print("Тестируем создание подписки...")
    
    # 1. Входим в систему
    login_data = {
        "email": "test_subscription@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        print(f"Статус входа: {response.status_code}")
        
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
    
    # 2. Создаем one_time подписку БЕЗ next_billing_date
    one_time_data = {
        "name": "Test One Time",
        "amount": 100.0,
        "currency": "RUB",
        "frequency": "one_time",
        "subscription_type": "one_time",
        "start_date": "2025-10-24"  # Добавляем start_date!
    }
    
    print(f"Данные: {json.dumps(one_time_data, indent=2)}")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(SUBSCRIPTION_URL, json=one_time_data, headers=headers)
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.text}")
        
        if response.status_code == 200:
            print("Успешно!")
        else:
            print("Ошибка!")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    simple_test()
