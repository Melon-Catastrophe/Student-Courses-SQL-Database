import sqlite3
from tabulate import tabulate

connection = sqlite3.connect('student_courses.db')
cursor = connection.cursor()

def create_tables():
  # This function creates the necessary tables in the database. It will drop the table before creation if it exists.

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


def populate_tables():
  # This function populates the tables with example default data.

  # Calls create_tables before population in order to clean up the primary keys.
  create_tables()

  # Inserts data about courses into table.
  values = (('CSE310', 'Applied Programming'), ('CIT171', 'Intro to Cybersecurity'), ('ECEN106', 'Computer Systems'), ('CIT111', 'Intro to Databases'), ('CSE150', 'Data Intuition and Insight'), ('CSE210', 'Programming with Classes'), ('GE101', 'College Success'))
  for i in range(len(values)):
    connection.execute('INSERT INTO courses (c_id, name) VALUES (?, ?)', values[i])
    connection.commit()

  # Inserts data about students into table.
  values = (('Will', 'Smith', '555-267-9928'), ('Tim', 'Willards', '267-543-7731'))
  for i in range(len(values)):
    connection.execute('INSERT INTO students (fname, lname, phone) VALUES (?, ?, ?)', values[i])
    connection.commit()

  # Inserts data about what students are enrolled in what classes into table.
  values = ((2, 1), (3, 1), (4, 1), (7, 1), (1, 2), (4, 2), (5, 2), (6, 2))
  for i in range(len(values)):
    connection.execute('INSERT INTO courses_has_students (courses_id, students_id) VALUES (?, ?)', values[i])
    connection.commit()


def display_tables():
  # This function displays all of the tables in the database. I did not use tabulate when displaying all tables so that the user could clearly see the keys of the database entries.
  
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
  # This function prompts the user for the first name of a student, then displays the courses that student is enrolled in.

  while True:
    print("\nWhat is the first name of the student whose courses you would like to view?")
    stu_name = input(">  ")

    # Checks to see if the input matches a student's name in the table.
    values = (stu_name.lower(), )
    cursor.execute('SELECT fname FROM students WHERE LOWER(students.fname) = ?', values)
  
    # This section breaks out of the loop if there is a student with that first name.
    if cursor.fetchone() != None:
      break
    else:
      print("Name not found. Please enter a student's name.")
  
  cursor.execute('SELECT c.c_id, c.name FROM students JOIN courses_has_students cs ON students.id = cs.students_id JOIN courses c ON cs.courses_id = c.id WHERE LOWER(students.fname) = ?', values)
  
  # Adds data to a list, then prints it into a table using tabulate.
  table = []
  for line in cursor.fetchall():
    table.append(list(line))
  print("\n", tabulate(table, headers=[stu_name.capitalize() + ''''s Courses''']))


def display_student_info():
  # This function displays the courses a student is enrolled in using tabulate.

  cursor.execute('SELECT fname, lname, phone FROM students ORDER BY fname')
  
  # Adds data to a list, then prints it into a table using tabulate.
  table = []
  for line in cursor.fetchall():
    table.append(list(line))
  print("\n", tabulate(table, headers=["First Name", "Last Name", "Phone Number"]))


def display_courses():
  # This function displays the courses in the database using tabulate.

  cursor.execute("SELECT c_id, name FROM courses ORDER BY courses.c_id")

  # Adds data to a list, then prints it into a table using tabulate.
  table = []
  for line in cursor.fetchall():
    table.append(list(line))
  print("\n", tabulate(table, headers=["Course ID", "Course Name"]))


def insert_courses():
  # This function allows a user to insert a course into the database. 

  new_c_id = input("\nPlease enter a course id.\n>  ")
  new_c_name = input("\nPlease enter a course name.\n>  ")
  
  values = (new_c_id, new_c_name)
  connection.execute('INSERT INTO courses (c_id, name) VALUES (?, ?)', values)
  connection.commit()


