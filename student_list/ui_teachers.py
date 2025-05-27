import tkinter as tk
from tkinter import messagebox, Scrollbar
from db import conn, cursor
from human import Teacher, humans

def setup_teacher_ui(frame_teachers):
    tk.Label(frame_teachers, text="👨‍🏫 Керування викладачами", font=("Helvetica", 14, "bold")).pack(pady=5)

    add_frame = tk.LabelFrame(frame_teachers, text="➕ Додати викладача", padx=10, pady=10, bg="#f0f0f0")
    add_frame.pack(fill="x", padx=5, pady=5)

    def add_labeled_entry(parent, label, var_list):
        tk.Label(parent, text=label, bg="#f0f0f0").pack(anchor="w")
        entry = tk.Entry(parent, width=40)
        entry.pack()
        var_list.append(entry)

    entries = []
    labels = ["Ім'я", "Прізвище", "Курси (через кому)", "Групи (через кому)", "Оцінки (через кому)"]
    for label in labels:
        add_labeled_entry(add_frame, label, entries)

    entry_t_name, entry_t_surname, entry_t_courses, entry_t_groups, entry_t_grades = entries

    def add_teacher():
        name = entry_t_name.get().strip()
        surname = entry_t_surname.get().strip()
        courses = entry_t_courses.get().split(",")
        groups = entry_t_groups.get().split(",")
        grades_raw = entry_t_grades.get().split(",")

        if not name or not surname:
            messagebox.showerror("Помилка", "Ім’я та прізвище є обов’язковими.")
            return

        teacher = Teacher(name, surname)

        for course in courses:
            if course.strip():
                teacher.add_course(course.strip())
        for group in groups:
            if group.strip():
                teacher.add_group(group.strip())
        for grade in grades_raw:
            try:
                teacher.add_grade(int(grade.strip()))
            except ValueError:
                continue

        humans[teacher.id] = teacher.to_dict()
        teacher.save_to_db(conn)

        output_teachers.insert(tk.END, f"✅ Додано:\n{teacher.show_info()}\n\n")

        for e in entries:
            e.delete(0, tk.END)

    tk.Button(add_frame, text="Додати", command=add_teacher, bg="#d0f0c0").pack(pady=5)

    update_frame = tk.LabelFrame(frame_teachers, text="🛠 Оновлення / Пошук / Видалення", padx=10, pady=10, bg="#f9f9f9")
    update_frame.pack(fill="x", padx=5, pady=5)

    entry_teacher_id = tk.Entry(update_frame, width=40)
    entry_update_course = tk.Entry(update_frame, width=40)
    entry_update_group = tk.Entry(update_frame, width=40)
    entry_update_grade = tk.Entry(update_frame, width=40)

    for label, entry in [
        ("ID викладача", entry_teacher_id),
        ("Новий курс (один)", entry_update_course),
        ("Нова група (одна)", entry_update_group),
        ("Нова оцінка (одна)", entry_update_grade)
    ]:
        tk.Label(update_frame, text=label, bg="#f9f9f9").pack(anchor="w")
        entry.pack()

    def update_teacher():
        try:
            tid = int(entry_teacher_id.get())
        except ValueError:
            messagebox.showerror("Помилка", "ID має бути числом")
            return

        cursor.execute("SELECT name, surname, groups, courses, grades FROM teachers WHERE id = ?", (tid,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Помилка", f"Викладача з ID {tid} не знайдено.")
            return

        name, surname, groups_str, courses_str, grades_str = result

        teacher = Teacher(name, surname)
        teacher.id = tid
        teacher.groups = groups_str.split(",") if groups_str else []
        teacher.courses = courses_str.split(",") if courses_str else []
        teacher.grades = list(map(int, grades_str.split(","))) if grades_str else []

        new_course = entry_update_course.get().strip()
        new_group = entry_update_group.get().strip()
        new_grade = entry_update_grade.get().strip()

        if new_course:
            teacher.add_course(new_course)
        if new_group:
            teacher.add_group(new_group)
        if new_grade:
            try:
                teacher.add_grade(int(new_grade))
            except ValueError:
                messagebox.showerror("Помилка", "Оцінка має бути числом")

        humans[teacher.id] = teacher.to_dict()
        teacher.save_to_db(conn)

        output_teachers.insert(tk.END, f"✅ Оновлено:\n{teacher.show_info()}\n\n")

        entry_teacher_id.delete(0, tk.END)
        entry_update_course.delete(0, tk.END)
        entry_update_group.delete(0, tk.END)
        entry_update_grade.delete(0, tk.END)

    def find_teacher():
        try:
            tid = int(entry_teacher_id.get())
        except ValueError:
            messagebox.showerror("Помилка", "ID має бути числом")
            return

        cursor.execute("SELECT name, surname, groups, courses, grades, average FROM teachers WHERE id = ?", (tid,))
        row = cursor.fetchone()
        output_teachers.delete("1.0", tk.END)

        if row:
            name, surname, groups, courses, grades, average = row
            info = (f"🆔 ID: {tid}\n👨‍🏫 {surname} {name}\n📘 Курси: {courses}\n👥 Групи: {groups}\n"
                    f"📊 Оцінки: {grades}\n📈 Середня: {average:.2f}\n\n")
            output_teachers.insert(tk.END, info)
        else:
            output_teachers.insert(tk.END, f"Викладача з ID {tid} не знайдено.\n")

    def delete_teacher():
        try:
            tid = int(entry_teacher_id.get())
        except ValueError:
            messagebox.showerror("Помилка", "ID має бути числом")
            return

        cursor.execute("SELECT id FROM teachers WHERE id = ?", (tid,))
        if not cursor.fetchone():
            messagebox.showinfo("Інформація", f"Викладача з ID {tid} не знайдено.")
            return

        cursor.execute("DELETE FROM teachers WHERE id = ?", (tid,))
        conn.commit()
        output_teachers.insert(tk.END, f"🗑 Видалено викладача з ID {tid}.\n")

        entry_teacher_id.delete(0, tk.END)
        entry_update_course.delete(0, tk.END)
        entry_update_group.delete(0, tk.END)
        entry_update_grade.delete(0, tk.END)

    tk.Button(update_frame, text="Оновити", command=update_teacher, bg="#add8e6").pack(pady=2)
    tk.Button(update_frame, text="Знайти", command=find_teacher, bg="#ccffcc").pack(pady=2)
    tk.Button(update_frame, text="Видалити", command=delete_teacher, bg="#ff9999").pack(pady=2)

    # --- Фрейм: Вивід інформації ---
    output_frame = tk.LabelFrame(frame_teachers, text="📋 Інформація", padx=10, pady=10)
    output_frame.pack(fill="both", expand=True, padx=5, pady=10)

    output_teachers_scroll = Scrollbar(output_frame)
    output_teachers_scroll.pack(side="right", fill="y")

    global output_teachers
    output_teachers = tk.Text(output_frame, height=12, width=70, yscrollcommand=output_teachers_scroll.set)
    output_teachers.pack(side="left", fill="both", expand=True)
    output_teachers_scroll.config(command=output_teachers.yview)

    def show_all_teachers():
        cursor.execute("SELECT id, name, surname, groups, courses, grades, average FROM teachers")
        rows = cursor.fetchall()
        output_teachers.delete("1.0", tk.END)
        if not rows:
            output_teachers.insert(tk.END, "❌ Немає записів про викладачів.\n")
        else:
            for row in rows:
                tid, name, surname, groups, courses, grades, average = row
                info = (f"🆔 ID: {tid}\n👨‍🏫 {surname} {name}\n📘 Курси: {courses}\n👥 Групи: {groups}\n"
                        f"📊 Оцінки: {grades}\n📈 Середня: {average:.2f}\n\n")
                output_teachers.insert(tk.END, info)

    tk.Button(frame_teachers, text="📂 Показати всіх викладачів", command=show_all_teachers, bg="#e6e6fa").pack(pady=5)
