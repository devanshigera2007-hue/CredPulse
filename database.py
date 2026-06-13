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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credit_transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        amount REAL,
        transaction_date TEXT,
        due_date TEXT,
        remarks TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        amount REAL,
        payment_date TEXT
    )
    """)

    conn.commit()
    conn.close()

create_tables()