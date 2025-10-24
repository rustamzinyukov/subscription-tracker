-- Исправление схемы Supabase
-- Выполните эти команды в Supabase SQL Editor

-- 1. Удаляем лишнее поле password_hash (если существует)
ALTER TABLE users DROP COLUMN IF EXISTS password_hash;

-- 2. Добавляем недостающие поля для users
ALTER TABLE users ADD COLUMN IF NOT EXISTS first_name VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_name VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP WITH TIME ZONE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS timezone VARCHAR(255) DEFAULT 'Europe/Moscow';
ALTER TABLE users ADD COLUMN IF NOT EXISTS language VARCHAR(255) DEFAULT 'ru';

-- 3. Проверяем схему users
SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;

-- 4. Проверяем схему subscriptions
SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default
FROM information_schema.columns 
WHERE table_name = 'subscriptions' 
ORDER BY ordinal_position;

-- 5. Статистика данных
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'subscriptions' as table_name, COUNT(*) as count FROM subscriptions;
