from data_manager.common_f import connect_to_db
from data_manager.user_functions.user_management import validate_subjects, __generate_new_user_query


def add_student(username: str, email: str, password: str, subjects: set, level: int, ic: str, fees: int = 0):
    """adds a new student. used by receptionist"""
    if len(subjects) > 3:
        print("Up to 3 subjects allowed!")
        return

    cursor, database = connect_to_db()
    if not validate_subjects(cursor, subjects):
        return

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

    if not validate_subjects(cursor, {assigned_subject}):
        return

    try:
        query = __generate_new_user_query(username, email, password, "tutor")
    except ValueError:
        print("Please enter a valid email format example@mail.domain")
        return

    new_user, username = query
    new_tutor = f'INSERT INTO tutors (name, subject, level, salary) VALUES ("{username}", "{assigned_subject}", {level}, {salary});'
    cursor.execute(new_user)
    cursor.execute(new_tutor)
    database.commit()
    database.close()


def add_receptionist(username, email, password: str):
    """Adds new receptionist to the database. Used by admin"""
    new_user, _ = __generate_new_user_query(username, email, password, "receptionist")
    cursor, database = connect_to_db()
    cursor.execute(new_user)
    database.commit()
    database.close()
