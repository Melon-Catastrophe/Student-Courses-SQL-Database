# Overview

I have learned somewhat recently about SQL Databases, which I find very interesting. I decided that I wanted to make a program in Python that can make and interact with a database, so I made this to increase my skill set in both Python and SQL as well as to show myself that I can make cool programs.

This is a program I made in Python that is able to read and write from an SQL Relational Database. The database stores information about students, courses, and the particular courses that each student is taking. 

To start the program, you can either run the main.py file or you can run the .exe file that was compiled. When it runs, you will see some options. These options are: 
1) Create Tables
2) Populate Tables
3) Insert into Table...
4) Display...
5) Delete...
6) Quit

A user can create and populate the tables with default values, display individual tables or all of the tables in the database, insert data into individual tables, delete a specific entry in a table, delete all tables, or quit. The options with a '...' have more specific options that will show after being selected. 

Sometimes, the program will ask for text input. An example of this occurs when deleting a specific entry from a table. Simply type the text that it asks for. If unsure what to type, just hit enter and you will see a messing telling you what the program expects.

[Link to Demo Video](https://youtu.be/m8JAX_JKE14)

# Relational Database

I am using a relational database that I created. I created it using SQLite. There is an option in the code to re-create and populate the tables back to their default values. 

There are three tables in this student_courses.db database: students, courses, and courses_has_students. The tables 'courses' and 'students' are joined in a many to many relationship using a bridge table called 'courses_has_students'. This junction table allows information to be stored about the courses that each individual student is taking.

# Development Environment

I coded this program in Python using Visual Studio Code. I used the libraries SQLite and Tabulate to help me create this. Pyinstaller was used to create an .exe of the file so that anyone can run it without needing to download Python. 

# Useful Websites

* [Stack Overflow](https://stackoverflow.com/)
* [W3 Schools - Python](https://www.w3schools.com/python/)
* [W3 Schools - SQL](https://www.w3schools.com/sql/)

# Future Work

Known bugs and improvements to be made:
* A GUI would be nice, but the program would still function in more or less the same way.
* Entering multiple words or very long words can sometimes overload the program and cause it to stop. 
* It would be cool if the program could be changed so that the text that is displayed is cleared from the window and replaced with the relevant text. For instance, going into a submenu could clear the screen and show just the submenu. I believe this could be accomplished using the curses library. 