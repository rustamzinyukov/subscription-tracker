# Subscription Tracker

Многоплатформенный сервис для управления подписками: Web, Flutter (iOS/Android/Web), Telegram Bot.

## 🚀 Быстрый старт

### 1. Настройка окружения

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd subscription-tracker

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r backendrequirements.txt
```

### 2. Настройка базы данных

```bash
# Создайте базу данных PostgreSQL
createdb subscription_tracker

# Скопируйте файл окружения
cp env.example .env

# Отредактируйте .env файл с вашими настройками
```

### 3. Инициализация базы данных

```bash
# Создайте таблицы и добавьте тестовые данные
python init_db.py
```

### 4. Запуск сервера

```bash
# Запустите backend сервер
python run_backend.py
```

Сервер будет доступен по адресу: http://localhost:8000
API документация: http://localhost:8000/docs

## 📋 Структура проекта

```
for_cursor/
├── backendappmain.py          # Главный файл FastAPI приложения
├── backendappmodels.py        # Модели базы данных SQLAlchemy
├── backendauth.py             # Система аутентификации JWT
├── backendschemas.py          # Pydantic схемы для API
├── backenddatabase.py         # Конфигурация базы данных
├── backendrouters/            # API роутеры
│   ├── auth.py               # Аутентификация
│   ├── subscriptions.py      # Управление подписками
│   ├── analytics.py          # Аналитика
│   └── telegram.py           # Telegram бот
├── backendrequirements.txt   # Python зависимости
├── env.example              # Пример переменных окружения
├── run_backend.py           # Скрипт запуска сервера
├── init_db.py              # Инициализация базы данных
└── README.md               # Документация
```

## 🔧 Конфигурация

### Переменные окружения (.env)

```env
# База данных
DATABASE_URL=postgresql://user:password@localhost:5432/subscription_tracker

# Безопасность
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_WEBHOOK_SECRET=your-webhook-secret

# API
API_V1_STR=/api/v1
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## 🛠️ API Endpoints

### Аутентификация
- `POST /api/v1/auth/register` - Регистрация пользователя
- `POST /api/v1/auth/login` - Вход в систему
- `POST /api/v1/auth/telegram-auth` - Аутентификация через Telegram
- `GET /api/v1/auth/me` - Информация о текущем пользователе

### Подписки
- `GET /api/v1/subscriptions/` - Список подписок
- `POST /api/v1/subscriptions/` - Создать подписку
- `GET /api/v1/subscriptions/{id}` - Получить подписку
- `PUT /api/v1/subscriptions/{id}` - Обновить подписку
- `DELETE /api/v1/subscriptions/{id}` - Удалить подписку

### Аналитика
- `GET /api/v1/analytics/monthly` - Месячная аналитика
- `GET /api/v1/analytics/yearly` - Годовая аналитика
- `GET /api/v1/analytics/trends/monthly` - Тренды по месяцам

### Telegram Bot
- `POST /api/v1/telegram/webhook` - Webhook для Telegram
- `POST /api/v1/telegram/send-notification` - Отправка уведомлений

## 🤖 Telegram Bot команды

- `/start` - Начать работу с ботом
- `/help` - Справка по командам
- `/list` - Показать все подписки
- `/add` - Добавить новую подписку
- `/stats` - Статистика трат
- `/settings` - Настройки

## 🔒 Безопасность

- JWT токены для аутентификации
- Валидация Telegram webhook с секретным токеном
- Хеширование паролей с bcrypt
- CORS настройки для безопасности
- Rate limiting для защиты от спама

## 📊 Модель данных

### Пользователи (Users)
- Базовая информация (имя, email, Telegram ID)
- Статус премиум подписки
- Настройки (часовой пояс, язык)

### Подписки (Subscriptions)
- Название и описание
- Сумма и валюта
- Дата следующего списания
- Частота (ежедневно/еженедельно/ежемесячно/ежегодно)
- Категория и провайдер

### Уведомления (Notifications)
- Запланированные напоминания
- Каналы доставки (Telegram/Email/Push)
- Статус отправки

## 🚀 Следующие шаги

1. **Настройте Telegram бота**:
   - Зарегистрируйте бота через @BotFather
   - Получите токен и добавьте в .env
   - Настройте webhook

2. **Развертывание**:
   - Настройте PostgreSQL на продакшене
   - Используйте Redis для кэширования
   - Настройте HTTPS для webhook

3. **Мониторинг**:
   - Добавьте логирование
   - Настройте мониторинг ошибок
   - Добавьте метрики производительности

## 📝 Лицензия

MIT License - см. файл LICENSE для деталей.