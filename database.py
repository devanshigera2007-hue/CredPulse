import sqlite3

def create_tables():
    conn = sqlite3.connect("credpulse.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        credit_limit REAL
    )
    """)

    conn.commit()
    conn.close()

create_tables()