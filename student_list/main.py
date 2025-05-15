from abc import ABC, abstractmethod

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




first = Student("Bogdan", "Krekhovetskyi", "fes-32")
second = Student("Bogdan", "Krekhovetskyi", "fes-32")
third = Teacher("Bogdan", "Krekhovetskyi")
third.add_course("first")
third.add_course("second")
third.add_course("third")
third.add_group("fes-12")
third.add_group("fes-22")
third.add_group("fes-32")
third.add_group("fes-42")


third.add_grade(2)
third.add_grade(4)
third.add_grade(5)
third.add_grade(1)
third.add_grade(3)



first.add_course("oop")
second.add_course("oop")
first.add_grade(1)
second.add_grade(2)
print(first.show_info())
print(second.show_info())
print(third.show_info())

humans[first.id] = first.to_dict()
humans[second.id] = second.to_dict()
humans[third.id] = third.to_dict()

print(humans)