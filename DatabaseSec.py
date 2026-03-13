import sqlite3
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv  # For secure credential storage (install with `pip install python-dotenv`)

# Load credentials from .env file (NEVER hardcode in code!)
load_dotenv()

# ------------------------------
# 1. SQLite Example (with parameterized queries)
# ------------------------------
def sqlite_secure_example():
    # Connect to SQLite DB (file-based; use :memory: for temp DB)
    conn = sqlite3.connect("secure_db.sqlite")
    cursor = conn.cursor()

    try:
        # Create table with limited permissions (SQLite uses file system permissions)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)

        # SAFE: Parameterized query (prevents SQL injection)
        user_data = ("jane_doe", "jane@example.com")
        cursor.execute("INSERT OR IGNORE INTO users (username, email) VALUES (?, ?)", user_data)

        # UNSAFE: String formatting (vulnerable to SQL injection - DO NOT USE!)
        # unsafe_query = f"INSERT INTO users VALUES ('{malicious_input}')"

        conn.commit()
        print("SQLite operation completed securely")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        conn.rollback()
    finally:
        # Always close connections to prevent leaks
        cursor.close()
        conn.close()

# ------------------------------
# 2. PostgreSQL Example (encrypted connection + least privilege)
# ------------------------------
def postgres_secure_example():
    # Secure connection parameters (use SSL for encryption)
    conn_params = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),  # User with ONLY necessary permissions (e.g., no DROP access)
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "sslmode": "require"  # Enforce encrypted connection
    }

    conn = None
    try:
        # Connect with SSL
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # SAFE: Parameterized query using psycopg2.sql module
        table_name = sql.Identifier("users")
        columns = sql.SQL(", ").join([sql.Identifier("username"), sql.Identifier("email")])
        values = sql.SQL("(%s, %s)")

        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES {}").format(
            table_name, columns, values
        )

        user_data = ("john_smith", "john@example.com")
        cursor.execute(insert_query, user_data)

        conn.commit()
        print("PostgreSQL operation completed securely")

    except psycopg2.Error as e:
        print(f"PostgreSQL error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()

# Example usage
if __name__ == "__main__":
    sqlite_secure_example()
    postgres_secure_example()
