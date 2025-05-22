#from abc import ABC, abstractmethod
from db import conn

class User:
    id_counter = 0
    def __init__(self, name:str, balance:int):
        self.id = User.id_counter
        self.name = name
        self.balance = balance
        self.changes = []
        User.id_counter += 1

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

    def save_to_db(self):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO balance (id, name, balance, changes)
            VALUES (?, ?, ?, ?)
        ''', (
            self.id,
            self.name,
            self.balance,
            ','.join(map(str, self.changes)),
        ))
        conn.commit()


def main():
    first = Operation('Bogdan', 12)
    first.add_change(10)
    print(first.get_amount())
    first.add_change(20)
    first.add_change(30)
    first.add_change(40)
    first.add_change(-50)
    print(first.get_changes())
    print(first.info())
    first.save_to_db()

main()
