from data_manager import connect_to_db


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
