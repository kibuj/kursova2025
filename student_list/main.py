from human import Student, sqlite3, Teacher, humans

conn = sqlite3.connect("humans.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    surname TEXT,
    group_name TEXT,
    courses TEXT,
    grades TEXT,
    average REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    surname TEXT,
    groups TEXT,
    courses TEXT,
    grades TEXT,
    average REAL
)
''')
conn.commit()


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
#print(first.show_info())
#print(second.show_info())
#print(third.show_info())

humans[first.id] = first.to_dict()
humans[second.id] = second.to_dict()
humans[third.id] = third.to_dict()

for student in humans.values():
    print(student['group'])


first.save_to_db(conn)
second.save_to_db(conn)
third.save_to_db(conn)