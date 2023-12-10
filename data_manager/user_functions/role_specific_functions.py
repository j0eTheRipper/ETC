from data_manager import connect_to_db
from data_manager.user_functions.user_management import validate_subjects, __generate_new_user_query


def add_student(username: str, email: str, password: str, subjects: set, level: int, ic: str, fees: int = 0):
    """adds a new student. used by receptionist"""
    cursor, database = connect_to_db()
    new_user = __generate_new_user_query(username, email, password, "student")
    new_student = f'INSERT INTO students (name, ID, subjects, level, fees) \
    VALUES ("{new_user[1]}", "{ic}", "{"-".join(list(subjects))}", {level}, {fees});'
    cursor.execute(new_user[0])
    cursor.execute(new_student)
    database.commit()
    database.close()


def add_tutor(username, email, password, assigned_subject, level, salary):
    """Adds a new tutor. Used by receptionist"""
    cursor, database = connect_to_db()

    # Checks if the subjects entered by the user are valid
    if not validate_subjects(cursor, {assigned_subject}):
        return

    # Handel errors if user entered invalid email
    try:
        query = __generate_new_user_query(username, email, password, "tutor")
    except ValueError:
        print("Please enter a valid email format example@mail.domain")
        return

    # inserts tutor into the users table and the tutors table
    new_user, username = query
    new_tutor = f'INSERT INTO tutors (name, subject, level, salary) VALUES ("{username}", "{assigned_subject}", {level}, {salary});'
    cursor.execute(new_user)
    cursor.execute(new_tutor)
    database.commit()
    database.close()


def add_receptionist(username, email, password: str):
    """Adds new receptionist to the database. Used by admin"""
    try:
        query = __generate_new_user_query(username, email, password, "receptionist")
    except ValueError:
        print("Please enter a valid email format example@mail.domain")
        return

    new_user, _ = query
    cursor, database = connect_to_db()
    cursor.execute(new_user)
    database.commit()
    database.close()


def view_all_tutors():
    cursor, database = connect_to_db()

    tutors = cursor.execute("SELECT * FROM tutors;").fetchall()
    return tutors


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
