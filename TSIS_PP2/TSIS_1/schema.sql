-- Таблица категорий
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Обновление основной таблицы
ALTER TABLE phonebook 
    ADD COLUMN IF NOT EXISTS email VARCHAR(100),
    ADD COLUMN IF NOT EXISTS birthday DATE,
    ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id);

-- Таблица для нескольких телефонов
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES phonebook(user_id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);