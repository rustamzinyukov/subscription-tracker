#!/usr/bin/env python3
"""
Тест разных типов подписок
Проверяем, как сохраняются подписки с разными настройками
"""

import requests
import json
from datetime import date, timedelta

# API endpoints
BASE_URL = "https://disciplined-cat-production.up.railway.app"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
SUBSCRIPTION_URL = f"{BASE_URL}/api/v1/subscriptions"

def test_subscription_types():
    """Тестируем разные типы подписок"""
    
    print("Тестируем разные типы подписок...")
    
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
    
    # 2. Тест 1: One-time подписка (без автопродления)
    print("\n2. Тест 1: One-time подписка (без автопродления)")
    one_time_data = {
        "name": "Adobe Creative Suite - One Time",
        "description": "Одноразовая покупка лицензии",
        "amount": 5999.99,
        "currency": "RUB",
        "frequency": "one_time",
        "subscription_type": "one_time",
        "start_date": date.today().isoformat(),
        "duration_type": "indefinite",
        "category": "Software",
        "provider": "Adobe"
    }
    
    try:
        response = requests.post(SUBSCRIPTION_URL, json=one_time_data, headers=headers)
        print(f"Статус one-time подписки: {response.status_code}")
        
        if response.status_code == 200:
            subscription = response.json()
            print(f"Создана one-time подписка: {subscription['name']}")
            print(f"  - ID: {subscription['id']}")
            print(f"  - Тип: {subscription['subscription_type']}")
            print(f"  - Частота: {subscription['frequency']}")
            print(f"  - Следующий платеж: {subscription.get('next_billing_date', 'NULL')}")
            print(f"  - Активна: {subscription['is_active']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # 3. Тест 2: Recurring подписка с автопродлением
    print("\n3. Тест 2: Recurring подписка с автопродлением")
    next_month = date.today() + timedelta(days=30)
    recurring_data = {
        "name": "Netflix Premium - Recurring",
        "description": "Ежемесячная подписка с автопродлением",
        "amount": 999.99,
        "currency": "RUB",
        "next_billing_date": next_month.isoformat(),
        "frequency": "monthly",
        "subscription_type": "recurring",
        "interval_unit": "month",
        "interval_count": 1,
        "category": "Entertainment",
        "provider": "Netflix"
    }
    
    try:
        response = requests.post(SUBSCRIPTION_URL, json=recurring_data, headers=headers)
        print(f"Статус recurring подписки: {response.status_code}")
        
        if response.status_code == 200:
            subscription = response.json()
            print(f"Создана recurring подписка: {subscription['name']}")
            print(f"  - ID: {subscription['id']}")
            print(f"  - Тип: {subscription['subscription_type']}")
            print(f"  - Частота: {subscription['frequency']}")
            print(f"  - Следующий платеж: {subscription.get('next_billing_date', 'NULL')}")
            print(f"  - Активна: {subscription['is_active']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # 4. Тест 3: Recurring подписка с пробным периодом
    print("\n4. Тест 3: Recurring подписка с пробным периодом")
    trial_start = date.today()
    trial_end = date.today() + timedelta(days=7)
    next_payment = date.today() + timedelta(days=30)
    
    trial_data = {
        "name": "Spotify Premium - Trial",
        "description": "Подписка с пробным периодом",
        "amount": 499.99,
        "currency": "RUB",
        "next_billing_date": next_payment.isoformat(),
        "frequency": "monthly",
        "subscription_type": "recurring",
        "interval_unit": "month",
        "interval_count": 1,
        "has_trial": True,
        "trial_start_date": trial_start.isoformat(),
        "trial_end_date": trial_end.isoformat(),
        "category": "Entertainment",
        "provider": "Spotify"
    }
    
    try:
        response = requests.post(SUBSCRIPTION_URL, json=trial_data, headers=headers)
        print(f"Статус trial подписки: {response.status_code}")
        
        if response.status_code == 200:
            subscription = response.json()
            print(f"Создана trial подписка: {subscription['name']}")
            print(f"  - ID: {subscription['id']}")
            print(f"  - Тип: {subscription['subscription_type']}")
            print(f"  - Частота: {subscription['frequency']}")
            print(f"  - Пробный период: {subscription['has_trial']}")
            print(f"  - Начало пробного периода: {subscription.get('trial_start_date', 'NULL')}")
            print(f"  - Конец пробного периода: {subscription.get('trial_end_date', 'NULL')}")
            print(f"  - Следующий платеж: {subscription.get('next_billing_date', 'NULL')}")
            print(f"  - Активна: {subscription['is_active']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # 5. Получаем все подписки для анализа
    print("\n5. Анализ всех подписок...")
    
    try:
        response = requests.get(SUBSCRIPTION_URL, headers=headers)
        print(f"Статус получения подписок: {response.status_code}")
        
        if response.status_code == 200:
            subscriptions = response.json()
            items = subscriptions.get('items', [])
            print(f"Всего подписок: {len(items)}")
            
            # Анализируем типы подписок
            one_time_count = 0
            recurring_count = 0
            trial_count = 0
            active_count = 0
            
            for sub in items:
                if sub['subscription_type'] == 'one_time':
                    one_time_count += 1
                elif sub['subscription_type'] == 'recurring':
                    recurring_count += 1
                
                if sub.get('has_trial', False):
                    trial_count += 1
                
                if sub['is_active']:
                    active_count += 1
                
                print(f"  - {sub['name']} ({sub['subscription_type']}) - активна: {sub['is_active']}")
            
            print(f"\nСтатистика:")
            print(f"  - One-time подписок: {one_time_count}")
            print(f"  - Recurring подписок: {recurring_count}")
            print(f"  - С пробным периодом: {trial_count}")
            print(f"  - Активных: {active_count}")
            
        else:
            print(f"Ошибка получения подписок: {response.text}")
    except Exception as e:
        print(f"Ошибка при получении подписок: {e}")

if __name__ == "__main__":
    test_subscription_types()
