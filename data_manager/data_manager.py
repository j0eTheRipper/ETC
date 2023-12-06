import sqlite3
import os

from data_manager.common_f import connect_to_db
from data_manager.user_functions.user_management import __generate_new_user_query


def view_all_tutors():
    cursor, database = connect_to_db()

    tutors = cursor.execute("SELECT * FROM tutors;").fetchall()
    return tutors


def get_subject(username):
    database = sqlite3.connect("data.sqlite")
    cursor = database.cursor()
    stu_classes = cursor.execute(f'SELECT subjects FROM students WHERE name="{username}";').fetchone()[0]
    return stu_classes


def view_all_students(tutor=''):
    cursor, database = connect_to_db()
    student_list = []

    if tutor:
        tutor_info = cursor.execute(f'SELECT subject, level FROM tutors WHERE name="{tutor}";').fetchone()
        subjects = tutor_info[0].split("-")
        level = tutor_info[1]
        for subject in subjects:
            subject_students = cursor.execute(f'SELECT name FROM students WHERE subjects LIKE "%{subject}%" and level={level};').fetchall()
            student_list.extend([i[0] for i in subject_students])
    else:
        student_list = [i[0] for i in cursor.execute(f'SELECT name FROM students;').fetchall()]

    return student_list


def request_subject_change(name, subject, new_subject):
    cursor, database = connect_to_db()
    student = cursor.execute(f'SELECT * FROM students WHERE name="{name}";').fetchone()
    student_subjects = student[1].split("-")
    student_has_pending_request = student[6]
    if student_has_pending_request:
        return "student has pending requests"

    if subject in student_subjects and new_subject not in student_subjects:
        cursor.execute(f'UPDATE students SET pending_request="{subject}>{new_subject}" WHERE name="{name}";')
        database.commit()

    database.close()


def view_subject_change_requests(username):
    cursor, database = connect_to_db()
    role = cursor.execute(f'select role from users where username="{username}";').fetchone()
    if role == "student":
        pending_requests = cursor.execute(f'SELECT name, pending_request FROM students WHERE username="{username}";').fetchall()
    else:
        pending_requests = cursor.execute('SELECT name, pending_request FROM students;').fetchall()
    return pending_requests


def handle_pending_request(student, is_accept):
    cursor, database = connect_to_db()
    current_subjects, pending_request = cursor.execute(f'SELECT subjects, pending_request FROM students WHERE name="{student}";').fetchone()
    if is_accept:
        old_subject, new_subject = pending_request.split(">")
        current_subjects = current_subjects.split("-")
        current_subjects.remove(old_subject)
        current_subjects.append(new_subject)
        current_subjects = '-'.join(current_subjects)
        cursor.execute(f'UPDATE students SET subjects="{current_subjects}", pending_request=NULL WHERE name="{student}";')
    else:
        cursor.execute(f'UPDATE students SET pending_request=NULL WHERE name="{student}";')

    database.commit()
    database.close()


def view_fees(username=""):
    cursor, database = connect_to_db()
    if username:
        student_fees = cursor.execute(f'SELECT fees, payment_status FROM students WHERE name="{username}";').fetchone()
    else:
        student_fees = cursor.execute(f'SELECT name, fees, payment_status FROM students;').fetchall()

    return student_fees


def pay_fees(username):
    cursor, database = connect_to_db()
    cursor.execute(f'UPDATE students SET payment_status="pending" WHERE name="{username}";')
    database.commit()
    database.close()


def accept_payment(username):
    cursor, database = connect_to_db()
    cursor.execute(f'UPDATE students SET payment_status="success" WHERE name="{username}";')
    database.commit()
    database.close()


def add_class(tutor_name, time):
    cursor, database = connect_to_db()

    tutor, level, subject = (cursor.execute(f'SELECT name, level, subject FROM tutors WHERE name="{tutor_name}";').
                             fetchone())

    cursor.execute(f'INSERT INTO classes (subject, level, tutor, time) VALUES ("{subject}", {level}, "{tutor}", "{time}");')
    database.commit()
    database.close()


def view_classes(username):
    cursor, database = connect_to_db()

    user_role = cursor.execute(f'SELECT role FROM users WHERE username="{username}";').fetchone()[0]
    classes = []
    if user_role == 'student':
        student_info = cursor.execute(f'SELECT * FROM students WHERE name="{username}";').fetchone()
        subjects = student_info[1].split("-")
        for i in subjects:
            classes.append(cursor.execute(f'SELECT subject, tutor, time from classes WHERE level={student_info[2]} AND subject="{i}";').fetchall())
    elif user_role == 'tutor':
        return cursor.execute(f'SELECT * FROM classes WHERE tutor="{username}";').fetchall()
    return classes


def update_class(class_id, new_date=None):
    cursor, database = connect_to_db()
    class_data = cursor.execute(f'SELECT * FROM classes WHERE "class-id"={class_id}').fetchone()
    if class_data:
        if new_date:
            cursor.execute(f'UPDATE classes SET time="{new_date}" WHERE "class-id"={class_id};')
        else:
            cursor.execute(f'DELETE FROM classes WHERE "class-id"={class_id};')

    database.commit()
    database.close()


def view_income():
    cursor, database = connect_to_db()

    students_fees = [i[0] for i in cursor.execute('SELECT fees FROM students WHERE payment_status="success";').fetchall()]
    tutors_income = [i[0] for i in cursor.execute('SELECT salary FROM tutors;').fetchall()]

    return sum(students_fees), sum(tutors_income)


def init_db():
    """Deletes the current database and creates a new one, and makes a default admin account"""
    if os.path.exists("data.sqlite"):
        os.remove("data.sqlite")

    cursor, database = connect_to_db()
    with open('data_manager\\schema.sql', 'r') as schema:
        script = schema.read()
    cursor.executescript(script)

    default_subjects = {"english", "computer", "bahasa melayu", "math", "physics", "chemistry", "biology"}
    for subject in default_subjects:
        cursor.execute(f'INSERT INTO subjects VALUES ("{subject}");')

    new_user = __generate_new_user_query("defaultadmin", "admin@etc.mail", "pleasechange123", "admin")[0]
    cursor.execute(new_user)
    database.commit()
    database.close()
    print("done executing the script!")
    print("""
    Admin details:
    username: defaultadmin
    password: pleasechange123
    """)


def other_subjects(subjects):
    database = sqlite3.connect("data.sqlite")
    cursor = database.cursor()
    subjects_not_use = []

    subjects_ = cursor.execute(f"SELECT * FROM subjects").fetchall()
    for i in subjects_:
        if i[0] not in subjects:
            subjects_not_use.append(i[0])

    return subjects_not_use



