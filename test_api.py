#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест API для проверки регистрации
"""

import requests
import json

def test_registration():
    """Тест регистрации пользователя"""
    
    url = "https://disciplined-cat-production.up.railway.app/api/v1/auth/register"
    
    data = {
        "email": "test@example.com",
        "password": "password123",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Отправляем запрос на: {url}")
    print(f"Данные: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.text}")
        
        if response.status_code == 200:
            print("✅ Регистрация успешна!")
        else:
            print("❌ Ошибка регистрации!")
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

if __name__ == "__main__":
    test_registration()
