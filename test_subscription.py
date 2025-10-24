#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест API для проверки создания подписки
"""

import requests
import json
from datetime import date, timedelta

def test_create_subscription():
    """Тест создания подписки"""
    
    # Сначала регистрируемся
    register_url = "https://disciplined-cat-production.up.railway.app/api/v1/auth/register"
    register_data = {
        "email": "test2@example.com",
        "password": "password123",
        "username": "testuser2",
        "first_name": "Test",
        "last_name": "User"
    }
    
    print("Регистрируем пользователя...")
    register_response = requests.post(register_url, json=register_data)
    
    if register_response.status_code != 200:
        print(f"Ошибка регистрации: {register_response.status_code}")
        print(register_response.text)
        return
    
    token = register_response.json()["access_token"]
    print(f"Получен токен: {token[:20]}...")
    
    # Теперь создаем подписку
    subscription_url = "https://disciplined-cat-production.up.railway.app/api/v1/subscriptions"
    subscription_data = {
        "name": "Netflix",
        "description": "Streaming service",
        "amount": 999.0,
        "currency": "RUB",
        "next_billing_date": (date.today() + timedelta(days=30)).isoformat(),
        "frequency": "monthly",
        "subscription_type": "recurring",
        "interval_unit": "month",
        "interval_count": 1,
        "has_trial": False,
        "category": "Entertainment",
        "provider": "Netflix"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    print(f"Создаем подписку...")
    print(f"Данные: {json.dumps(subscription_data, indent=2)}")
    
    try:
        response = requests.post(subscription_url, json=subscription_data, headers=headers)
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.text}")
        
        if response.status_code == 200:
            print("Подписка создана успешно!")
        else:
            print("Ошибка создания подписки!")
            
    except Exception as e:
        print(f"Ошибка запроса: {e}")

if __name__ == "__main__":
    test_create_subscription()
