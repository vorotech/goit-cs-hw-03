import psycopg2
import pandas as pd
import io
import os

# Get connection parameters from environment variables or use default values
db_host = os.getenv("POSTGRES_HOST", "localhost")
db_name = os.getenv("POSTGRES_DB", "hw03")
db_user = os.getenv("POSTGRES_USER", "postgres")
db_password = os.getenv("POSTGRES_PASSWORD", "postgres")


def get_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=db_host, database=db_name, user=db_user, password=db_password
    )


def get_user_by_task_id(task_id):
    """Retrieve the user assigned to a specific task."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT users.id, users.fullname, users.email
                FROM tasks
                JOIN users ON tasks.user_id = users.id
                WHERE tasks.id = %s;
            """,
                (task_id,),
            )
            return cur.fetchone()


def get_tasks_by_user(user_id):
    """Retrieve all tasks assigned to a specific user."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT tasks.id, tasks.title, tasks.description, status.name AS status
                FROM tasks
                JOIN status ON tasks.status_id = status.id
                WHERE tasks.user_id = %s;
            """,
                (user_id,),
            )
            return cur.fetchall()


def get_tasks_by_status(status_name):
    """Retrieve all tasks with a specific status."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT tasks.id, tasks.title, tasks.description, status.name AS status
                FROM tasks
                JOIN status ON tasks.status_id = status.id
                WHERE tasks.status_id = (SELECT id FROM status WHERE name = %s);
            """,
                (status_name,),
            )
            return cur.fetchall()


def update_task_status(task_id, new_status_name):
    """Update the status of a specific task."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET status_id = (SELECT id FROM status WHERE name = %s)
                WHERE id = %s;
            """,
                (new_status_name, task_id),
            )
            conn.commit()


def get_users_without_tasks():
    """Retrieve all users who do not have any tasks assigned."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, fullname, email
                FROM users
                WHERE id NOT IN (SELECT user_id FROM tasks);
            """)
            return cur.fetchall()


def add_new_task_for_user(title, description, status_name, user_id):
    """Add a new task for a specific user."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tasks (title, description, status_id, user_id)
                VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s);
            """,
                (title, description, status_name, user_id),
            )
            conn.commit()


def get_incomplete_tasks():
    """Retrieve all tasks that are not marked as completed."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT tasks.id, tasks.title, tasks.description, status.name AS status
                FROM tasks
                JOIN status ON tasks.status_id = status.id
                WHERE status.name != 'completed';
            """)
            return cur.fetchall()


def delete_task_by_id(task_id):
    """Delete a specific task by its ID."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM tasks
                WHERE id = %s;
            """,
                (task_id,),
            )
            conn.commit()


def find_users_by_email_pattern(email_pattern):
    """Find users whose email matches a specific pattern."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, fullname, email
                FROM users
                WHERE email LIKE %s;
            """,
                (email_pattern,),
            )
            return cur.fetchall()


def update_user_fullname(user_id, new_fullname):
    """Update the fullname of a specific user."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET fullname = %s
                WHERE id = %s;
            """,
                (new_fullname, user_id),
            )
            conn.commit()


def get_task_count_by_status():
    """Retrieve the count of tasks for each status."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT status.name AS status, COUNT(tasks.id) AS task_count
                FROM tasks
                JOIN status ON tasks.status_id = status.id
                GROUP BY status.name;
            """)
            return cur.fetchall()


def get_tasks_for_users_with_email_domain(domain):
    """Retrieve tasks assigned to users with a specific email domain."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT tasks.id, tasks.title, tasks.description, users.fullname, users.email, status.name AS status
                FROM tasks
                JOIN users ON tasks.user_id = users.id
                JOIN status ON tasks.status_id = status.id
                WHERE users.email LIKE %s;
            """,
                (f"%{domain}",),
            )
            return cur.fetchall()


def get_tasks_without_description():
    """Retrieve all tasks that do not have a description."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, user_id, status_id
                FROM tasks
                WHERE description IS NULL OR description = '';
            """)
            return cur.fetchall()


def get_users_with_tasks_in_progress():
    """Retrieve users and their tasks that are marked as 'in progress'."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT users.id AS user_id, users.fullname, tasks.id AS task_id, tasks.title, tasks.description, status.name AS status
                FROM tasks
                INNER JOIN users ON tasks.user_id = users.id
                INNER JOIN status ON tasks.status_id = status.id
                WHERE status.name = 'in progress';
            """)
            return cur.fetchall()


def get_users_and_task_count():
    """Retrieve users and the count of their tasks."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT users.id AS user_id, users.fullname, users.email, COUNT(tasks.id) AS task_count
                FROM users
                LEFT JOIN tasks ON users.id = tasks.user_id
                GROUP BY users.id, users.fullname, users.email;
            """)
            return cur.fetchall()


