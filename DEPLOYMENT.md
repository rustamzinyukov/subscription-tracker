# 🚂 Railway Deployment Guide

Полное руководство по развертыванию Subscription Tracker на Railway.

## 📋 Предварительные требования

- [Railway аккаунт](https://railway.app)
- [Railway CLI](https://docs.railway.app/develop/cli)
- [Docker](https://www.docker.com) (для локальной разработки)
- [Git](https://git-scm.com)

## 🚀 Быстрое развертывание

### 1. Установка Railway CLI

```bash
npm install -g @railway/cli
```

### 2. Автоматическая настройка

```bash
# Клонируйте репозиторий
git clone <your-repo-url>
cd subscription-tracker

# Запустите автоматическую настройку
make railway-setup
```

### 3. Развертывание

```bash
make railway-deploy
```

## 🔧 Ручная настройка

### 1. Создание проекта

```bash
# Войдите в Railway
railway login

# Создайте новый проект
railway init

# Свяжите с существующим репозиторием
railway link
```

### 2. Настройка базы данных

```bash
# Добавьте PostgreSQL
railway add postgresql

# Получите URL базы данных
railway variables get DATABASE_URL
```

### 3. Переменные окружения

```bash
# Основные настройки
railway variables set ENVIRONMENT=production
railway variables set DEBUG=false
railway variables set LOG_LEVEL=INFO

# Безопасность
railway variables set SECRET_KEY=$(openssl rand -hex 32)
railway variables set JWT_SECRET_KEY=$(openssl rand -hex 32)
railway variables set TELEGRAM_WEBHOOK_SECRET=$(openssl rand -hex 32)

# Telegram Bot (получите токен от @BotFather)
railway variables set TELEGRAM_BOT_TOKEN=your-bot-token-here

# CORS (замените на ваш домен)
railway variables set CORS_ORIGINS=https://your-app.railway.app
```

### 4. Развертывание

```bash
# Разверните приложение
railway up

# Получите URL приложения
railway domain
```

## 🤖 Настройка Telegram бота

### 1. Создание бота

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям для создания бота
4. Сохраните полученный токен

### 2. Настройка webhook

```bash
# Получите URL вашего приложения
APP_URL=$(railway domain)

# Установите webhook
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://$APP_URL/api/v1/telegram/webhook\"}"
```

### 3. Проверка webhook

```bash
# Проверьте статус webhook
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

## 🐳 Docker развертывание

### Локальная разработка

```bash
# Запустите все сервисы
make docker-up

# Инициализируйте базу данных
make docker-init

# Остановите сервисы
make docker-down
```

### Ручной запуск

```bash
# Соберите образ
docker build -t subscription-tracker .

# Запустите с переменными окружения
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SECRET_KEY=your-secret-key \
  subscription-tracker
```

## 📊 Мониторинг и логи

### Railway Dashboard

1. Откройте [Railway Dashboard](https://railway.app/dashboard)
2. Выберите ваш проект
3. Перейдите в раздел "Deployments"
4. Просматривайте логи в реальном времени

### Локальные логи

```bash
# Просмотр логов Railway
railway logs

# Просмотр логов Docker
docker-compose logs -f backend
```

## 🔧 Переменные окружения

### Обязательные переменные

```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

### Опциональные переменные

```env
# API настройки
API_V1_STR=/api/v1
PROJECT_NAME=Subscription Tracker
VERSION=1.0.0

# CORS
CORS_ORIGINS=https://your-domain.com

# Уведомления
NOTIFICATION_ENABLED=true
NOTIFICATION_TIMEZONE=Europe/Moscow

# Премиум функции
FREE_TIER_MAX_SUBSCRIPTIONS=5
PREMIUM_PRICE_MONTHLY=4.99
PREMIUM_PRICE_YEARLY=49.99

# Мониторинг
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
```

## 🚨 Устранение неполадок

### Проблемы с базой данных

```bash
# Проверьте подключение к БД
railway run python -c "from app.core.database import engine; print('DB connected:', engine.url)"

# Инициализируйте БД
railway run python init_db.py
```

### Проблемы с Telegram webhook

```bash
# Проверьте статус webhook
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"

# Удалите webhook
curl -X POST "https://api.telegram.org/bot<TOKEN>/deleteWebhook"

# Установите заново
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d "url=https://your-app.railway.app/api/v1/telegram/webhook"
```

### Проблемы с CORS

```bash
# Проверьте CORS настройки
railway variables get CORS_ORIGINS

# Обновите CORS
railway variables set CORS_ORIGINS=https://your-frontend-domain.com
```

## 📈 Масштабирование

### Автоматическое масштабирование

Railway автоматически масштабирует ваше приложение на основе нагрузки.

### Мониторинг производительности

1. **Railway Metrics**: Встроенные метрики в dashboard
2. **Sentry**: Отслеживание ошибок
3. **Custom Metrics**: Добавьте свои метрики в код

### Оптимизация

```python
# Добавьте в app/main.py
from prometheus_client import Counter, Histogram, generate_latest

# Метрики
REQUEST_COUNT = Counter('requests_total', 'Total requests')
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    REQUEST_COUNT.inc()
    REQUEST_DURATION.observe(process_time)
    
    return response
```

## 🔒 Безопасность

### SSL/TLS

Railway автоматически предоставляет SSL сертификаты.

### Переменные окружения

Никогда не коммитьте секреты в Git:

```bash
# Добавьте в .gitignore
.env
.env.local
.env.production

# Используйте Railway variables
railway variables set SECRET_KEY=your-secret
```

### Rate Limiting

```python
# Добавьте в app/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/v1/subscriptions/")
@limiter.limit("10/minute")
def get_subscriptions(request: Request, ...):
    # Ваш код
```

## 📞 Поддержка

- [Railway Documentation](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [GitHub Issues](https://github.com/your-repo/issues)

## 🎉 Готово!

Ваше приложение развернуто на Railway! 

- **API**: `https://your-app.railway.app`
- **Docs**: `https://your-app.railway.app/docs`
- **Health**: `https://your-app.railway.app/health`
