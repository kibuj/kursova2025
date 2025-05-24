import tkinter as tk
from tkinter import messagebox
from main import Operation
from db import conn

current_user = None

def create_user():
    global current_user
    name = name_entry.get()
    try:
        balance = int(balance_entry.get())
    except ValueError:
        messagebox.showerror("Помилка", "Баланс має бути числом")
        return

    current_user = Operation(name, balance)
    current_user.save_to_db()
    update_output(f"Створено користувача: {name} з балансом {balance}\nID: {current_user.id}")

def load_user():
    global current_user
    try:
        user_id = int(load_id_entry.get())
    except ValueError:
        messagebox.showerror("Помилка", "ID має бути числом")
        return

    user = Operation.load_from_db(user_id, conn)
    if user:
        current_user = user
        update_output(f"Завантажено користувача: {user.name} з балансом {user.balance}\nID: {user.id}")
    else:
        messagebox.showerror("Помилка", f"Користувача з ID {user_id} не знайдено")

def show_info():
    if not current_user:
        messagebox.showerror("Помилка", "Спочатку завантажте або створіть користувача")
        return
    update_output(f"{current_user.info()}\nБаланс: {current_user.get_amount()}\nЗміни: {current_user.get_changes()}")

def add_change():
    global current_user
    if not current_user:
        messagebox.showerror("Помилка", "Спочатку завантажте або створіть користувача")
        return
    try:
        change = int(change_entry.get())
    except ValueError:
        messagebox.showerror("Помилка", "Зміна має бути числом")
        return

    current_user.add_change(change)
    current_user.save_to_db()
    update_output(f"Додано зміну: {change}\n{current_user.info()}")

def update_output(text):
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, text)
    output_text.config(state="disabled")

root = tk.Tk()
root.title("Фінансовий трекер")
root.geometry("400x500")
root.resizable(False, False)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Ім'я користувача:").grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(frame, width=30)
name_entry.grid(row=0, column=1)

tk.Label(frame, text="Початковий баланс:").grid(row=1, column=0, sticky="w")
balance_entry = tk.Entry(frame, width=30)
balance_entry.grid(row=1, column=1)

tk.Button(frame, text="Створити користувача", command=create_user, bg="#add8e6").grid(row=2, column=0, columnspan=2, pady=5)

tk.Label(frame, text="ID користувача:").grid(row=3, column=0, sticky="w")
load_id_entry = tk.Entry(frame, width=30)
load_id_entry.grid(row=3, column=1)

tk.Button(frame, text="Завантажити користувача", command=load_user, bg="#d0f0c0").grid(row=4, column=0, columnspan=2, pady=5)

tk.Label(frame, text="Зміна (доход/витрата):").grid(row=5, column=0, sticky="w")
change_entry = tk.Entry(frame, width=30)
change_entry.grid(row=5, column=1)

tk.Button(frame, text="Додати зміну", command=add_change, bg="#ffd580").grid(row=6, column=0, columnspan=2, pady=5)

tk.Button(frame, text="Показати інформацію", command=show_info, bg="#ffb6c1").grid(row=7, column=0, columnspan=2, pady=5)

output_text = tk.Text(frame, height=10, width=45, wrap="word")
output_text.grid(row=8, column=0, columnspan=2, pady=10)
output_text.config(state="disabled")

root.mainloop()