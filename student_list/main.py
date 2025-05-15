from abc import ABC, abstractmethod


class Human(ABC):
    id_counter = 0
    def __init__(self, name, surname):
        self.id = Human.id_counter
        self.name = name
        self.surname = surname
        self.grades = []
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

    def average(self):
        return super().average()


    def show_info(self):
        return (f"Студент: {self.surname} {self.name}\n"
                f"ID: {self.id}\n"
                f"Група: {self.groups}\n"
                f"Курси: {self.courses}\n")




first = Student("Bogdan", "Krekhovetskyi", "fes-32")
second = Student("Bogdan", "Krekhovetskyi", "fes-32")

first.add_course("oop")
second.add_course("oop")
first.add_grade(1)
second.add_grade(2)
print(first.show_info())
print(second.show_info())