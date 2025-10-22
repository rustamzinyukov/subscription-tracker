# Subscription Tracker

Многоплатформенный сервис для управления подписками: Web, Flutter (iOS/Android/Web), Telegram Bot.

## 🚀 Быстрый старт (Updated for Railway)

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
subscription-tracker/
├── backend/                    # Backend API (FastAPI)
│   ├── app/                   # Основное приложение
│   │   ├── core/              # Основные модули
│   │   │   ├── auth.py        # Аутентификация JWT
│   │   │   └── database.py    # Конфигурация БД
│   │   ├── models/            # Модели данных
│   │   │   └── database.py    # SQLAlchemy модели
│   │   ├── schemas/           # Pydantic схемы
│   │   │   └── schemas.py     # API схемы
│   │   ├── routers/           # API роутеры
│   │   │   ├── auth.py        # Аутентификация
│   │   │   ├── subscriptions.py # Подписки
│   │   │   ├── analytics.py   # Аналитика
│   │   │   └── telegram.py    # Telegram бот
│   │   ├── services/          # Бизнес-логика
│   │   ├── utils/             # Утилиты
│   │   └── main.py            # Главный файл
│   ├── migrations/            # Миграции БД
│   ├── tests/                 # Тесты
│   ├── requirements.txt       # Python зависимости
│   ├── .env.example          # Переменные окружения
│   ├── run.py               # Запуск сервера
│   └── init_db.py           # Инициализация БД
├── web/                       # Web frontend (Next.js)
│   └── package.json
├── mobile/                    # Mobile app (Flutter)
│   └── pubspec.yaml
├── telegram/                  # Telegram bot
├── docs/                      # Документация
│   └── erd.md
├── scripts/                   # Скрипты развертывания
│   ├── deploy.sh
│   └── setup-railway.sh
├── docker-compose.yml         # Docker Compose
├── Dockerfile                 # Docker образ
├── Makefile                  # Команды разработки
├── railway.json              # Railway конфигурация
├── railway.toml              # Railway настройки
├── Procfile                  # Heroku/Railway процесс
└── README.md                 # Документация
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

## 🚂 Развертывание на Railway

### Быстрый старт

1. **Установите Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Настройте проект**:
   ```bash
   make railway-setup
   ```

3. **Разверните приложение**:
   ```bash
   make railway-deploy
   ```

### Ручная настройка

1. **Создайте проект на Railway**:
   ```bash
   railway login
   railway init
   ```

2. **Добавьте PostgreSQL**:
   ```bash
   railway add postgresql
   ```

3. **Установите переменные окружения**:
   ```bash
   railway variables set SECRET_KEY=$(openssl rand -hex 32)
   railway variables set JWT_SECRET_KEY=$(openssl rand -hex 32)
   railway variables set TELEGRAM_BOT_TOKEN=your-bot-token
   ```

4. **Разверните**:
   ```bash
   railway up
   ```

### Docker развертывание

```bash
# Локальная разработка
make docker-up

# Инициализация базы данных
make docker-init

# Остановка
make docker-down
```

## 🚀 Следующие шаги

1. **Настройте Telegram бота**:
   - Зарегистрируйте бота через @BotFather
   - Получите токен и добавьте в Railway variables
   - Настройте webhook: `https://your-app.railway.app/api/v1/telegram/webhook`

2. **Мониторинг**:
   - Railway автоматически предоставляет логи
   - Настройте Sentry для отслеживания ошибок
   - Добавьте метрики производительности

3. **Масштабирование**:
   - Railway автоматически масштабирует приложение
   - Настройте Redis для кэширования
   - Добавьте CDN для статических файлов

## 📝 Лицензия

MIT License - см. файл LICENSE для деталей.