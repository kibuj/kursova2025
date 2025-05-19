import sqlite3

conn = sqlite3.connect("humans.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        surname TEXT,
        group_name TEXT,
        courses TEXT,
        grades TEXT,
        average REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        surname TEXT,
        groups TEXT,
        courses TEXT,
        grades TEXT,
        average REAL
    )
''')

conn.commit()