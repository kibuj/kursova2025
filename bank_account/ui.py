import tkinter as tk
from tkinter import messagebox, simpledialog
from db import conn
from main import BankAccount


def run_ui():
    window = tk.Tk()
    window.title("💰 Bank Account Manager")
    window.geometry("500x400")
    window.configure(bg="#f0f0f0")

    account = None

    def create_account():
        nonlocal account
        name = simpledialog.askstring("Створення акаунта", "Введіть ім’я власника:")
        balance = simpledialog.askfloat("Створення акаунта", "Введіть початковий баланс:")
        if name is not None and balance is not None:
            account = BankAccount(name, balance)
            messagebox.showinfo("✅ Успішно", f"Акаунт для {name} створено.")
        update_display()

    def deposit():
        if account:
            amount = simpledialog.askfloat("Поповнення", "Сума поповнення:")
            if amount:
                try:
                    account.deposit(amount)
                    update_display()
                except ValueError as e:
                    messagebox.showerror("Помилка", str(e))

    def withdraw():
        if account:
            amount = simpledialog.askfloat("Зняття", "Сума зняття:")
            if amount:
                try:
                    account.withdraw(amount)
                    update_display()
                except ValueError as e:
                    messagebox.showerror("Помилка", str(e))

    def save_account():
        if account:
            account.save_to_db(conn)
            messagebox.showinfo("✅ Збережено", f"Акаунт збережено (ID = {account.id})")

    def load_account():
        nonlocal account
        acc_id = simpledialog.askinteger("Завантаження", "Введіть ID рахунку:")
        if acc_id:
            acc = BankAccount.load_from_db(acc_id, conn)
            if acc:
                account = acc
                messagebox.showinfo("✅ Завантажено", f"Акаунт з ID {acc_id} завантажено.")
            else:
                messagebox.showerror("Помилка", "Рахунок не знайдено.")
        update_display()

    def show_info_by_id():
        acc_id = simpledialog.askinteger("Інформація по ID", "Введіть ID рахунку:")
        if acc_id:
            acc = BankAccount.load_from_db(acc_id, conn)
            if acc:
                info = (
                    f"ID: {acc.id}\n"
                    f"Власник: {acc._BankAccount__owner}\n"
                    f"Баланс: {acc.get_balance()}\n"
                    f"Транзакції:\n" + '\n'.join(acc.get_transaction_history())
                )
                messagebox.showinfo("Інформація по акаунту", info)
            else:
                messagebox.showerror("Помилка", f"Акаунт з ID {acc_id} не знайдено.")

    def update_display():
        text_box.delete("1.0", tk.END)
        if account:
            text_box.insert(tk.END, f"Власник: {account._BankAccount__owner}\n")
            text_box.insert(tk.END, f"Баланс: {account.get_balance():.2f}\n")
            text_box.insert(tk.END, "Транзакції:\n")
            for t in account.get_transaction_history():
                text_box.insert(tk.END, f"- {t}\n")

    tk.Label(window, text="💳 Банківський акаунт", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

    btn_frame = tk.Frame(window, bg="#f0f0f0")
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Створити акаунт", width=20, command=create_account).grid(row=0, column=0, padx=5, pady=2)
    tk.Button(btn_frame, text="Поповнити", width=20, command=deposit).grid(row=0, column=1, padx=5, pady=2)
    tk.Button(btn_frame, text="Зняти", width=20, command=withdraw).grid(row=1, column=0, padx=5, pady=2)
    tk.Button(btn_frame, text="Зберегти", width=20, command=save_account).grid(row=1, column=1, padx=5, pady=2)
    tk.Button(btn_frame, text="Завантажити", width=20, command=load_account).grid(row=2, column=0, padx=5, pady=2)
    tk.Button(btn_frame, text="Інформація по ID", width=20, command=show_info_by_id).grid(row=2, column=1, padx=5, pady=2)

    text_box = tk.Text(window, height=10, width=60, bg="#ffffff")
    text_box.pack(pady=10)

    window.mainloop()
    conn.close()

if __name__ == "__main__":
    run_ui()
