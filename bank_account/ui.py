import tkinter as tk
from tkinter import messagebox, simpledialog, PhotoImage
from db import conn
from main import BankAccount

def run_ui():
    window = tk.Tk()
    window.title("💰 Bank Account Manager")
    window.geometry("500x360")
    window.configure(bg="#e8f4f8")


    tk.Label(
        window,
        text="💳 Банківський акаунт",
        font=("Helvetica", 18, "bold"),
        fg="#333333",
        bg="#e8f4f8"
    ).pack(pady=10)

    account = None

    def create_account():
        nonlocal account
        name = simpledialog.askstring("👤 Створення акаунта", "Введіть ім’я власника:")
        balance = simpledialog.askfloat("💵 Початковий баланс", "Введіть початковий баланс:")
        if name is not None and balance is not None:
            account = BankAccount(name, balance)
            messagebox.showinfo("✅ Успішно", f"Акаунт для {name} створено 💳.")
        update_display()

    def deposit():
        if account:
            amount = simpledialog.askfloat("➕ Поповнення", "Введіть суму:")
            if amount:
                try:
                    account.deposit(amount)
                    update_display()
                    messagebox.showinfo("✅ Готово", f"На рахунок зараховано {amount:.2f} ₴")
                except ValueError as e:
                    messagebox.showerror("⚠️ Помилка", str(e))

    def withdraw():
        if account:
            amount = simpledialog.askfloat("➖ Зняття", "Введіть суму:")
            if amount:
                try:
                    account.withdraw(amount)
                    update_display()
                    messagebox.showinfo("✅ Готово", f"З рахунку знято {amount:.2f} ₴")
                except ValueError as e:
                    messagebox.showerror("⚠️ Помилка", str(e))

    def save_account():
        if account:
            account.save_to_db(conn)
            messagebox.showinfo("💾 Збереження", f"Акаунт збережено (ID: {account.id})")

    def load_account():
        nonlocal account
        acc_id = simpledialog.askinteger("📂 Завантажити", "Введіть ID рахунку:")
        if acc_id:
            acc = BankAccount.load_from_db(acc_id, conn)
            if acc:
                account = acc
                messagebox.showinfo("✅ Завантажено", f"Акаунт з ID {acc_id} завантажено.")
            else:
                messagebox.showerror("❌ Не знайдено", "Рахунок не знайдено.")
        update_display()

    def show_info_by_id():
        acc_id = simpledialog.askinteger("🔍 Перевірити", "Введіть ID рахунку:")
        if acc_id:
            acc = BankAccount.load_from_db(acc_id, conn)
            if acc:
                info = (
                    f"📌 ID: {acc.id}\n"
                    f"👤 Власник: {acc._BankAccount__owner}\n"
                    f"💰 Баланс: {acc.get_balance():.2f} ₴\n"
                    f"🧾 Транзакції:\n" + '\n'.join(acc.get_transaction_history())
                )
                messagebox.showinfo("📋 Інформація про акаунт", info)
            else:
                messagebox.showerror("❌ Не знайдено", f"Акаунт з ID {acc_id} не існує.")

    def update_display():
        text_box.delete("1.0", tk.END)
        if account:
            text_box.insert(tk.END, f"👤 Власник: {account._BankAccount__owner}\n")
            text_box.insert(tk.END, f"💰 Баланс: {account.get_balance():.2f} ₴\n")
            text_box.insert(tk.END, "🧾 Транзакції:\n")
            for t in account.get_transaction_history():
                text_box.insert(tk.END, f"• {t}\n")

    btn_frame = tk.Frame(window, bg="#e8f4f8")
    btn_frame.pack(pady=10)

    def styled_button(text, row, column, command):
        tk.Button(
            btn_frame,
            text=text,
            width=20,
            bg="#4da6ff",
            fg="white",
            font=("Helvetica", 10, "bold"),
            command=command
        ).grid(row=row, column=column, padx=6, pady=6)

    styled_button("Створити акаунт", 0, 0, create_account)
    styled_button("Поповнити", 0, 1, deposit)
    styled_button("Зняти", 1, 0, withdraw)
    styled_button("Зберегти", 1, 1, save_account)
    styled_button("Завантажити", 2, 0, load_account)
    styled_button("Інфо по ID", 2, 1, show_info_by_id)

    text_box = tk.Text(window, height=10, width=70, bg="#ffffff", font=("Consolas", 10))
    text_box.pack(pady=10)

    window.mainloop()
    conn.close()

if __name__ == "__main__":
    run_ui()
