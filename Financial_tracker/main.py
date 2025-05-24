#from abc import ABC, abstractmethod
from db import conn

class User:
    def __init__(self, name:str, balance:int):
        self.id = None
        self.name = name
        self.balance = balance
        self.changes = []

    def get_changes(self):
        return self.changes

    def get_amount(self):
        return self.balance


class Operation(User):
    def __init__(self, name:str, balance:int):
        super().__init__(name, balance)
        self.old_balance = balance

    def add_change(self, change:int):
        self.changes.append(change)
        self.balance += change

    def info(self):
        if sum(self.changes) < 0:
            return f"Баланс зменшився на: {self.old_balance - self.balance}"
        elif sum(self.changes) == 0:
            return f"Баланс не змінився: {self.balance}"
        else:
            return f"Баланс збільшився на :{self.balance - self.old_balance}"


    @classmethod
    def load_from_db(cls, user_id:int, conn):
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, name, balance, changes FROM balance WHERE id={user_id}")
        row = cursor.fetchone()

        if row:
            instance = cls(row[1], row[2])
            instance.id = row[0]
            instance.changes = list(map(int, row[3].split(','))) if row[3] else []
            instance.old_balance = row[2] - sum(instance.changes)
            return instance
        else:
            return None

    def save_to_db(self):
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM balance WHERE id = ?", (self.id,))
        existing = cursor.fetchone()

        if existing:
            cursor.execute('''
                UPDATE balance
                SET name = ?, balance = ?, changes = ?
                WHERE id = ?
            ''', (
                self.name,
                self.balance,
                ','.join(map(str, self.changes)),
                self.id
            ))
        else:
            cursor.execute('''
                INSERT INTO balance (id, name, balance, changes)
                VALUES (?, ?, ?, ?)
            ''', (
                self.id,
                self.name,
                self.balance,
                ','.join(map(str, self.changes))
            ))
            self.id = cursor.lastrowid
        conn.commit()


#def main():
#    first = Operation('Bogdan', 12)
#    first.add_change(10)
#    print(first.get_amount())
#    first.add_change(20)
#    first.add_change(30)
#    first.add_change(40)
#    first.add_change(-50)
#    print(first.get_changes())
#    print(first.info())
#    first.save_to_db()
#    print(first.id)
#    second = Operation.load_from_db(0, conn)
#    second.add_change(10)
#    second.save_to_db()
#    print(second.info())
#
#main()
