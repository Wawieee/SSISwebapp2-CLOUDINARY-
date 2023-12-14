from flask import render_template, request, redirect, url_for, flash
from app import app, cloudinary
import cloudinary
import cloudinary.uploader
import cloudinary.api
from app.models.course import get_courses, add_course, get_course_by_code, update_course, delete_course, search_courses, check_course_code_exists, get_courses_with_college
from app.models.student import get_students, add_student, get_student_by_id, update_student, delete_student, search_students, check_student_id_exists, delete_cloudinary_resource
from app.models.college import get_colleges, add_college, get_college_by_code, update_college, delete_college, search_colleges, check_college_code_exists

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    students = get_students()
    return render_template('student.html', students=students, courses=get_courses())
    
@app.route('/add_student', methods=['GET', 'POST'])
def add_student_route():
    if request.method == 'POST':
        id = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        course_code = request.form['course_code']
        year = request.form['year']
        gender = request.form['gender']
        photo = request.files['photo']


        existing_student = get_student_by_id(id)
        if existing_student:
            flash(f'Student with ID {id} already exists!', 'warning')
            return render_template('add_student.html', courses=get_courses(), id=id, firstname=firstname, lastname=lastname, course_code=course_code, year=year, gender=gender)
  
        # Check if a photo is provided
        if photo:
            # Upload photo to Cloudinary
            cloudinary_response = cloudinary.uploader.upload(photo)
            cloudinary_image_url = cloudinary_response['secure_url']
        else:
            # Use a placeholder photo if no photo is provided
            cloudinary_image_url = "/static/profile_placeholder.png"

        add_student(id, firstname, lastname, course_code, year, gender, cloudinary_image_url)
        flash(f'Student successfully added!', 'success')
        return redirect('/students')

    return render_template('add_student.html', courses=get_courses())

@app.route('/edit_student/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'GET':
        student = get_student_by_id(student_id)
        courses = get_courses()
        return render_template('edit_student.html', student=student, courses=courses)
    elif request.method == 'POST':
        student_id_input = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        course_code = request.form['course_code']
        year = request.form['year']
        gender = request.form['gender']

        if student_id_input != student_id:
            if check_student_id_exists(student_id_input):
                flash('ID already exists. Please choose a different ID.', 'warning')
                return redirect(url_for('edit_student', student_id=student_id))

        # Check if a new photo is uploaded
        if 'photo' in request.files:
            photo = request.files['photo']

            # If the file input is not empty, update the photo
            if photo.filename != '':
                # Get the current student's photo public ID
                current_photo_url = get_student_by_id(student_id)[6]
                current_public_id = current_photo_url.split('/')[-1].split('.')[0]

                # Delete the current photo in Cloudinary
                delete_cloudinary_resource(current_public_id)

                # Upload the new photo to Cloudinary
                cloudinary_response = cloudinary.uploader.upload(photo)
                cloudinary_image_url = cloudinary_response['secure_url']

                # Update the student information with the new photo
                update_student(student_id, student_id_input, firstname, lastname, course_code, year, gender, cloudinary_image_url)
                flash('Student information successfully updated!', 'success')
                return redirect(url_for('students'))

        # If no new photo is uploaded, update the student information without changing the photo
        update_student(student_id, student_id_input, firstname, lastname, course_code, year, gender)
        flash('Student information successfully updated!', 'success')
        return redirect(url_for('students'))

@app.route('/delete_student/<student_id>')
def delete_student_route(student_id):
    delete_student(student_id)
    flash(f'Student successfully deleted!', 'success')
    return redirect('/students')

@app.route('/search_student', methods=['POST'])
def search_student():
    search_by = request.form['search_by']
    search_term = request.form['search_term']
    
    students = search_students(search_by, search_term)
    return render_template('student.html', students=students)

@app.route('/colleges')
def colleges():
    colleges = get_colleges()
    return render_template('college.html', colleges=colleges)

@app.route('/add_college', methods=['GET', 'POST'])
def add_college_route():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']

        if check_college_code_exists(code):
            flash(f'College with code {code} already exists!', 'warning')
            return render_template('add_college.html')
        else:
            add_college(code, name)
            flash(f'College successfully added!', 'success')
        
        return redirect('/colleges')
    return render_template('add_college.html')

@app.route('/search_college', methods=['POST'])
def search_college():
    search_by = request.form['search_by']
    search_term = request.form['search_term']

    colleges = search_colleges(search_by, search_term)

    return render_template('college.html', colleges=colleges)

@app.route('/edit_college/<college_code>', methods=['GET', 'POST'])
def edit_college(college_code):
    if request.method == 'GET':
        college = get_college_by_code(college_code)
        return render_template('edit_college.html', college=college)
    elif request.method == 'POST':
        name = request.form['name']
        new_college_code = request.form['code']

        if new_college_code != college_code and check_college_code_exists(new_college_code):
            flash('College code already exists. Please choose a different code.', 'warning')
            return redirect(url_for('edit_college', college_code=college_code))

        update_college(college_code, new_college_code, name)
        flash('College successfully updated!', 'success')

        return redirect(url_for('colleges'))

@app.route('/delete_college/<code>')
def delete_college_route(code):
    delete_college(code)
    flash(f'College successfully deleted!', 'success')
    return redirect('/colleges')

"""
@app.route('/courses')
def courses():
    courses = get_courses_with_college()
    return render_template('course.html', courses=courses)
"""
@app.route('/courses')
def courses():
    courses = get_courses()
    colleges = get_colleges()
    return render_template('course.html', courses=courses, colleges=colleges)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course_route():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        college_code = request.form['college_code']

        existing_course = get_course_by_code(code)
        if existing_course:
            flash(f'Course with code {code} already exists!', 'warning')
            colleges = get_colleges()
            return render_template('add_course.html', colleges=colleges)
        else:
            add_course(code, name, college_code)
            flash(f'Course successfully added!', 'success')
        
        return redirect('/courses')
    colleges = get_colleges()
    return render_template('add_course.html', colleges=colleges)



@app.route('/search_course', methods=['POST'])
def search_course():
    search_by = request.form['search_by']
    search_term = request.form['search_term']

    courses = search_courses(search_by, search_term)

    return render_template('course.html', courses=courses)

@app.route('/edit_course/<course_code>', methods=['GET', 'POST'])
def edit_course(course_code):
    if request.method == 'GET':
        course = get_course_by_code(course_code)
        colleges = get_colleges()
        return render_template('edit_course.html', course=course, colleges=colleges)
    elif request.method == 'POST':
        name = request.form['name']
        new_course_code = request.form['code']
        college_code = request.form['college_code']

        if new_course_code != course_code and check_course_code_exists(new_course_code):
            flash('Course code already exists. Please choose a different code.', 'warning')
            return redirect(url_for('edit_course', course_code=course_code))

        update_course(course_code, new_course_code, name, college_code)
        flash('Course successfully updated!', 'success')

        return redirect(url_for('courses'))

@app.route('/delete_course/<code>')
def delete_course_route(code):
    delete_course(code)
    flash(f'Course successfully deleted!', 'success')
    return redirect('/courses')