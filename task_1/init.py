import os
import psycopg2

# Отримуємо параметри підключення з змінних середовища або використовуємо значення за замовчуванням
db_host = os.getenv('POSTGRES_HOST', 'localhost')
db_name = os.getenv('POSTGRES_DB', 'hw03')
db_user = os.getenv('POSTGRES_USER', 'postgres')
db_password = os.getenv('POSTGRES_PASSWORD', 'postgres')

# Параметри підключення до PostgreSQL
conn = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)

# Створення курсора для виконання SQL-запитів
cur = conn.cursor()

# Створюємо таблицю users
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);
"""
cur.execute(create_users_table)

# Створюємо таблицю status
create_status_table = """
CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);
"""
cur.execute(create_status_table)

# Додаємо початкові записи у таблицю status
insert_statuses = """
INSERT INTO status (name)
VALUES
    ('new'),
    ('in progress'),
    ('completed')
ON CONFLICT (name) DO NOTHING;
"""
cur.execute(insert_statuses)

# Створюємо таблицю tasks з каскадним видаленням для зовнішнього ключа user_id
create_tasks_table = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER REFERENCES status(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
"""
cur.execute(create_tasks_table)

# Фіксуємо зміни у базі даних
conn.commit()

# Закриваємо курсор і підключення
cur.close()
conn.close()

print("Ініціалізація бази даних завершена успішно.")