def insert_students():
  # This function allows a user to insert a student into the database. 

  new_fname = input("\nPlease enter the student's first name.\n>  ")
  new_lname = input("\nPlease enter the student's last name.\n>  ")
  new_phone = input("\nPlease enter the student's phone number using the format '123-456-6789'.\n>  ")
  
  values = (new_fname, new_lname, new_phone)
  connection.execute('INSERT INTO students (fname, lname, phone) VALUES (?, ?, ?)', values)
  connection.commit()


def insert_courses_has_students():
  # This function allows a user to insert data for what courses a student is taking into the database. 

  # It is important that the user inputs an integer corresponding to a primary key of the course and the student. While loops are used to ensure that inputted data is an integer data type. 
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
  # This function deletes all data within a selected table.

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
  # This function deletes a selected entry of a table.
  
  while True:
    # Prompts for name of table and checks if table exists. 
    print("\nType the name of the table you would like to delete from.")
    table_name = input(">  ")
    values = (table_name, )
    cursor.execute(''' SELECT name FROM sqlite_master WHERE type = 'table' AND name = (?) ''', values)
    
    try:
      # If the table exists, then it will extract the data from that table into the list 'table'.
      if cursor.fetchone()[0] == table_name:
        query = 'SELECT * FROM ' + table_name
        cursor.execute(query)
        
        table = []
        for line in cursor.fetchall():
          table.append(list(line))

        # Depending on which table was selected, the data needs to be shown differently. These statements display each entry in the table and prompts the user for which entry they would like to delete, which is stored in variable 'choice'.
        if table_name == 'students':
          print("\n", tabulate(table, headers=["ID", "First Name", "Last Name", "Phone Number"]))
          choice = input("\nWhat is the ID of the entry that you would like to delete?\n>  ")
       
        elif table_name == 'courses':
          print("\n", tabulate(table, headers=["ID", "Course ID", "Course Name"]))
          choice = input("\nWhat is the ID of the entry that you would like to delete?\n>  ")
       
        elif table_name == 'courses_has_students':
          # Inserts arbitrary IDs into the tabulate table (the table that is displayed, not the database table) to make it easier for the user to select an entry to delete.
          for i in range(len(table)):
            table[i].insert(0, i)
          print("\n", tabulate(table, headers=["Line Number", "Courses ID", "Student ID"]))
          
          while True:
            try:
              choice = int(input("\nWhat is the Line Number of the entry that you would like to delete?\n>  "))
              if type(choice) == int and choice in range(len(table)):
                break
              else:
                print("Please enter a line number.")
            except ValueError or IndexError:
              print("Please enter a line number.")
            

        values = (choice, )
        # Because the tables 'courses' and 'students' have data corresponding to two tables, we must first delete the data in its own table first before deleting its corresponding data in the 'courses_has_students' table.
        if table_name == 'students' or table_name == 'courses':
          query = 'DELETE FROM ' + table_name + ' WHERE id = (?)'
          connection.execute(query, values)
        

        # The following code will delete corresponding entries in the courses_has_students table.
        if table_name == 'courses_has_students':
          query = 'DELETE FROM courses_has_students WHERE courses_id = (?) AND students_id = (?)'
          # Sets values to the IDs that were displayed in the tabulate table. 
          values = (table[choice][1], table[choice][2])
        elif table_name == 'students':
          query = 'DELETE FROM courses_has_students WHERE students_id = (?)'
        elif table_name == 'courses':
          query = 'DELETE FROM courses_has_students WHERE courses_id = (?)'
        connection.execute(query, values)
        connection.commit()
        break

    # If the table name input is not a table name, then it will throw a TypeError.
    except TypeError:
      print("Please enter one of three table names: courses, students, or courses_has_students.")


# This is the main function that runs. It displays some options, and asks the user for an input to modify the database.
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
      # Displays the insert options and calls appropriate functions.
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
      # Displays the display options and calls the appropriate functions.
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
      # Displays the delete options and calls appropriate functions.
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