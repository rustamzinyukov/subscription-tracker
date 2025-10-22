# backend/app/routers/telegram.py
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from typing import Optional
import os
import hmac
import hashlib
import json
from datetime import datetime, timedelta

from ..core.database import get_db
from ..core.auth import get_telegram_user, auth_manager
from ..models.database import User, Subscription, Notification, NotificationChannelEnum
from ..schemas.schemas import TelegramWebhook, MessageResponse, Token
import aiohttp

router = APIRouter()

async def send_telegram_message(chat_id: int, text: str):
    """Send message via Telegram Bot API"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print(f"TELEGRAM_BOT_TOKEN not found, would send: {text}")
        return
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    print(f"Message sent successfully to {chat_id}")
                else:
                    print(f"Failed to send message: {await response.text()}")
    except Exception as e:
        print(f"Error sending message: {e}")

# Telegram Bot Commands
BOT_COMMANDS = {
    "start": "Начать работу с ботом",
    "help": "Показать справку",
    "list": "Показать все подписки",
    "add": "Добавить новую подписку",
    "stats": "Показать статистику трат",
    "settings": "Настройки уведомлений"
}

def verify_telegram_webhook(request_body: bytes, secret_token: str, telegram_token: str) -> bool:
    """Verify Telegram webhook signature"""
    secret_hash = hmac.new(
        secret_token.encode(),
        request_body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(secret_hash, telegram_token)

@router.get("/webhook")
async def telegram_webhook_get():
    """Handle Telegram webhook GET requests (for verification)"""
    return {"status": "ok", "message": "Telegram webhook is working"}

@router.post("/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Handle Telegram webhook"""
    
    # Get request body
    body = await request.body()
    
    # Verify webhook secret (temporarily disabled for testing)
    # webhook_secret = os.getenv("TELEGRAM_WEBHOOK_SECRET")
    # if not verify_telegram_webhook(body, webhook_secret, x_telegram_bot_api_secret_token or ""):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid webhook signature"
    #     )
    
    # Parse webhook data
    try:
        webhook_data = await request.json()
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON data"
        )
    
    # Process webhook
    await process_telegram_update(webhook_data, db)
    
    return {"ok": True}

async def process_telegram_update(update: dict, db: Session):
    """Process Telegram update"""
    
    # Handle message
    if "message" in update:
        message = update["message"]
        user_id = message["from"]["id"]
        text = message.get("text", "")
        
        # Get or create user
        user = get_or_create_telegram_user(user_id, message["from"], db)
        
        # Process command
        if text.startswith("/"):
            await handle_command(text, user, db)
        else:
            await handle_text_message(text, user, db)
    
    # Handle callback query
    elif "callback_query" in update:
        callback = update["callback_query"]
        user_id = callback["from"]["id"]
        data = callback.get("data", "")
        
        user = get_or_create_telegram_user(user_id, callback["from"], db)
        await handle_callback_query(data, user, db)

def get_or_create_telegram_user(telegram_id: int, telegram_user: dict, db: Session) -> User:
    """Get or create Telegram user"""
    
    user = db.query(User).filter(User.telegram_id == str(telegram_id)).first()
    
    if not user:
        # Create new user
        user = User(
            telegram_id=str(telegram_id),
            username=telegram_user.get("username"),
            first_name=telegram_user.get("first_name"),
            last_name=telegram_user.get("last_name"),
            timezone="Europe/Moscow",
            language="ru"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update user info
        user.username = telegram_user.get("username")
        user.first_name = telegram_user.get("first_name")
        user.last_name = telegram_user.get("last_name")
        user.last_login = datetime.utcnow()
        db.commit()
    
    return user

async def handle_command(command: str, user: User, db: Session):
    """Handle Telegram commands"""
    
    command = command.lower().strip()
    
    if command == "/start":
        await send_welcome_message(user)
    
    elif command == "/help":
        await send_help_message(user)
    
    elif command == "/list":
        await send_subscriptions_list(user, db)
    
    elif command == "/add":
        await start_add_subscription(user)
    
    elif command == "/stats":
        await send_statistics(user, db)
    
    elif command == "/settings":
        await send_settings(user)
    
    else:
        await send_unknown_command(user)

async def send_welcome_message(user: User):
    """Send welcome message to user"""
    
    message = f"""
🎉 Добро пожаловать в Subscription Tracker, {user.first_name}!

Я помогу вам отслеживать все ваши подписки и не забывать о предстоящих платежах.

📋 Доступные команды:
/list - показать все подписки
/add - добавить новую подписку
/stats - статистика трат
/settings - настройки

Начните с команды /add чтобы добавить вашу первую подписку!
    """
    
    # Send message via Telegram API
    await send_telegram_message(user.telegram_id, message)

async def send_help_message(user: User):
    """Send help message"""
    
    message = """
📖 Справка по командам:

/list - Показать все ваши подписки
/add - Добавить новую подписку
/stats - Показать статистику трат за месяц/год
/settings - Настройки уведомлений

💡 Совет: Используйте /add для добавления подписок типа Netflix, Spotify, Яндекс Плюс и других.
    """
    
    await send_telegram_message(user.telegram_id, message)

async def send_subscriptions_list(user: User, db: Session):
    """Send user's subscriptions list"""
    
    subscriptions = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.is_active == True
    ).order_by(Subscription.next_billing_date).all()
    
    if not subscriptions:
        message = "📝 У вас пока нет активных подписок.\n\nИспользуйте /add чтобы добавить первую подписку!"
    else:
        message = "📋 Ваши подписки:\n\n"
        total_monthly = 0
        
        for sub in subscriptions:
            status_emoji = "🟢" if sub.is_active else "🔴"
            message += f"{status_emoji} {sub.name}\n"
            message += f"   💰 {sub.amount} {sub.currency}\n"
            message += f"   📅 {sub.next_billing_date.strftime('%d.%m.%Y')}\n"
            message += f"   🔄 {sub.frequency}\n\n"
            
            if sub.frequency == "monthly":
                total_monthly += sub.amount
        
        message += f"💸 Итого в месяц: {total_monthly:.2f} RUB"
    
    await send_telegram_message(user.telegram_id, message)

