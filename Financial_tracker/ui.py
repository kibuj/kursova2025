import tkinter as tk
from tkinter import messagebox
from main import Operation
from db import conn

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    update_output(f"👤 Створено користувача: {name}\n💰 Баланс: {balance} ₴\n🆔 ID: {current_user.id}")
    clear_graph()

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
        update_output(f"🔄 Завантажено користувача: {user.name}\n💰 Баланс: {user.balance} ₴\n🆔 ID: {user.id}")
        clear_graph()
    else:
        messagebox.showerror("Помилка", f"Користувача з ID {user_id} не знайдено")

def show_info():
    if not current_user:
        messagebox.showerror("Помилка", "Спочатку завантажте або створіть користувача")
        return
    update_output(
        f"📄 Інформація про користувача\n"
        f"🧾 {current_user.info()}\n"
        f"💰 Баланс: {current_user.get_amount()} ₴\n"
        f"📊 Зміни: {current_user.get_changes()}"
    )

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
    update_output(f"➕ Додано зміну: {change} ₴\n🧾 {current_user.info()}")
    clear_graph()

def show_graph():
    if not current_user:
        messagebox.showerror("Помилка", "Спочатку завантажте або створіть користувача")
        return

    changes = current_user.get_changes()
    if not changes:
        messagebox.showinfo("Немає даних", "Немає змін для побудови графіка")
        return

    balances = [current_user.balance - sum(changes)]
    for change in changes:
        balances.append(balances[-1] + change)

    graph_window = tk.Toplevel()
    graph_window.title(f"📈 Графік змін — {current_user.name}")
    graph_window.geometry("600x400")
    graph_window.configure(bg="#f0f0f0")

    fig = Figure(figsize=(6, 3.5), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(range(len(balances)), balances, marker='o', linestyle='-', color='royalblue')
    ax.set_title(f"📊 Баланс користувача: {current_user.name}")
    ax.set_xlabel("Операція")
    ax.set_ylabel("Баланс (₴)")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(padx=10, pady=10)


def clear_graph():
    for widget in graph_frame.winfo_children():
        widget.destroy()

def update_output(text):
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, text)
    output_text.config(state="disabled")

root = tk.Tk()
root.title("💼 Фінансовий трекер")
root.geometry("500x720")
root.configure(bg="#e6f2ff")
root.resizable(False, False)

tk.Label(
    root, text="💰 Фінансовий Трекер", font=("Helvetica", 16, "bold"),
    bg="#e6f2ff", fg="#333"
).pack(pady=10)

frame = tk.Frame(root, padx=15, pady=15, bg="#f9f9f9", relief="groove", bd=2)
frame.pack(fill="both", expand=True, padx=10, pady=10)

def add_labeled_entry(row, label_text):
    tk.Label(frame, text=label_text, bg="#f9f9f9", anchor="w").grid(row=row, column=0, sticky="w", pady=4)
    entry = tk.Entry(frame, width=30)
    entry.grid(row=row, column=1, pady=4)
    return entry

name_entry = add_labeled_entry(0, "Ім'я користувача:")
balance_entry = add_labeled_entry(1, "Початковий баланс:")
load_id_entry = add_labeled_entry(3, "ID користувача:")
change_entry = add_labeled_entry(5, "Зміна (дохід/витрата):")

def add_button(text, command, row, color):
    tk.Button(frame, text=text, command=command, bg=color, fg="black", width=35).grid(
        row=row, column=0, columnspan=2, pady=4
    )

add_button("➕ Створити користувача", create_user, 2, "#b3e6ff")
add_button("📂 Завантажити користувача", load_user, 4, "#d0f0c0")
add_button("💸 Додати зміну", add_change, 6, "#ffe680")
add_button("ℹ️ Показати інформацію", show_info, 7, "#ffb6c1")
add_button("📈 Побудувати графік", show_graph, 8, "#c3f2ff")

tk.Label(frame, text="📋 Вивід:", bg="#f9f9f9", anchor="w").grid(row=9, column=0, sticky="w", pady=(10, 0))
output_text = tk.Text(frame, height=8, width=50, wrap="word", bg="#ffffff", font=("Consolas", 10))
output_text.grid(row=10, column=0, columnspan=2, pady=(5, 10))
output_text.config(state="disabled")

graph_frame = tk.Frame(frame, bg="#f9f9f9")
graph_frame.grid(row=11, column=0, columnspan=2, pady=10)

root.mainloop()
