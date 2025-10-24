#!/usr/bin/env python3
"""
Проверяем подписки в базе данных
"""

import requests
import json

# API endpoints
BASE_URL = "https://disciplined-cat-production.up.railway.app"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
SUBSCRIPTION_URL = f"{BASE_URL}/api/v1/subscriptions"

def check_subscriptions():
    """Проверяем подписки"""
    
    print("Проверяем подписки в базе данных...")
    
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
    
    # 2. Получаем все подписки
    try:
        response = requests.get(SUBSCRIPTION_URL, headers=headers)
        print(f"Статус получения подписок: {response.status_code}")
        
        if response.status_code == 200:
            subscriptions = response.json()
            items = subscriptions.get('items', [])
            print(f"Всего подписок: {len(items)}")
            
            for sub in items:
                print(f"\n--- {sub['name']} ---")
                print(f"  Тип: {sub['subscription_type']}")
                print(f"  Частота: {sub['frequency']}")
                print(f"  Сумма: {sub['amount']} {sub['currency']}")
                print(f"  Следующий платеж: {sub.get('next_billing_date', 'NULL')}")
                print(f"  Дата начала: {sub.get('start_date', 'NULL')}")
                print(f"  Дата окончания: {sub.get('end_date', 'NULL')}")
                print(f"  Пробный период: {sub.get('has_trial', False)}")
                if sub.get('has_trial'):
                    print(f"    Начало пробного периода: {sub.get('trial_start_date', 'NULL')}")
                    print(f"    Конец пробного периода: {sub.get('trial_end_date', 'NULL')}")
                print(f"  Активна: {sub['is_active']}")
                print(f"  Категория: {sub.get('category', 'N/A')}")
                
        else:
            print(f"Ошибка получения подписок: {response.text}")
    except Exception as e:
        print(f"Ошибка при получении подписок: {e}")

if __name__ == "__main__":
    check_subscriptions()
