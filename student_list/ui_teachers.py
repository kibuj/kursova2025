import tkinter as tk
from tkinter import messagebox
from db import conn, cursor
from human import Teacher, humans


def setup_teacher_ui(frame_teachers):
    global entry_t_name, entry_t_surname, entry_t_courses, entry_t_groups, entry_t_grades
    global entry_teacher_id, entry_update_course, entry_update_group, entry_update_grade
    global output_teachers

    tk.Label(frame_teachers, text="Ім'я").pack()
    entry_t_name = tk.Entry(frame_teachers)
    entry_t_name.pack()

    tk.Label(frame_teachers, text="Прізвище").pack()
    entry_t_surname = tk.Entry(frame_teachers)
    entry_t_surname.pack()

    tk.Label(frame_teachers, text="Курси (через кому)").pack()
    entry_t_courses = tk.Entry(frame_teachers)
    entry_t_courses.pack()

    tk.Label(frame_teachers, text="Групи (через кому)").pack()
    entry_t_groups = tk.Entry(frame_teachers)
    entry_t_groups.pack()

    tk.Label(frame_teachers, text="Оцінки (через кому)").pack()
    entry_t_grades = tk.Entry(frame_teachers)
    entry_t_grades.pack()

    output_teachers = tk.Text(frame_teachers, height=10, width=60)
    output_teachers.pack(pady=10)
    # --- ОНОВЛЕННЯ / ПОШУК / ВИДАЛЕННЯ ВИКЛАДАЧІВ ЗА ID ---

    tk.Label(frame_teachers, text="Оновити/пошук/видалення викладача за ID").pack()
    entry_teacher_id = tk.Entry(frame_teachers)
    entry_teacher_id.pack()

    tk.Label(frame_teachers, text="Новий курс (один)").pack()
    entry_update_course = tk.Entry(frame_teachers)
    entry_update_course.pack()

    tk.Label(frame_teachers, text="Нова група (одна)").pack()
    entry_update_group = tk.Entry(frame_teachers)
    entry_update_group.pack()

    tk.Label(frame_teachers, text="Нова оцінка (одна)").pack()
    entry_update_grade = tk.Entry(frame_teachers)
    entry_update_grade.pack()


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

        output_teachers.insert(tk.END, f"Оновлено:\n{teacher.show_info()}\n\n")

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
            info = (f"ID: {tid}\n"
                    f"Викладач: {surname} {name}\n"
                    f"Групи: {groups}\n"
                    f"Курси: {courses}\n"
                    f"Оцінки: {grades}\n"
                    f"Середня оцінка: {average:.2f}\n\n")
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
        output_teachers.insert(tk.END, f"Викладач з ID {tid} видалений.\n")

        entry_teacher_id.delete(0, tk.END)
        entry_update_course.delete(0, tk.END)
        entry_update_group.delete(0, tk.END)
        entry_update_grade.delete(0, tk.END)


    tk.Button(frame_teachers, text="Оновити викладача", command=update_teacher).pack(pady=2)
    tk.Button(frame_teachers, text="Видалити викладача", command=delete_teacher).pack(pady=2)


    def add_teacher():
        name = entry_t_name.get()
        surname = entry_t_surname.get()
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

        output_teachers.insert(tk.END, teacher.show_info() + "\n\n")

        entry_t_name.delete(0, tk.END)
        entry_t_surname.delete(0, tk.END)
        entry_t_courses.delete(0, tk.END)
        entry_t_groups.delete(0, tk.END)
        entry_t_grades.delete(0, tk.END)

    def show_all_teachers():
        cursor.execute("SELECT id, name, surname, groups, courses, grades, average FROM teachers")
        rows = cursor.fetchall()
        output_teachers.delete("1.0", tk.END)
        if not rows:
            output_teachers.insert(tk.END, "Немає записів про викладачів.\n")
        else:
            for row in rows:
                tid, name, surname, groups, courses, grades, average = row
                info = (f"ID: {tid}\n"
                        f"Викладач: {surname} {name}\n"
                        f"Групи: {groups}\n"
                        f"Курси: {courses}\n"
                        f"Оцінки: {grades}\n"
                        f"Середня оцінка: {average:.2f}\n\n")
                output_teachers.insert(tk.END, info)

    tk.Button(frame_teachers, text="Додати викладача", command=add_teacher).pack(pady=5)
    tk.Button(frame_teachers, text="Показати викладачів", command=show_all_teachers).pack(pady=5)