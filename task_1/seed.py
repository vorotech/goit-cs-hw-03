import os
import psycopg2
from faker import Faker

# Ініціалізація Faker
fake = Faker()

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

# Генеруємо випадкових користувачів та додаємо їх у таблицю users
def seed_users(num_users):
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.unique.email()
        cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))
    conn.commit()

# Генеруємо випадкові завдання для користувачів
def seed_tasks(num_tasks):
    cur.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cur.fetchall()]  # Отримуємо список всіх id користувачів

    cur.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cur.fetchall()]  # Отримуємо список всіх статусів

    for _ in range(num_tasks):
        title = fake.sentence(nb_words=6)
        description = fake.text(max_nb_chars=200)
        status_id = fake.random_element(status_ids)  # Випадковий статус
        user_id = fake.random_element(user_ids[1:])  # Випадковий користувач (один буде без завдань)
        cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                    (title, description, status_id, user_id))
    conn.commit()

# Головна функція для запуску генерації даних
def seed_database():
    print("Seeding users...")
    seed_users(20)  # Генеруємо 20 користувачів

    print("Seeding tasks...")
    seed_tasks(50)  # Генеруємо 50 завдань

# Викликаємо функцію для заповнення бази
if __name__ == "__main__":
    seed_database()

# Закриваємо курсор і підключення
cur.close()
conn.close()
