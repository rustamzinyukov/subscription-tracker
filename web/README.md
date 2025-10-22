# Subscription Tracker Web

Современное веб-приложение для управления подписками, построенное на Next.js 14 с TypeScript и Tailwind CSS.

## 🚀 Возможности

- **Управление подписками**: Добавление, редактирование, удаление подписок
- **Аналитика**: Детальная статистика расходов и подписок
- **Уведомления**: Отслеживание предстоящих платежей
- **Аутентификация**: JWT-авторизация с поддержкой Telegram
- **Адаптивный дизайн**: Работает на всех устройствах
- **Темная тема**: Поддержка темной темы (в разработке)

## 🛠 Технологии

- **Next.js 14** - React фреймворк с App Router
- **TypeScript** - Типизированный JavaScript
- **Tailwind CSS** - Utility-first CSS фреймворк
- **Axios** - HTTP клиент для API запросов
- **React Hooks** - Управление состоянием

## 📦 Установка

1. Установите зависимости:
```bash
npm install
```

2. Создайте файл `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Запустите приложение:
```bash
npm run dev
```

Приложение будет доступно по адресу `http://localhost:3000`

## 🏗 Структура проекта

```
web/
├── app/                    # App Router (Next.js 14)
│   ├── globals.css        # Глобальные стили
│   ├── layout.tsx         # Корневой layout
│   ├── page.tsx           # Главная страница
│   ├── login/             # Страница входа
│   └── analytics/         # Страница аналитики
├── components/            # React компоненты
│   ├── Header.tsx         # Шапка приложения
│   ├── SubscriptionCard.tsx # Карточка подписки
│   ├── AddSubscriptionButton.tsx # Кнопка добавления
│   ├── StatsCard.tsx     # Карточка статистики
│   └── UpcomingBills.tsx  # Предстоящие платежи
├── lib/                   # Утилиты и API клиент
│   ├── api.ts            # API клиент
│   └── utils.ts          # Вспомогательные функции
├── types/                # TypeScript типы
│   └── index.ts         # Основные типы
└── public/              # Статические файлы
```

## 🎨 Дизайн система

### Цвета
- **Primary**: Синий (#3b82f6)
- **Secondary**: Серый (#64748b)
- **Success**: Зеленый (#10b981)
- **Warning**: Желтый (#f59e0b)
- **Error**: Красный (#ef4444)

### Компоненты
- **Cards**: Закругленные карточки с тенью
- **Buttons**: Кнопки с hover эффектами
- **Forms**: Стилизованные формы ввода
- **Navigation**: Адаптивная навигация

## 🔧 API интеграция

Приложение интегрируется с FastAPI бэкендом через следующие endpoints:

- `POST /api/v1/auth/login` - Вход в систему
- `POST /api/v1/auth/register` - Регистрация
- `GET /api/v1/auth/me` - Текущий пользователь
- `GET /api/v1/subscriptions/` - Список подписок
- `POST /api/v1/subscriptions/` - Создание подписки
- `PUT /api/v1/subscriptions/{id}` - Обновление подписки
- `DELETE /api/v1/subscriptions/{id}` - Удаление подписки
- `GET /api/v1/analytics/monthly` - Месячная аналитика
- `GET /api/v1/analytics/yearly` - Годовая аналитика

## 📱 Адаптивность

Приложение полностью адаптивно и работает на:
- 📱 Мобильных устройствах (320px+)
- 📱 Планшетах (768px+)
- 💻 Десктопах (1024px+)
- 🖥 Больших экранах (1280px+)

## 🚀 Развертывание

### Vercel (рекомендуется)
1. Подключите репозиторий к Vercel
2. Установите переменные окружения
3. Деплой автоматически

### Docker
```bash
docker build -t subscription-tracker-web .
docker run -p 3000:3000 subscription-tracker-web
```

### Статический экспорт
```bash
npm run build
npm run export
```

## 🔐 Безопасность

- JWT токены хранятся в localStorage
- Автоматический редирект при истечении токена
- Валидация данных на клиенте и сервере
- HTTPS в продакшене

## 🧪 Тестирование

```bash
# Запуск тестов
npm test

# Запуск тестов с покрытием
npm run test:coverage

# E2E тесты
npm run test:e2e
```

## 📈 Производительность

- **Lighthouse Score**: 95+
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте feature ветку
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License - см. файл LICENSE для деталей.

## 📞 Поддержка

Если у вас есть вопросы или проблемы:
- Создайте Issue в GitHub
- Напишите в Telegram: @subscription_tracker_bot
- Email: support@subscription-tracker.com
