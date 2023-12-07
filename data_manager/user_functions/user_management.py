import os
import re

from data_manager import connect_to_db

ROLES = {"admin", "receptionist", "tutor", "student"}


def __generate_new_user_query(username: str, email: str, password: str, role: str):
    role = role.lower()
    if role not in ROLES:
        print("role invalid!")
        return

    username = ''.join(username.lower().split())
    try:
        email = re.match(r"^[A-Za-z0-9]+@[a-z]+\.[a-z]+", email).group()
    except AttributeError:
        raise ValueError

    return f'INSERT INTO users (username, email, password, role) VALUES ("{username}", "{email}", "{password}", "{role}");', username


def login(password, email=None, username=None):
    """Returns the user's role if the password was correct. otherwise returns None"""
    cursor, database = connect_to_db()
    user_info = None

    if username:
        username = username.replace(" ", '')
        user_info = cursor.execute(f'SELECT username, password, role FROM users WHERE username="{username}"').fetchone()
    elif email:
        email = email.replace(" ", '')
        user_info = cursor.execute(f'SELECT username, password, role FROM users WHERE email="{email}"').fetchone()

    if user_info:
        if password == user_info[1]:
            return user_info[2], user_info[0]


def change_profile(username, new_username='', new_password='', new_email=''):
    cursor, database = connect_to_db()
    user_role = cursor.execute(f'SELECT role FROM users WHERE username="{username}";').fetchone()[0]

    if new_username:  # user specified new username
        if user_role == 'student':
            # updates the username in the students table
            cursor.execute(f'UPDATE students SET name="{new_username}" WHERE name="{username}";')
        elif user_role == 'tutor':
            # updates the tutors in the students table
            cursor.execute(f'UPDATE tutors SET name="{new_username}" WHERE name="{username}";')

        cursor.execute(f'UPDATE users SET username="{new_username}" WHERE username="{username}"')

    if new_password:  # user specified password
        cursor.execute(f'UPDATE users SET password="{new_password}" WHERE username="{username}"')

    if new_email:  # user specified email
        try:
            email = re.match(r"^[a-z]+@[a-z]+\.[a-z]+", new_email).group()
        except AttributeError:
            return 'please enter a valid email'

        cursor.execute(f'UPDATE users SET email="{email}" WHERE username="{username}"')

    database.commit()
    database.close()


def remove_user(username: str = ''):
    """deletes user from the database."""
    cursor, database = connect_to_db()

    role = cursor.execute(f'SELECT role FROM users WHERE username="{username}";').fetchone()
    if role:
        role = role[0]

        if role == "tutor":
            # deletes all classes assigned by the tutor
            cursor.execute(f'DELETE FROM classes WHERE tutor="{username}";')
            # deletes tutor from tutors table
            cursor.execute(f'DELETE FROM tutors WHERE name="{username}";')
        elif role == "student":
            cursor.execute(f'DELETE FROM students WHERE name="{username}";')

        cursor.execute(f'DELETE FROM users WHERE username="{username}";')

        database.commit()
        database.close()
        return "Deleted Successfully!"
    else:
        database.close()
        return "Doesn't exist!"


def validate_subjects(cursor, subjects):
    valid_subjects = set(map(lambda a: a[0], cursor.execute("SELECT * FROM subjects;").fetchall()))
    if (subjects & valid_subjects) != subjects:
        print("some of the subjects selected are invalid")
        return
    return True


def initialize_admin():
    """Deletes the current database and creates a new one, and makes a default admin account"""
    if os.path.exists("data.sqlite"):
        os.remove("data.sqlite")

    cursor, database = connect_to_db()
    with open('data_manager\\schema.sql', 'r') as schema:
        script = schema.read()
    cursor.executescript(script)

    default_subjects = {"english", "computer", "bahasa", "math", "physics", "chemistry", "biology"}
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
