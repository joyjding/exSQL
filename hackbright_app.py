#Connecting SQL to Python
#7_02_13
#Joy Ding and Katherine Hennes

import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students2 WHERE github = ?"""
    DB.execute(query, (github,)) # Must be tuple even if only one value is subbed
    row = DB.fetchone()
    print """\
    Student: %s %s
    Github account: %s"""%(row[0], row[1], row[2])

def get_project_by_title(title):
    query = """SELECT title, description, max_grade FROM Projects2 WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
    Project: %s
    Description %s
    Max Grade: %d""" % (row[0], row[1], row[2]) 

def get_grade_by_project(title):
    query = """SELECT Projects2.title, Grades2.grade 
    FROM Projects2 INNER JOIN Grades2 
    ON Grades2.project_title = Projects2.title 
    WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print "OK"
    print """\
    Project: %s
    Grade: %d""" %(row[0], row[1])

def update_grade(grade, project_title, student_github):
    query = """UPDATE Grades2 SET grade=? WHERE student_github=? and project_title=?"""
    DB.execute(query, (grade, student_github, project_title))
    CONN.commit()
    print "Successfully added %s's grade for %s: %d " %(student_github, project_title, int(grade)) 

def get_grades_by_student(first_name, last_name):
    query = """SELECT S.first_name, S.last_name, P.title, G.grade
    FROM Grades2 G
    JOIN Students2 S ON (S.github = G.student_github)
    JOIN Projects2 P ON (G.project_title = P.title)
    WHERE S.first_name = ? and S.last_name = ?"""

    DB.execute(query, (first_name, last_name))
    rows=DB.fetchall()
    
    print "\tStudent: %s %s" % (first_name, last_name)
    for row in rows:
        print """\
        \tProject: %s
        \t\tGrade: %d""" % (row[2], row[3])

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students2 values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" %(first_name, last_name)

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects2 values (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s %s" % (title, description)

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("my_database.db") # DB connection executes queries
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(", ")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "grade":
            get_grade_by_project(*args)
        elif command == "new_grade":
            update_grade(*args)
        elif command == "get_grades":
            get_grades_by_student(*args)

    CONN.close()

if __name__ == "__main__":
    main()
