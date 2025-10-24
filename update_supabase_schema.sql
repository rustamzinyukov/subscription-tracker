-- Обновление схемы Supabase для поддержки nullable next_billing_date
-- Выполните эти команды в Supabase SQL Editor

-- 1. Делаем next_billing_date nullable для one_time подписок
ALTER TABLE subscriptions ALTER COLUMN next_billing_date DROP NOT NULL;

-- 2. Проверяем текущую схему
SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default
FROM information_schema.columns 
WHERE table_name = 'subscriptions' 
AND column_name IN ('next_billing_date', 'frequency', 'subscription_type')
ORDER BY ordinal_position;

-- 3. Проверяем существующие данные
SELECT 
    id, 
    name, 
    subscription_type, 
    frequency, 
    next_billing_date,
    start_date,
    end_date
FROM subscriptions 
ORDER BY id;
