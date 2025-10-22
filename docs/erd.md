# ER-диаграмма базы данных

## Таблицы:

### `users`
- id (PK)
- telegram_id (UNIQUE, nullable)
- email (UNIQUE, nullable)
- is_premium (bool)

### `subscriptions`
- id (PK)
- user_id (FK → users.id)
- name (str)
- amount (float)
- currency (str, default=RUB)
- next_billing_date (date)
- frequency (enum: daily/weekly/monthly/yearly)
- is_active (bool)
- category (str, nullable)

### `notifications`
- id (PK)
- subscription_id (FK)
- scheduled_at (datetime)
- sent (bool)
- channel (enum: telegram/email/push)

---
Связи: один пользователь → много подписок → много уведомлений.