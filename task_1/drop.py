import psycopg2
import os

# Get connection parameters from environment variables or use default values
db_host = os.getenv('POSTGRES_HOST', 'localhost')
db_name = os.getenv('POSTGRES_DB', 'hw03')
db_user = os.getenv('POSTGRES_USER', 'postgres')
db_password = os.getenv('POSTGRES_PASSWORD', 'postgres')

def get_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )

def drop_tables():
    """Drop the users, tasks, and status tables if they exist."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Disable foreign key checks temporarily
            cur.execute("DROP TABLE IF EXISTS tasks CASCADE;")
            cur.execute("DROP TABLE IF EXISTS status CASCADE;")
            cur.execute("DROP TABLE IF EXISTS users CASCADE;")
            conn.commit()
            print("Tables 'tasks', 'status', and 'users' have been dropped.")

if __name__ == "__main__":
    drop_tables()