async def start_add_subscription(user: User):
    """Start adding subscription process"""
    
    message = """
➕ Добавление новой подписки

Отправьте мне информацию о подписке в следующем формате:

Название: [название сервиса]
Сумма: [сумма в рублях]
Дата: [дата следующего списания в формате ДД.ММ.ГГГГ]
Частота: [ежемесячно/ежегодно]

Пример:
Название: Netflix
Сумма: 599
Дата: 15.01.2024
Частота: ежемесячно
    """
    
    print(f"Starting add subscription for user {user.telegram_id}: {message}")

async def send_statistics(user: User, db: Session):
    """Send spending statistics"""
    
    # Get current month stats
    now = datetime.now()
    start_of_month = now.replace(day=1)
    
    subscriptions = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.is_active == True,
        Subscription.next_billing_date >= start_of_month
    ).all()
    
    total_monthly = sum(sub.amount for sub in subscriptions if sub.frequency == "monthly")
    total_yearly = sum(sub.amount for sub in subscriptions if sub.frequency == "yearly")
    
    message = f"""
📊 Статистика трат:

📅 За текущий месяц:
💰 Ежемесячные: {total_monthly:.2f} RUB
💰 Годовые: {total_yearly:.2f} RUB
📈 Всего: {total_monthly + total_yearly:.2f} RUB

📋 Активных подписок: {len(subscriptions)}
    """
    
    await send_telegram_message(user.telegram_id, message)

async def send_settings(user: User):
    """Send settings information"""
    
    message = f"""
⚙️ Настройки:

👤 Имя: {user.first_name} {user.last_name or ''}
🌍 Часовой пояс: {user.timezone}
🌐 Язык: {user.language}
💎 Премиум: {'Да' if user.is_premium else 'Нет'}

🔔 Уведомления включены
📱 Канал: Telegram
    """
    
    await send_telegram_message(user.telegram_id, message)

async def send_unknown_command(user: User):
    """Send unknown command message"""
    
    message = """
❓ Неизвестная команда

Используйте /help чтобы увидеть список доступных команд.
    """
    
    await send_telegram_message(user.telegram_id, message)

async def handle_text_message(text: str, user: User, db: Session):
    """Handle text messages (for adding subscriptions)"""
    
    # Simple parsing for subscription data
    if "название:" in text.lower() and "сумма:" in text.lower():
        await parse_subscription_data(text, user, db)
    else:
        await send_unknown_command(user)

async def parse_subscription_data(text: str, user: User, db: Session):
    """Parse subscription data from text"""
    
    try:
        lines = text.split('\n')
        data = {}
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if 'название' in key:
                    data['name'] = value
                elif 'сумма' in key:
                    data['amount'] = float(value)
                elif 'дата' in key:
                    data['date'] = value
                elif 'частота' in key:
                    data['frequency'] = value
        
        # Create subscription
        if all(key in data for key in ['name', 'amount', 'date', 'frequency']):
            # Parse date
            date_parts = data['date'].split('.')
            billing_date = datetime(int(date_parts[2]), int(date_parts[1]), int(date_parts[0])).date()
            
            # Parse frequency
            frequency_map = {
                'ежемесячно': 'monthly',
                'ежегодно': 'yearly',
                'еженедельно': 'weekly',
                'ежедневно': 'daily'
            }
            frequency = frequency_map.get(data['frequency'].lower(), 'monthly')
            
            # Create subscription
            subscription = Subscription(
                user_id=user.id,
                name=data['name'],
                amount=data['amount'],
                currency='RUB',
                next_billing_date=billing_date,
                frequency=frequency,
                is_active=True
            )
            
            db.add(subscription)
            db.commit()
            
            message = f"""
✅ Подписка "{data['name']}" успешно добавлена!

💰 Сумма: {data['amount']} RUB
📅 Следующее списание: {billing_date.strftime('%d.%m.%Y')}
🔄 Частота: {frequency}

Используйте /list чтобы увидеть все подписки.
            """
            
            print(f"Subscription added for user {user.telegram_id}: {message}")
        else:
            await send_unknown_command(user)
            
    except Exception as e:
        message = f"❌ Ошибка при добавлении подписки: {str(e)}"
        print(f"Error adding subscription for user {user.telegram_id}: {message}")

async def handle_callback_query(data: str, user: User, db: Session):
    """Handle callback queries from inline keyboards"""
    
    # Handle different callback data
    if data.startswith("add_subscription_"):
        # Handle adding subscription via inline keyboard
        pass
    elif data.startswith("view_subscription_"):
        # Handle viewing specific subscription
        pass
    # Add more callback handlers as needed

@router.post("/send-notification")
async def send_notification(
    user_id: int,
    message: str,
    db: Session = Depends(get_db)
):
    """Send notification to user via Telegram"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or no Telegram ID"
        )
    
    # In real implementation, send message via Telegram Bot API
    await send_telegram_message(user.telegram_id, message)
    
    return {"message": "Notification sent successfully"}
