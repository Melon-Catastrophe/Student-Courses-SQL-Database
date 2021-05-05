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
  create_tables()

  connection.execute('DELETE FROM courses')
  connection.execute('DELETE FROM students')
  connection.execute('DELETE FROM courses_has_students')
  connection.commit()

  values = (('CSE310', 'Applied Programming'), ('CIT171', 'Intro to Cybersecurity'), ('ECEN106', 'Computer Systems'), ('CIT111', 'Intro to Databases'), ('CSE150', 'Data Intuition and Insight'), ('CSE210', 'Programming with Classes'), ('GE101', 'College Success'))
  for i in range(len(values)):
    connection.execute('INSERT INTO courses (c_id, name) VALUES (?, ?)', values[i])
    connection.commit()

  values = (('Will', 'Smith', '555-267-9928'), ('Tim', 'Willards', '267-543-7731'))
  for i in range(len(values)):
    connection.execute('INSERT INTO students (fname, lname, phone) VALUES (?, ?, ?)', values[i])
    connection.commit()

  # courses_id, students_id
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


def display_student_info():
  cursor.execute('SELECT fname, lname, phone FROM students ORDER BY fname')
  print("\nStudent Information")
  
  for row in cursor.fetchall():
    item_list = []
    for item in row:
      item_list.append(item)
    print(item_list[0] + "\t" + item_list[1] + "     \t" + item_list[2])


def display_courses():
  cursor.execute("SELECT c_id, name FROM courses ORDER BY courses.c_id")
  print("\nCourse ID" + "  \tCourse Name")

  for item in cursor.fetchall():
    print(item[0], "  \t" + str(item[1]))


def insert_courses():
  new_c_id = input("\nPlease enter a course id.\n>  ")
  new_c_name = input("\nPlease enter a course name.\n>  ")
  
  values = (new_c_id, new_c_name)
  connection.execute('INSERT INTO courses (c_id, name) VALUES (?, ?)', values)
  connection.commit()


def insert_students():
  new_fname = input("\nPlease enter the student's first name.\n>  ")
  new_lname = input("\nPlease enter the student's last name.\n>  ")
  new_phone = input("\nPlease enter the student's phone number using the format '123-456-6789'.\n>  ")
  
  values = (new_fname, new_lname, new_phone)
  connection.execute('INSERT INTO students (fname, lname, phone) VALUES (?, ?, ?)', values)
  connection.commit()


def insert_courses_has_students():
  while True:
    new_courses_id = input("\nPlease enter the ID number for the course.\n>  ")
    try:
      new_courses_id = int(new_courses_id)
    except ValueError:
      print("ValueError: User did not input an integer")
    if isinstance(new_courses_id, int):
      break
  while True:
    new_students_id = input("\nPlease enter the ID number for the student.\n>  ")
    try:
      new_students_id = int(new_students_id)
    except ValueError:
      print("ValueError: User did not input an integer")
    if isinstance(new_students_id, int):
      break
  
  values = (new_courses_id, new_students_id)
  connection.execute('INSERT INTO courses_has_students (courses_id, students_id) VALUES (?, ?)', values)
  connection.commit()

if __name__ == '__main__':
  print("Welcome to Database Manager")
  
  while True:
    print("\n1) Create Tables", "\n2) Populate Tables", "\n3) Insert into Table...", "\n4) Display...", "\n5) Delete Table(s)..." "\n6) Quit\n")
    choice = input(">  ")
    if choice == '1':
      create_tables()
      print("Tables created.")

    elif choice == '2':
      populate_tables()
      print("Tables populated with default values.")

    elif choice == '3':
      while True:
        print("\nWhich table would you like to insert into?", "\n1) Courses", "\n2) Students", "\n3) Courses Has Students", "\n4) Quit")
        choice = input(">  ")
        if choice == '1':
          insert_courses()
          break
        elif choice == '2': 
          insert_students()
          break
        elif choice == '3':
          insert_courses_has_students()
          break
        elif choice == '4':
          break
        else:
          print("Please enter a choice 1-3.")

    elif choice == '4':
      while True:
        print("\nDisplay...", "\n1) Courses", "\n2) Students", "\n3) Student's Schedule", "\n4) All Tables", "\n5) Quit")
        choice = input(">  ")
        if choice == '1':
          display_courses()
          break
        elif choice == '2':
          display_student_info()
          break
        elif choice == '3':
          display_student_courses()
          break
        elif choice == '4':
          display_tables()
          break
        elif choice == '5':
          break
        else:
          print("Please enter a choice 1-5.")

    elif choice == '5':
      while True:
        print("\nWhich table would you like to delete?", "\n1) Courses", "\n2) Students", "\n3) Courses Has Students", "\n4) All Tables", "\n5) Quit")
        choice = input(">  ")
        if choice == '1':
          connection.execute('DELETE FROM courses')
          break
        elif choice == '2':
          connection.execute('DELETE FROM students')
          break
        elif choice == '3':
          connection.execute('DELETE FROM courses_has_students')
          break
        elif choice == '4':
          connection.execute('DELETE FROM courses')
          connection.execute('DELETE FROM students')
          connection.execute('DELETE FROM courses_has_students')
          break
        elif choice == '5':
          break
        else:
          print("Please enter a choice 1-5.")
      
      connection.commit()

    elif choice == '6':
      break
    else:
      print("Please enter a choice 1-6.")

  print("\n")
  connection.close()