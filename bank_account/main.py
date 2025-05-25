class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0.0):
        self.id = None
        self.__owner = owner
        self.__balance = initial_balance
        self.__transactions = []

    def deposit(self, amount: float):
        if amount > 0:
            self.__balance += amount
            self.__transactions.append(f"Deposit {amount}")
        else:
            raise ValueError("Сума має бути більшою за 0")

    def withdraw(self, amount: float):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            self.__transactions.append(f"Withdraw {amount}")
        else:
            raise ValueError("Недостатньо коштів або неправильна сума")

    def get_balance(self):
        return self.__balance

    def get_transaction_history(self):
        return self.__transactions

    def save_to_db(self, conn):
        cursor = conn.cursor()
        transactions_str = ','.join(self.__transactions)

        if self.id is None:
            cursor.execute('''
                INSERT INTO balance (owner, balance, transactions)
                VALUES (?, ?, ?)
            ''', (self.__owner, self.__balance, transactions_str))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE balance
                SET owner = ?, balance = ?, transactions = ?
                WHERE id = ?
            ''', (self.__owner, self.__balance, transactions_str, self.id))

        conn.commit()

    @classmethod
    def load_from_db(cls, account_id: int, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT id, owner, balance, transactions FROM balance WHERE id = ?", (account_id,))
        row = cursor.fetchone()
        if row:
            instance = cls(row[1], row[2])
            instance.id = row[0]
            instance.__transactions = row[3].split(',') if row[3] else []
            return instance
        else:
            return None
