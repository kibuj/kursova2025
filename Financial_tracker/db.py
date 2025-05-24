import sqlite3

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS balance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        balance INTEGER NOT NULL,
        changes TEXT
    )
''')

conn.commit()
