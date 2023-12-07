import sqlite3

from data_manager import connect_to_db


def get_subject(username):
    database = sqlite3.connect("data.sqlite")
    cursor = database.cursor()
    stu_classes = cursor.execute(f'SELECT subjects FROM students WHERE name="{username}";').fetchone()[0]
    return stu_classes


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


def handle_subject_request(student, is_accept):
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


def other_subjects(subjects):
    database = sqlite3.connect("data.sqlite")
    cursor = database.cursor()
    subjects_not_use = []

    subjects_ = cursor.execute(f"SELECT * FROM subjects").fetchall()
    for i in subjects_:
        if i[0] not in subjects:
            subjects_not_use.append(i[0])

    return subjects_not_use
