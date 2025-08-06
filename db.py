import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            chat_id BIGINT UNIQUE NOT NULL,
            first_name TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_user(chat_id, name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (chat_id, first_name)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING;
    """, (chat_id, name))
    conn.commit()
    cur.close()
    conn.close()

def get_all_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT chat_id FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

