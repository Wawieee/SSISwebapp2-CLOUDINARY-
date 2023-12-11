from app import mysql

def get_colleges():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM college")
    colleges = cur.fetchall()
    cur.close()
    return colleges

def add_college(code, name):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO college (code, name) VALUES (%s, %s)", (code, name))
    mysql.connection.commit()
    cur.close()

def get_college_by_code(college_code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM college WHERE code = %s", (college_code,))
    college = cur.fetchone()
    cur.close()
    return college

def check_college_code_exists(code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM college WHERE code = %s", (code,))
    result = cur.fetchone()
    cur.close()
    return result is not None

def update_college(old_college_code, new_college_code, name):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE college SET code = %s, name = %s WHERE code = %s", (new_college_code, name, old_college_code))
    mysql.connection.commit()
    cur.close()

def delete_college(code):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM college WHERE code = %s", (code,))
    mysql.connection.commit()
    cur.close()

def search_colleges(search_by, search_term):
    cur = mysql.connection.cursor()
    if search_by == 'code':
        cur.execute("SELECT * FROM college WHERE code LIKE %s", ('%' + search_term + '%',))
    elif search_by == 'name':
        cur.execute("SELECT * FROM college WHERE name LIKE %s", ('%' + search_term + '%',))
    colleges = cur.fetchall()
    cur.close()
    return colleges
