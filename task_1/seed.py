import psycopg2
from faker import Faker

# Ініціалізація Faker
fake = Faker()

# Параметри підключення до PostgreSQL
conn = psycopg2.connect(
    host="localhost",  # Якщо база знаходиться в контейнері, вкажіть відповідну адресу контейнера
    database="hw03",
    user="postgres",
    password="postgres"
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
        user_id = fake.random_element(user_ids)  # Випадковий користувач
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
