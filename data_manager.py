import sqlite3
import os

ROLES = {"admin", "receptionist", "tutor", "student_index"}


def __generate_new_user_query(username: str, password: str, role: str):
    role = role.lower()
    if role not in ROLES:
        print("role invalid!")
        return

    username = ''.join(username.lower().split())
    return f'INSERT INTO users (username, password, role) VALUES ("{username}", "{password}", "{role}");', username


def add_student(username: str, password: str, subjects: set, level: int, icad: str, fees: int = 0):
    """adds a new student_index. used by receptionist"""
    if len(subjects) > 3:
        print("Up to 3 subjects allowed!")
        return

    cursor, database = connect_to_db()
    if not validate_subjects(cursor, subjects):
        return

    new_user = __generate_new_user_query(username, password, "student_index")
    new_student = f'INSERT INTO students (name, ID, subjects, level, fees) \
    VALUES ("{new_user[1]}", "{icad}", "{"-".join(list(subjects))}", {level}, {fees});'
    cursor.execute(new_user[0])
    cursor.execute(new_student)
    database.commit()
    database.close()


def validate_subjects(cursor, subjects):
    valid_subjects = set(map(lambda a: a[0], cursor.execute("SELECT * FROM subjects;").fetchall()))
    if (subjects & valid_subjects) != subjects:
        print("some of the subjects selected are invalid")
        return
    return True


def add_tutor(username, password, assigned_subject, level, salary):
    """Adds a new tutor. Used by receptionist"""
    cursor, database = connect_to_db()

    if not validate_subjects(cursor, {assigned_subject}):
        return

    new_user, username = __generate_new_user_query(username, password, "tutor")
    new_tutor = f'INSERT INTO tutors (name, subject, level, salary) VALUES ("{username}", "{assigned_subject}", {level}, {salary});'
    cursor.execute(new_user)
    cursor.execute(new_tutor)
    database.commit()
    database.close()


def add_receptionist(username, password: str):
    """Adds new receptionist to the database. Used by admin"""
    new_user, _ = __generate_new_user_query(username, password, "receptionist")
    cursor, database = connect_to_db()
    cursor.execute(new_user)
    database.commit()
    database.close()


def remove_user(username: str = ''):
    """deletes user from the database."""
    cursor, database = connect_to_db()

    role = cursor.execute(f'SELECT role FROM users WHERE username="{username}";').fetchone()
    if role:
        role = role[0]
        if role == "tutor":
            cursor.execute(f'DELETE FROM classes WHERE tutor="{username}";')
            cursor.execute(f'DELETE FROM tutors WHERE name="{username}";')
        elif role == "student_index":
            cursor.execute(f'DELETE FROM students WHERE name="{username}";')
        cursor.execute(f'DELETE FROM users WHERE username="{username}";')
        database.commit()
        database.close()
        return "Deleted Successfully!"
    else:
        database.close()
        return "Doesn't exist!"


def view_all_tutors():
    cursor, database = connect_to_db()

    tutors = cursor.execute("SELECT * FROM tutors;").fetchall()
    return tutors


def view_all_students(tutor=''):
    cursor, database = connect_to_db()
    student_list = []

    if tutor:
        tutor_info = cursor.execute(f'SELECT subjects, level FROM tutors WHERE name="{tutor}";').fetchone()
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
    student_has_pending_request = student[5]
    if student_has_pending_request:
        return "student_index has pending requests"

    if subject in student_subjects and new_subject not in student_subjects:
        cursor.execute(f'UPDATE students SET pending_request="{subject}>{new_subject}" WHERE name="{name}";')
        database.commit()

    database.close()


def view_subject_change_requests():
    cursor, database = connect_to_db()
    pending_requests = cursor.execute('SELECT name, pending_request FROM students;').fetchall()
    return pending_requests


def handle_pending_request(student, is_accept):
    cursor, database = connect_to_db()
    current_subjects, pending_request, accepted_requests, denied_requests = cursor.execute(f'SELECT subjects, pending_request, accepted_requests, denied_requests FROM students WHERE name="{student}";').fetchone()
    if is_accept:
        old_subject, new_subject = pending_request.split(">")
        current_subjects = current_subjects.split("-")
        current_subjects.remove(old_subject)
        current_subjects.append(new_subject)
        current_subjects = '-'.join(current_subjects)
        print(pending_request)
        if not accepted_requests:
            accepted_requests = pending_request
        else:
            accepted_requests += "-" + pending_request
        cursor.execute(f'UPDATE students SET subjects="{current_subjects}", pending_request=NULL, accepted_requests="{accepted_requests}" WHERE name="{student}";')
    else:
        denied_requests += "-" + pending_request
        cursor.execute(f'UPDATE students SET pending_request=NULL, denied_requests="{denied_requests}" WHERE name="{student}";')

    database.commit()
    database.close()


