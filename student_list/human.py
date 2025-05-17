from abc import ABC, abstractmethod
import sqlite3
humans = {}

class Human(ABC):
    id_counter = 0
    def __init__(self, name, surname):
        self.id = Human.id_counter
        self.name = name
        self.surname = surname
        self.grades = []
        self.human = {}
        Human.id_counter += 1

    @abstractmethod
    def show_info(self):
        pass

    @abstractmethod
    def average(self):
        if not self.grades:
            return 0
        try:
            return sum(self.grades) / len(self.grades)
        except TypeError as ex:
            print(f"Значення повинне бути int: {ex}\n")


class Student(Human):
    def __init__(self, name, surname, group):
        super().__init__( name, surname)
        self.group = group
        self.grades = []
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

    def add_grade(self, grade):
        self.grades.append(grade)

    def average(self):
        return super().average()

    def show_info(self):
        return (f"Студент: {self.surname} {self.name}\n"
                f"ID: {self.id}\n"
                f"Група: {self.group}\n"
                f"Курси: {self.courses}\n"
                f"Оцінки: {self.grades}\n"
                f"Середня оцінка: {self.average()}")

    def to_dict(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'group': self.group,
            'courses': self.courses,
            'grades': self.grades,
            'average': self.average()
        }

    def save_to_db(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO students (id, name, surname, group_name, courses, grades, average)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.id,
            self.name,
            self.surname,
            self.group,
            ','.join(self.courses),
            ','.join(map(str, self.grades)),
            self.average()
        ))
        conn.commit()



class Teacher(Human):
    def __init__(self, name, surname):
        super().__init__( name, surname)
        self.groups = []
        self.courses = []
        self.grades = []

    def add_course(self, course):
        self.courses.append(course)

    def add_group(self, group):
        self.groups.append(group)

    def add_grade(self, grade):
        self.grades.append(grade)

    def average(self):
        return super().average()


    def show_info(self):
        return (f"Викладач: {self.surname} {self.name}\n"
                f"ID: {self.id}\n"
                f"Групи: {self.groups}\n"
                f"Курси: {self.courses}\n"
                f"Середня оцінка виставлена викладачем: {self.average()}")

    def to_dict(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'group': self.groups,
            'courses': self.courses,
            'average': self.average()
        }

    def save_to_db(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO teachers (id, name, surname, groups, courses, grades, average)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.id,
            self.name,
            self.surname,
            ','.join(self.groups),
            ','.join(self.courses),
            ','.join(map(str, self.grades)),
            self.average()
        ))
        conn.commit()