def main():
    """Main function to demonstrate the usage of the query functions with pandas."""

    # Create a string buffer to capture the output
    buffer = io.StringIO()

    buffer.write("1. Отримуємо всі завдання для конкретного користувача:")
    tasks = get_tasks_by_user(1)
    tasks_df = pd.DataFrame(
        tasks, columns=["Task ID", "Title", "Description", "Status"]
    )
    buffer.write(f"{tasks_df}\n\n")

    buffer.write("\n2. Вибираємо всі завдання з конкретним статусом 'new':")
    tasks_with_new_status = get_tasks_by_status("new")
    tasks_with_new_status_df = pd.DataFrame(
        tasks_with_new_status, columns=["Task ID", "Title", "Description", "Status"]
    )
    buffer.write(f"{tasks_with_new_status_df}\n\n")

    buffer.write("\n3. Оновлюємо статус конкретного завдання:")
    if not tasks_with_new_status_df.empty:
        task_id_to_update = int(
            tasks_with_new_status_df.iloc[0]["Task ID"]
        )  # Convert to int
        buffer.write(f"\nОновлюємо статус завдання із ID {task_id_to_update} в 'in progress'\n\n")
        update_task_status(task_id_to_update, "in progress")

    buffer.write("\n4. Вибираємо всіх користувачів, які не мають жодного завдання:")
    users_without_tasks = get_users_without_tasks()
    users_without_tasks_df = pd.DataFrame(
        users_without_tasks, columns=["User ID", "Fullname", "Email"]
    )
    buffer.write(f"{users_without_tasks_df}\n\n")

    buffer.write("\n5. Додаємо нове завдання для користувача:")
    if not users_without_tasks_df.empty:
        user_id = int(users_without_tasks_df.iloc[0]["User ID"])  # Convert to int
        add_new_task_for_user("Another Task", "", "in progress", user_id)
        buffer.write("\nЗавдання користувача після додавання нового:")
        user_tasks_df = pd.DataFrame(
            get_tasks_by_user(user_id),
            columns=["Task ID", "Title", "Description", "Status"],
        )
        buffer.write(f"{user_tasks_df}\n\n")

    buffer.write("\n6. Вибираємо всі завдання, які ще не завершено:")
    incomplete_tasks = get_incomplete_tasks()
    incomplete_tasks_df = pd.DataFrame(
        incomplete_tasks, columns=["Task ID", "Title", "Description", "Status"]
    )
    buffer.write(f"{incomplete_tasks_df}\n\n")

    buffer.write("\n7. Видаляємо конкретне завдання за його id:")
    if not incomplete_tasks_df.empty:
        task_id_to_delete = int(
            incomplete_tasks_df.iloc[0]["Task ID"]
        )  # Convert to int
        user_id = int(get_user_by_task_id(task_id_to_delete)[0])  # Convert to int
        buffer.write(f"\nВидалення завдання із ID {task_id_to_delete}")
        delete_task_by_id(task_id_to_delete)
        buffer.write("\nЗавдання користувача після видалення:")
        updated_user_tasks_df = pd.DataFrame(
            get_tasks_by_user(user_id),
            columns=["Task ID", "Title", "Description", "Status"],
        )
        buffer.write(f"{updated_user_tasks_df}\n\n")

    buffer.write("\n8. Знаходимо користувачів за електронною поштою з умовою LIKE:")
    users_by_email_df = pd.DataFrame(
        find_users_by_email_pattern("%@example.com%"),
        columns=["User ID", "Fullname", "Email"],
    )
    buffer.write(f"{users_by_email_df}\n\n")

    buffer.write("\n9. Оновлюємо ім'я користувача:")
    update_user_fullname(1, "John Doe")
    buffer.write("\nUser 1's name updated to 'John Doe'.")

    buffer.write("\n10. Отримуємо кількість завдань для кожного статусу:")
    task_count_status_df = pd.DataFrame(
        get_task_count_by_status(), columns=["Status", "Task Count"]
    )
    buffer.write(f"{task_count_status_df}\n\n")

    buffer.write(
        "\n11. Вибираємо завдання, призначені користувачам, чия електронна пошта містить '@example.com':"
    )
    tasks_with_email_domain_df = pd.DataFrame(
        get_tasks_for_users_with_email_domain("@example.com"),
        columns=["Task ID", "Title", "Description", "Fullname", "Email", "Status"],
    )
    buffer.write(f"{tasks_with_email_domain_df}\n\n")

    buffer.write("\n12. Вибираємо завдання, у яких відсутній опис:")
    tasks_without_description_df = pd.DataFrame(
        get_tasks_without_description(),
        columns=["Task ID", "Title", "User ID", "Status ID"],
    )
    buffer.write(f"{tasks_without_description_df}\n\n")

    buffer.write(
        "\n13. Вибираємо користувачів та їхні завдання, які знаходяться у статусі 'in progress':"
    )
    users_with_tasks_in_progress_df = pd.DataFrame(
        get_users_with_tasks_in_progress(),
        columns=["User ID", "Fullname", "Task ID", "Title", "Description", "Status"],
    )
    buffer.write(f"{users_with_tasks_in_progress_df}\n\n")

    buffer.write("\n14. Отримуємо користувачів та кількість їхніх завдань:")
    users_task_count_df = pd.DataFrame(
        get_users_and_task_count(),
        columns=["User ID", "Fullname", "Email", "Task Count"],
    )
    buffer.write(f"{users_task_count_df}\n\n")

    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(buffer.getvalue())

if __name__ == "__main__":
    main()
