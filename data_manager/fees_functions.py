from data_manager import connect_to_db


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


def view_income():
    cursor, database = connect_to_db()

    students_fees = [i[0] for i in cursor.execute('SELECT fees FROM students WHERE payment_status="success";').fetchall()]
    tutors_income = [i[0] for i in cursor.execute('SELECT salary FROM tutors;').fetchall()]

    return sum(students_fees), sum(tutors_income)
