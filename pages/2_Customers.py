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