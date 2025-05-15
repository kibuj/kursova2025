from abc import ABC, abstractmethod


class Human(ABC):
    id_counter = 0
    def __init__(self, name, surname):
        self.id = Human.id_counter
        self.name = name
        self.surname = surname
        Human.id_counter += 1

    @abstractmethod
    def show_info(self):
        pass

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

    def show_info(self):
        return (f"Студент: {self.surname} {self.name}\n"
                f"ID: {self.id}\n"
                f"Група: {self.group}\n"
                f"Курси: {self.courses}\n"
                f"Оцінки: {self.grades}")


first = Student("Bogdan", "Krekhovetskyi", "fes-32")
second = Student("Bogdan", "Krekhovetskyi", "fes-32")

first.add_course("oop")
second.add_course("oop")
first.add_grade("1")
second.add_grade("2")
print(first.show_info())
print(second.show_info())