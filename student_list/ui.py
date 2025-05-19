import tkinter as tk
from tkinter import ttk, messagebox
from db import conn, cursor
from human import Student, Teacher, humans
from ui_students import setup_student_ui
from ui_teachers import setup_teacher_ui

def launch_app():
    root = tk.Tk()
    root.title("Система обліку студентів та викладачів")
    root.geometry("550x700")

    notebook = ttk.Notebook(root)
    frame_students = ttk.Frame(notebook)
    frame_teachers = ttk.Frame(notebook)

    notebook.add(frame_students, text='Студенти')
    notebook.add(frame_teachers, text='Викладачі')
    notebook.pack(expand=True, fill="both")

    setup_student_ui(frame_students)
    setup_teacher_ui(frame_teachers)


    root.mainloop()
