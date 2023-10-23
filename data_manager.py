import sqlite3
import os

ROLES = {"admin", "receptionist", "tutor", "student"}


def __generate_new_user_query(username: str, password: str, role: str):
    role = role.lower()
    if role not in ROLES:
        print("role invalid!")
        return

    username = ''.join(username.lower().split())
    return f'INSERT INTO users (username, password, role) VALUES ("{username}", "{password}", "{role}");', username


def add_student(username: str, password: str, subjects: set, icad: str, fees: int = 0):
    if len(subjects) > 3:
        print("Up to 3 subjects allowed!")
        return

    database = sqlite3.connect("data.sqlite")
    cursor = database.cursor()
    if not validate_subjects(cursor, subjects):
        return

    new_user = __generate_new_user_query(username, password, "student")
    new_student = f'INSERT INTO students (name, ID, subjects, fees) \
    VALUES ("{new_user[1]}", "{icad}", "{"-".join(list(subjects))}", {fees});'
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


def add_tutor(username, password, assigned_subject: str):
    database = sqlite3.connect('data.sqlite')
    cursor = database.cursor()

    if not validate_subjects(cursor, {assigned_subject}):
        return

    new_user, username = __generate_new_user_query(username, password, "tutor")
    new_tutor = f'INSERT INTO tutors (name, subject) VALUES ("{username}", "{assigned_subject}");'
    cursor.execute(new_user)
    cursor.execute(new_tutor)
    database.commit()
    database.close()


def add_receptionist(username, password, role):
    new_user, _ = __generate_new_user_query(username, password, role)
    database = sqlite3.connect("data.sqlite")
    cursor = database.cursor()
    cursor.execute(new_user)
    database.commit()
    database.close()


def remove_user(username: str = '', icad: str = ''):
    pass


def init_db():
    """Deletes the current database and creates a new one, and makes a default admin"""
    if os.path.exists("data.sqlite"):
        os.remove("data.sqlite")

    database = sqlite3.connect("data.sqlite")
    cursor = database.cursor()
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
