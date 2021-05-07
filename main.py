import sqlite3
from tabulate import tabulate

connection = sqlite3.connect('student_courses.db')
cursor = connection.cursor()

# This function creates the necessary tables in the database. It will drop the table before creation if it exists.
def create_tables():
  # If a table exists, it drops it.
  connection.execute('DROP TABLE IF EXISTS courses')
  connection.execute('DROP TABLE IF EXISTS students')
  connection.execute('DROP TABLE IF EXISTS courses_has_students')
  connection.commit()
  
  # Creation of tables.
  connection.execute('CREATE TABLE courses (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, c_id VARCHAR(10) NOT NULL, name TEXT NOT NULL);')
  connection.execute('CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, fname TEXT NOT NULL, lname TEXT NOT NULL, phone VARCHAR(12))')
  connection.execute('CREATE TABLE courses_has_students (courses_id VARCHAR(10) NOT NULL, students_id TEXT NOT NULL, PRIMARY KEY (courses_id, students_id))')
  connection.commit()


# This function will populate the tables with example default data.
# It also runs create_tables before population in order to clean up the primary keys. 
def populate_tables():
  create_tables()

  # connection.execute('DELETE FROM courses')
  # connection.execute('DELETE FROM students')
  # connection.execute('DELETE FROM courses_has_students')
  # connection.commit()

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
  
    # This section breaks out of the loop if there is a student with that first name.
    if cursor.fetchone() != None:
      break
    else:
      print("Name not found. Please enter a student's name.")
  
  cursor.execute('SELECT c.c_id, c.name FROM students JOIN courses_has_students cs ON students.id = cs.students_id JOIN courses c ON cs.courses_id = c.id WHERE LOWER(students.fname) = ?', values)
  
  table = []
  for line in cursor.fetchall():
    table.append(list(line))
  print("\n", tabulate(table, headers=[stu_name.capitalize() + ''''s Courses''']))


def display_student_info():
  cursor.execute('SELECT fname, lname, phone FROM students ORDER BY fname')
  
  table = []
  for line in cursor.fetchall():
    table.append(list(line))

  print("\n", tabulate(table, headers=["First Name", "Last Name", "Phone Number"]))


def display_courses():
  cursor.execute("SELECT c_id, name FROM courses ORDER BY courses.c_id")

  table = []
  for line in cursor.fetchall():
    table.append(list(line))

  print("\n", tabulate(table, headers=["Course ID", "Course Name"]))


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


def delete_table():
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


def delete_entry():
  while True:
    print("\nType the name of the table you would like to delete from.")
    table_name = input(">  ")
    values = (table_name, )
    cursor.execute(''' SELECT name FROM sqlite_master WHERE type = 'table' AND name = (?) ''', values)
    
    try:
      if cursor.fetchone()[0] == table_name:
        query = 'SELECT * FROM ' + table_name
        cursor.execute(query)
        
        table = []
        for line in cursor.fetchall():
          table.append(list(line))

        if table_name == 'students':
          print("\n", tabulate(table, headers=["ID", "First Name", "Last Name", "Phone Number"]))
          choice = input("\nWhat is the ID of the entry that you would like to delete?\n>  ")
        elif table_name == 'courses':
          print("\n", tabulate(table, headers=["ID", "Course ID", "Course Name"]))
          choice = input("\nWhat is the ID of the entry that you would like to delete?\n>  ")
        elif table_name == 'courses_has_students':
          for i in range(len(table)):
            table[i].insert(0, i)
          print("\n", tabulate(table, headers=["Line Number", "Courses ID", "Student ID"]))
          choice = input("\nWhat is the Line Number of the entry that you would like to delete?\n>  ")
          
        while True:
          choice = int(choice)    # Be sure to determine whether it is an int or not. Or maybe whether or not it successfully deletes. 
          break
        
        values = (choice, )
        query = 'DELETE FROM ' + table_name + ' WHERE id = (?)'

        if table_name == 'courses_has_students':
          query = 'DELETE FROM courses_has_students WHERE courses_id = (?) AND students_id = (?)'
          values = (table[choice][1], table[choice][2])
        
        connection.execute(query, values)
        if table_name == 'students':
          connection.execute('DELETE FROM courses_has_students WHERE students_id = (?)', values)
        elif table_name == 'courses':
          connection.execute('DELETE FROM courses_has_students WHERE courses_id = (?)', values)

        connection.commit()
        break

    except TypeError:     # If the input is not a table name, then it will throw a TypeError.
      print("Please enter one of three table names: courses, students, or courses_has_students.")


if __name__ == '__main__':
  print("Welcome to Database Manager")
  
  while True:
    print("\n1) Create Tables", "\n2) Populate Tables", "\n3) Insert into Table...", "\n4) Display...", "\n5) Delete..." "\n6) Quit\n")
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
      print("\nWould you like to delete 1) tables, or 2) table entries?")
      choice = input(">  ")
      if choice == '1':
        delete_table()
      elif choice == '2':
        delete_entry()
        
      else:
        print("Please enter a choice 1-2.")

    elif choice == '6':
      break
    else:
      print("Please enter a choice 1-6.")

  print("\n")
  connection.close()