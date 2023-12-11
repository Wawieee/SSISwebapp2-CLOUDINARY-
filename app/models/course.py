from app import mysql

def get_courses():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM course")
    courses = cur.fetchall()
    cur.close()
    return courses

def add_course(code, name, college_code):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO course (code, name, college_code) VALUES (%s, %s, %s)",
                (code, name, college_code))
    mysql.connection.commit()
    cur.close()

def get_course_by_code(course_code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM course WHERE code = %s", (course_code,))
    course = cur.fetchone()
    cur.close()
    return course

def update_course(old_course_code, new_course_code, name, college_code):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE course SET code = %s, name = %s, college_code = %s WHERE code = %s", (new_course_code, name, college_code, old_course_code))
    mysql.connection.commit()
    cur.close()

def check_course_code_exists(course_code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM course WHERE code = %s", (course_code,))
    count = cur.fetchone()[0]
    cur.close()
    return count > 0

def delete_course(code):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM course WHERE code = %s", (code,))
    mysql.connection.commit()
    cur.close()

def search_courses(search_by, search_term):
    cur = mysql.connection.cursor()
    if search_by == 'code':
        cur.execute("SELECT * FROM course WHERE code LIKE %s", ('%' + search_term + '%',))
    elif search_by == 'name':
        cur.execute("SELECT * FROM course WHERE name LIKE %s", ('%' + search_term + '%',))
    elif search_by == 'college_code':
        cur.execute("SELECT * FROM course WHERE college_code = %s", (search_term,))
    courses = cur.fetchall()
    cur.close()
    return courses

def get_courses_with_college():
    cur = mysql.connection.cursor()
    cur.execute("SELECT course.code, course.name, course.college_code, college.name FROM course JOIN college ON course.college_code = college.code")
    courses = cur.fetchall()
    cur.close()
    return courses
