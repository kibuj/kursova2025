import sqlite3

conn = sqlite3.connect("bank_account.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS balance (
        id INTEGER PRIMARY KEY,
        owner TEXT NOT NULL,
        balance REAL NOT NULL,
        transactions TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
