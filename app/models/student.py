from app import mysql
import cloudinary

# Update the get_students function in your Python code
# Update the SQL query in get_students function
def get_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT s.*, c.name AS course_name, co.name AS college_name, co.code AS college_code FROM student s LEFT JOIN course c ON s.course_code = c.code LEFT JOIN college co ON c.college_code = co.code")
    students = cur.fetchall()
    cur.close()
    return students

def get_courses():
    cur = mysql.connection.cursor()
    cur.execute("SELECT code FROM course")
    courses = cur.fetchall()
    cur.close()
    return courses

def add_student(id, firstname, lastname, course_code, year, gender, cloudinary_image_url):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO student (id, firstname, lastname, course_code, year, gender, cloudinary_image_url) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (id, firstname, lastname, course_code, year, gender, cloudinary_image_url)
    )
    mysql.connection.commit()
    cur.close()

def is_student_id_unique(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM student WHERE id = %s", (id,))
    count = cur.fetchone()[0]
    cur.close()
    return count == 0

def get_student_by_id(student_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE id = %s", (student_id,))
    student = cur.fetchone()
    cur.close()
    return student

def update_student(original_student_id, student_id, firstname, lastname, course_code, year, gender, cloudinary_image_url=None):
    cur = mysql.connection.cursor()
    if cloudinary_image_url:
        cur.execute(
            "UPDATE student SET id = %s, firstname = %s, lastname = %s, course_code = %s, year = %s, gender = %s, cloudinary_image_url = %s WHERE id = %s",
            (student_id, firstname, lastname, course_code, year, gender, cloudinary_image_url, original_student_id))
    else:
        cur.execute(
            "UPDATE student SET id = %s, firstname = %s, lastname = %s, course_code = %s, year = %s, gender = %s WHERE id = %s",
            (student_id, firstname, lastname, course_code, year, gender, original_student_id))
    mysql.connection.commit()
    cur.close()

def check_student_id_exists(student_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE id = %s", (student_id,))
    result = cur.fetchone()
    cur.close()
    return result is not None

def delete_student(student_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT cloudinary_image_url FROM student WHERE id = %s", (student_id,))
    result = cur.fetchone()
    if result:
        # Get the current student's photo public ID
        current_photo_url = result[0]
        current_public_id = current_photo_url.split('/')[-1].split('.')[0]

        # Delete the current photo in Cloudinary
        delete_cloudinary_resource(current_public_id)

    # Now, delete the student from the database
    cur.execute("DELETE FROM student WHERE id = %s", (student_id,))
    mysql.connection.commit()
    cur.close()

def search_students(search_by, search_term):
    cur = mysql.connection.cursor()

    if search_by == 'id':
        cur.execute("SELECT s.*, c.name AS course_name, co.name AS college_name, co.code AS college_code FROM student s LEFT JOIN course c ON s.course_code = c.code LEFT JOIN college co ON c.college_code = co.code WHERE s.id LIKE %s", ('%' + search_term + '%',))
    elif search_by == 'firstname':
        cur.execute("SELECT s.*, c.name AS course_name, co.name AS college_name, co.code AS college_code FROM student s LEFT JOIN course c ON s.course_code = c.code LEFT JOIN college co ON c.college_code = co.code WHERE s.firstname LIKE %s", ('%' + search_term + '%',))
    elif search_by == 'lastname':
        cur.execute("SELECT s.*, c.name AS course_name, co.name AS college_name, co.code AS college_code FROM student s LEFT JOIN course c ON s.course_code = c.code LEFT JOIN college co ON c.college_code = co.code WHERE s.lastname LIKE %s", ('%' + search_term + '%',))
    elif search_by == 'course_code':
        cur.execute("SELECT s.*, c.name AS course_name, co.name AS college_name, co.code AS college_code FROM student s LEFT JOIN course c ON s.course_code = c.code LEFT JOIN college co ON c.college_code = co.code WHERE s.course_code LIKE %s OR c.name LIKE %s", ('%' + search_term + '%', '%' + search_term + '%'))
    elif search_by == 'college_code':  # Add search option for college code
        cur.execute("SELECT s.*, c.name AS course_name, co.name AS college_name, co.code AS college_code FROM student s LEFT JOIN course c ON s.course_code = c.code LEFT JOIN college co ON c.college_code = co.code WHERE co.code LIKE %s OR co.name LIKE %s", ('%' + search_term + '%', '%' + search_term + '%'))
    elif search_by == 'year':
        cur.execute("SELECT s.*, c.name AS course_name, co.name AS college_name, co.code AS college_code FROM student s LEFT JOIN course c ON s.course_code = c.code LEFT JOIN college co ON c.college_code = co.code WHERE s.year = %s", (int(search_term),))
    elif search_by == 'gender':
        cur.execute("SELECT s.*, c.name AS course_name, co.name AS college_name, co.code AS college_code FROM student s LEFT JOIN course c ON s.course_code = c.code LEFT JOIN college co ON c.college_code = co.code WHERE LOWER(s.gender) = LOWER(%s)", (search_term,))

    students = cur.fetchall()
    cur.close()
    return students






def delete_cloudinary_resource(public_id):
    """Delete a resource in Cloudinary based on its public ID."""
    try:
        cloudinary.api.delete_resources([public_id])
        return True
    except Exception as e:
        print(f"Error deleting Cloudinary resource: {e}")
        return False