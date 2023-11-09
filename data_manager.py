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


def add_student(username: str, password: str, subjects: set, level: int, icad: str, fees: int = 0):
    """adds a new student. used by receptionist"""
    if len(subjects) > 3:
        print("Up to 3 subjects allowed!")
        return

    database = sqlite3.connect("data.sqlite")
    cursor = database.cursor()
    if not validate_subjects(cursor, subjects):
        return

    new_user = __generate_new_user_query(username, password, "student")
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


def add_tutor(username, password, assigned_subject: str, level, salary):
    """Adds a new tutor. Used by receptionist"""
    database = sqlite3.connect('data.sqlite')
    cursor = database.cursor()

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
    database = sqlite3.connect("data.sqlite")
    cursor = database.cursor()
    cursor.execute(new_user)
    database.commit()
    database.close()


def remove_user(username: str = ''):
    """deletes user from the database."""
    database = sqlite3.connect("data.sqlite")
    cursor = database.cursor()

    role = cursor.execute(f'SELECT role FROM users WHERE username="{username};"').fetchone()
    if role:
        role = role[0]
        if role == "tutor":
            cursor.execute(f'DELETE FROM classes WHERE tutor="{username};')
            cursor.execute(f'DELETE FROM tutors WHERE name="{username};')
        elif role == "student":
            cursor.execute(f'DELETE FROM students WHERE name="{username}";')
        cursor.execute(f'DELETE FROM users WHERE username={username};')
    else:
        return False


def view_all(role=''):
    database = sqlite3.connect('data.sqlite')
    cursor = database.cursor()
    base_query = "SELECT username FROM users "
    if role:
        users = cursor.execute(base_query + f'WHERE role="{role}";').fetchall()
    else:
        users = cursor.execute(base_query + ';').fetchall()

    database.close()
    return users


def view_all_students(tutor=''):
    database = sqlite3.connect('data.sqlite')
    cursor = database.cursor()
    tutor_info = cursor.execute(f'SELECT subject, level FROM tutors WHERE name="{tutor}";').fetchone()
    subject = tutor_info[0]
    level = tutor_info[1]

    if tutor:
        student_list = cursor.execute(f'SELECT name FROM students WHERE subjects LIKE "%{subject}%" and level={level};').fetchall()
    else:
        student_list = cursor.execute(f'SELECT name FROM students;').fetchall()

    return [i[0] for i in student_list]


def change_profile(username, new_username='', new_password=''):
    database = sqlite3.connect('data.sqlite')
    cursor = database.cursor()
    if new_username:
        cursor.execute(f'UPDATE users SET username="{new_username}" WHERE username="{username}"')
    if new_password:
        cursor.execute(f'UPDATE users SET password="{new_password}" WHERE username="{username}"')

    database.commit()
    database.close()


def init_db():
    """Deletes the current database and creates a new one, and makes a default admin account"""
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


def login(username, password):
    """Returns the user's role if the password was correct. otherwise returns 'wrong password'"""
    db = sqlite3.connect('data.sqlite')
    cursor = db.cursor()
    username = ''.join(username.lower())
    user_info = cursor.execute(f'SELECT * FROM users WHERE username="{username}"').fetchone()
    if user_info:
        if password == user_info[1]:
            return user_info[2]
        return 'wrong password'
    return 'wrong username'
