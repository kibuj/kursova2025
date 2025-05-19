import tkinter as tk
from tkinter import messagebox
from db import conn, cursor
from human import Student, humans


def setup_student_ui(frame_students):
    global entry_s_name, entry_s_surname, entry_s_group, output_students
    global entry_update_id, entry_new_course, entry_new_grade, entry_new_group

    tk.Label(frame_students, text="Ім'я").pack()
    entry_s_name = tk.Entry(frame_students)
    entry_s_name.pack()

    tk.Label(frame_students, text="Прізвище").pack()
    entry_s_surname = tk.Entry(frame_students)
    entry_s_surname.pack()

    tk.Label(frame_students, text="Група").pack()
    entry_s_group = tk.Entry(frame_students)
    entry_s_group.pack()

    output_students = tk.Text(frame_students, height=10, width=60)
    output_students.pack(pady=10)

    def add_student():
        name = entry_s_name.get()
        surname = entry_s_surname.get()
        group = entry_s_group.get()

        if not name or not surname or not group:
            messagebox.showerror("Помилка", "Заповніть усі поля для студента.")
            return

        student = Student(name, surname, group)
        humans[student.id] = student.to_dict()
        student.save_to_db(conn)

        output_students.insert(tk.END, student.show_info() + "\n\n")

        entry_s_name.delete(0, tk.END)
        entry_s_surname.delete(0, tk.END)
        entry_s_group.delete(0, tk.END)

    def show_all_students():
        cursor.execute("SELECT id, name, surname, group_name, courses, grades, average FROM students")
        rows = cursor.fetchall()
        output_students.delete("1.0", tk.END)
        if not rows:
            output_students.insert(tk.END, "Немає записів про студентів.\n")
        else:
            for row in rows:
                sid, name, surname, group, courses, grades, average = row
                info = (f"ID: {sid}\n"
                        f"Студент: {surname} {name}\n"
                        f"Група: {group}\n"
                        f"Курси: {courses}\n"
                        f"Оцінки: {grades}\n"
                        f"Середня оцінка: {average:.2f}\n\n")
                output_students.insert(tk.END, info)

    tk.Button(frame_students, text="Додати студента", command=add_student).pack(pady=5)
    tk.Button(frame_students, text="Показати студентів", command=show_all_students).pack(pady=5)

    # === ОНОВЛЕННЯ СТУДЕНТА ===

    tk.Label(frame_students, text="Оновити студента за ID").pack()
    entry_update_id = tk.Entry(frame_students)
    entry_update_id.pack()

    tk.Label(frame_students, text="Додати курс (один)").pack()
    entry_new_course = tk.Entry(frame_students)
    entry_new_course.pack()

    tk.Label(frame_students, text="Додати оцінку (одна)").pack()
    entry_new_grade = tk.Entry(frame_students)
    entry_new_grade.pack()

    tk.Label(frame_students, text="Змінити групу").pack()
    entry_new_group = tk.Entry(frame_students)
    entry_new_group.pack()

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

        output_students.insert(tk.END, f"Оновлено:\n{student.show_info()}\n\n")

        entry_update_id.delete(0, tk.END)
        entry_new_course.delete(0, tk.END)
        entry_new_grade.delete(0, tk.END)
        entry_new_group.delete(0, tk.END)

    tk.Button(frame_students, text="Оновити дані студента", command=update_student).pack(pady=5)

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
        output_students.insert(tk.END, f"Студент з ID {sid} видалений.\n")

        entry_update_id.delete(0, tk.END)
        entry_new_course.delete(0, tk.END)
        entry_new_grade.delete(0, tk.END)
        entry_new_group.delete(0, tk.END)

    tk.Button(frame_students, text="Видалити студента", command=delete_student).pack(pady=5)
