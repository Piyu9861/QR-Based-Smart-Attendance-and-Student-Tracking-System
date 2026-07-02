import mysql.connector
from mysql.connector import Error

# ── DB SETTINGS — change password if needed ──────────────────
DB_HOST     = '127.0.0.1'
DB_USER     = 'root'
DB_PASSWORD = ''           # ← put your MySQL password here if set
DB_NAME     = 'qr_attendance_db'
DB_PORT     = 3306

def get_db_connection():
    """Returns a fresh MySQL connection. Called per request."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            charset='utf8mb4',
            autocommit=False,          # manual commit — rollback on error
            connection_timeout=30,
            use_pure=True,             # pure Python driver — avoids C-ext issues
            raise_on_warnings=False    # suppress non-fatal warnings
        )
        return conn
    except Error as e:
        raise Exception(
            f"❌ Database connection failed: {e}\n"
            f"Check: MySQL running? DB '{DB_NAME}' exists? Password correct?\n"
            f"Run: mysql -u {DB_USER} -p < qr_attendance_db_FINAL.sql"
        )