def view_fees(username=""):
    cursor, database = connect_to_db()
    if username:
        student_fees = cursor.execute(f'SELECT fees FROM students WHERE name="{username}";').fetchone()[0]
    else:
        student_fees = cursor.execute(f'SELECT student_index, fees, payment FROM students;').fetchall()

    return student_fees


def pay_fees(username, ammount):
    cursor, database = connect_to_db()
    cursor.execute(f'UPDATE students SET payment={ammount} where name="{username}";')
    database.commit()
    database.close()


def accept_payment(username):
    cursor, database = connect_to_db()
    fees, payment = cursor.execute(f'SELECT fees, payment FROM student_index WHERE name="{username}";')
    if payment <= fees:
        return
    else:
        fees -= payment
        cursor.execute(f'UPDATE students SET payment=NULL, fees={fees} WHERE name="{username}";')
        database.commit()
    database.close()


def add_class(tutor_name, time):
    cursor, database = connect_to_db()

    tutor, level, subject = (cursor.execute(f'SELECT name, level, subject FROM tutors WHERE name="{tutor_name}";').
                             fetchone())

    cursor.execute(f'INSERT INTO classes (subject, level, tutor, time) VALUES ("{subject}", {level}, "{tutor}", "{time}");')
    database.commit()
    database.close()


def connect_to_db():
    database = sqlite3.connect("data.sqlite")
    cursor = database.cursor()
    return cursor, database


def view_classes(username):
    cursor, database = connect_to_db()

    user_role = cursor.execute(f'SELECT role FROM users WHERE username="{username}";').fetchone()[0]
    classes = []
    if user_role == 'student_index':
        student_info = cursor.execute(f'SELECT * FROM students WHERE name="{username}";').fetchone()
        subjects = student_info[1].split("-")
        for i in subjects:
            classes.append(cursor.execute(f'SELECT * from classes WHERE level={student_info[2]} AND subject="{i}";').fetchall())
    elif user_role == 'tutor':
        return cursor.execute(f'SELECT * FROM classes WHERE tutor="{username}";').fetchall()
    return classes


def change_profile(username, new_username='', new_password=''):
    cursor, database = connect_to_db()
    user_role = cursor.execute(f'SELECT role FROM users WHERE username="{username}";').fetchone()[0]
    if new_username:
        if user_role == 'student_index':
            cursor.execute(f'UPDATE students SET name="{new_username}" WHERE name="{username}";')
        elif user_role == 'tutor':
            cursor.execute(f'UPDATE tutors SET name="{new_username}" WHERE name="{username}";')
        cursor.execute(f'UPDATE users SET username="{new_username}" WHERE username="{username}"')
    if new_password:
        cursor.execute(f'UPDATE users SET password="{new_password}" WHERE username="{username}"')

    database.commit()
    database.close()


def init_db():
    """Deletes the current database and creates a new one, and makes a default admin account"""
    if os.path.exists("data.sqlite"):
        os.remove("data.sqlite")

    cursor, database = connect_to_db()
    with open('schema.sql', 'r') as schema:
        script = schema.read()
    cursor.executescript(script)

    default_subjects = {"english", "computer", "bahasa melayu", "math", "physics", "chemistry", "biology"}
    for subject in default_subjects:
        cursor.execute(f'INSERT INTO subjects VALUES ("{subject}");')

    new_user = __generate_new_user_query("defaultadmin", "pleasechange123", "admin")[0]
    cursor.execute(new_user)
    database.commit()
    database.close()
    print("done executing the script!")
    print("""
    Admin details:
    username: defaultadmin
    password: pleasechange123
    """)


def login(username, password):
    """Returns the user's role if the password was correct. otherwise returns 'wrong password'"""
    cursor, database = connect_to_db()
    username = ''.join(username.lower())
    user_info = cursor.execute(f'SELECT * FROM users WHERE username="{username}"').fetchone()
    if user_info:
        if password == user_info[1]:
            return user_info[2]
        return 'wrong password'
    return 'wrong username'
