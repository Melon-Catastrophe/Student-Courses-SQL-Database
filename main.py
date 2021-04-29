import sqlite3

connection = sqlite3.connect('test.db')
cursor = connection.cursor()


def create_tables():
  cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='students' ''')
  if cursor.fetchone()[0] == 1:
    connection.execute('DROP TABLE students')
    connection.commit()
   
  cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='courses' ''')
  if cursor.fetchone()[0] == 1:
    connection.execute('DROP TABLE courses')
    connection.commit()

  cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='courses_has_students' ''')
  if cursor.fetchone()[0] == 1:
    connection.execute('DROP TABLE courses_has_students')
    connection.commit()

  connection.execute('CREATE TABLE courses (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, c_id VARCHAR(10) NOT NULL, name TEXT NOT NULL);')
  connection.execute('CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, fname TEXT NOT NULL, lname TEXT NOT NULL, phone VARCHAR(12))')
  connection.execute('CREATE TABLE courses_has_students (courses_id VARCHAR(10) NOT NULL, students_id TEXT NOT NULL, PRIMARY KEY (courses_id, students_id))')
  connection.commit()


def populate_tables():
  connection.execute('DELETE FROM courses')
  connection.execute('DELETE FROM students')
  connection.commit()

  values = (('CSE310', 'Applied Programming'), ('CIT171', 'Intro to Cybersecurity'), ('ECEN106', 'Computer Systems'), ('CIT111', 'Intro to Databases'), ('CSE150', 'Data Intuition and Insight'), ('CSE210', 'Programming with Classes'), ('GE101', 'College Success'))
  for i in range(len(values)):
    connection.execute('INSERT INTO courses (c_id, name) VALUES (?, ?)', values[i])
    connection.commit()

  values = (('Will', 'Smith', '555-267-9928'), ('Tim', 'Willards', '267-543-7731'))
  for i in range(len(values)):
    connection.execute('INSERT INTO students (fname, lname, phone) VALUES (?, ?, ?)', values[i])
    connection.commit()

  # courses_id, student_id
  values = ((2, 1), (3, 1), (4, 1), (7, 1), (1, 2), (4, 2), (5, 2), (6, 2))
  for i in range(len(values)):
    connection.execute('INSERT INTO courses_has_students (courses_id, students_id) VALUES (?, ?)', values[i])
    connection.commit()


def display_tables():
  cursor.execute('SELECT * FROM courses')
  print("\nCourses Table")
  for row in cursor.fetchall():
    print(row)
  
  cursor.execute('SELECT * FROM students')
  print("\nStudents Table")
  for row in cursor.fetchall():
    print(row)

  cursor.execute('SELECT * FROM courses_has_students')
  print("\nCourses Has Students Table")
  for row in cursor.fetchall():
    print(row)


def display_student_courses():
  while True:
    print("\nWhat is the first name of the student whose courses you would like to view?")
    stu_name = input(">  ")

    values = (stu_name.lower(), )
    cursor.execute('SELECT fname FROM students WHERE LOWER(students.fname) = ?', values)
  
    if cursor.fetchone() != None:
      break
    else:
      print("Name not found. Please enter a student's name.")
  
  print('\n' + stu_name.capitalize() + ''''s Courses''')
  cursor.execute('SELECT c.c_id, c.name FROM students JOIN courses_has_students cs ON students.id = cs.students_id JOIN courses c ON cs.courses_id = c.id WHERE LOWER(students.fname) = ?', values)
  
  for item in cursor.fetchall():
    print(item[0] + '\t\t' + item[1])


if __name__ == '__main__':
  print("Welcome to Database Manager")
  
  while True:
    print("\n1) Create Tables", "\n2) Populate Tables", "\n3) Insert into Table", "\n4) Display Student's Courses", "\n5) Display Tables", "\n6) Quit\n")
    choice = input(">  ")
    if choice == '1':
      create_tables()
      print("Tables created.")

    elif choice == '2':
      populate_tables()
      print("Tables populated with default values.")

    elif choice == '3':
      pass
    elif choice == '4':
      display_student_courses()

    elif choice == '5':
      display_tables()

    elif choice == '6':
      break
    else:
      print("Please enter a choice 1-6.")

  print("\n")
  connection.close()