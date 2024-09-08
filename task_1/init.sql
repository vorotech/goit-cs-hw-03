-- Створюємо таблицю users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- Створюємо таблицю status
CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Додаємо початкові записи у таблицю status
INSERT INTO status (name) VALUES ('new'), ('in progress'), ('completed');

-- Створюємо таблицю tasks з каскадним видаленням для зовнішнього ключа user_id
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER REFERENCES status(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
