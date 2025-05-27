import tkinter as tk
from tkinter import messagebox, Scrollbar
from db import conn, cursor
from human import Student, humans

def setup_student_ui(frame_students):
    tk.Label(frame_students, text="🎓 Керування студентами", font=("Helvetica", 14, "bold")).pack(pady=5)

    add_frame = tk.LabelFrame(frame_students, text="➕ Додати студента", padx=10, pady=10, bg="#f0f8ff")
    add_frame.pack(fill="x", padx=5, pady=5)

    global entry_s_name, entry_s_surname, entry_s_group
    entry_s_name = tk.Entry(add_frame, width=40)
    entry_s_surname = tk.Entry(add_frame, width=40)
    entry_s_group = tk.Entry(add_frame, width=40)

    for label, entry in [("Ім'я", entry_s_name), ("Прізвище", entry_s_surname), ("Група", entry_s_group)]:
        tk.Label(add_frame, text=label, bg="#f0f8ff").pack(anchor="w")
        entry.pack()

    def add_student():
        name = entry_s_name.get().strip()
        surname = entry_s_surname.get().strip()
        group = entry_s_group.get().strip()

        if not name or not surname or not group:
            messagebox.showerror("Помилка", "Заповніть усі поля для студента.")
            return

        student = Student(name, surname, group)
        humans[student.id] = student.to_dict()
        student.save_to_db(conn)

        output_students.insert(tk.END, f"✅ Додано:\n{student.show_info()}\n\n")

        entry_s_name.delete(0, tk.END)
        entry_s_surname.delete(0, tk.END)
        entry_s_group.delete(0, tk.END)

    tk.Button(add_frame, text="Додати студента", command=add_student, bg="#d0f0c0").pack(pady=5)

    output_frame = tk.LabelFrame(frame_students, text="📋 Інформація", padx=10, pady=10)
    output_frame.pack(fill="both", expand=True, padx=5, pady=5)

    global output_students
    scroll = Scrollbar(output_frame)
    scroll.pack(side="right", fill="y")

    output_students = tk.Text(output_frame, height=12, width=70, yscrollcommand=scroll.set)
    output_students.pack(side="left", fill="both", expand=True)
    scroll.config(command=output_students.yview)

    def show_all_students():
        cursor.execute("SELECT id, name, surname, group_name, courses, grades, average FROM students")
        rows = cursor.fetchall()
        output_students.delete("1.0", tk.END)
        if not rows:
            output_students.insert(tk.END, "❌ Немає записів про студентів.\n")
        else:
            for row in rows:
                sid, name, surname, group, courses, grades, average = row
                info = (f"🆔 ID: {sid}\n👤 {surname} {name}\n🏫 Група: {group}\n📘 Курси: {courses}\n"
                        f"📊 Оцінки: {grades}\n📈 Середня: {average:.2f}\n\n")
                output_students.insert(tk.END, info)

    tk.Button(frame_students, text="📂 Показати всіх студентів", command=show_all_students, bg="#e6e6fa").pack(pady=5)

    update_frame = tk.LabelFrame(frame_students, text="🛠 Оновити / Видалити", padx=10, pady=10, bg="#f9f9f9")
    update_frame.pack(fill="x", padx=5, pady=5)

    global entry_update_id, entry_new_course, entry_new_grade, entry_new_group
    entry_update_id = tk.Entry(update_frame, width=40)
    entry_new_course = tk.Entry(update_frame, width=40)
    entry_new_grade = tk.Entry(update_frame, width=40)
    entry_new_group = tk.Entry(update_frame, width=40)

    for label, entry in [
        ("ID студента", entry_update_id),
        ("Новий курс", entry_new_course),
        ("Нова оцінка", entry_new_grade)
    ]:
        tk.Label(update_frame, text=label, bg="#f9f9f9").pack(anchor="w")
        entry.pack()

    def update_student():
        try:
            student_id = int(entry_update_id.get())
        except ValueError:
            messagebox.showerror("Помилка", "ID має бути числом")
            return

        cursor.execute("SELECT name, surname, group_name, courses, grades FROM students WHERE id = ?", (student_id,))
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Помилка", f"Студента з ID {student_id} не знайдено.")
            return

        name, surname, group, courses_str, grades_str = result

        student = Student(name, surname, group)
        student.id = student_id
        student.courses = courses_str.split(",") if courses_str else []
        student.grades = list(map(int, grades_str.split(","))) if grades_str else []

        new_course = entry_new_course.get().strip()
        if new_course:
            student.add_course(new_course)

        new_grade = entry_new_grade.get().strip()
        if new_grade:
            try:
                student.add_grade(int(new_grade))
            except ValueError:
                messagebox.showerror("Помилка", "Оцінка має бути числом")

        new_group = entry_new_group.get().strip()
        if new_group:
            student.group = new_group

        humans[student.id] = student.to_dict()
        student.save_to_db(conn)

        output_students.insert(tk.END, f"✅ Оновлено:\n{student.show_info()}\n\n")

        entry_update_id.delete(0, tk.END)
        entry_new_course.delete(0, tk.END)
        entry_new_grade.delete(0, tk.END)
        entry_new_group.delete(0, tk.END)

    def delete_student():
        try:
            sid = int(entry_update_id.get())
        except ValueError:
            messagebox.showerror("Помилка", "ID має бути числом")
            return

        cursor.execute("SELECT id FROM students WHERE id = ?", (sid,))
        if not cursor.fetchone():
            messagebox.showinfo("Інформація", f"Студента з ID {sid} не знайдено.")
            return

        cursor.execute("DELETE FROM students WHERE id = ?", (sid,))
        conn.commit()
        output_students.insert(tk.END, f"🗑 Студент з ID {sid} видалений.\n")

        entry_update_id.delete(0, tk.END)
        entry_new_course.delete(0, tk.END)
        entry_new_grade.delete(0, tk.END)
        entry_new_group.delete(0, tk.END)

    tk.Button(update_frame, text="Оновити дані", command=update_student, bg="#add8e6").pack(pady=2)
    tk.Button(update_frame, text="Видалити студента", command=delete_student, bg="#ff9999").pack(pady=2)
