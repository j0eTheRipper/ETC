from common_functions import print_all_students
from data_manager.fees_functions import view_fees, accept_payment
from data_manager.subject_functions import view_subject_change_requests, handle_subject_request, other_subjects
from data_manager.user_functions.user_management import remove_user
from data_manager.user_functions.role_specific_functions import add_student
import re


def register_student():
    student_name = input("please enter the new student name: ")
    student_email = input("please enter the new student's email: ")
    student_email = re.match(r"^[A-Za-z0-9]+@[a-z]+\.[a-z]+", student_email)

    if not student_email:
        print("Please enter a valid email example@mail.com")
        return

    student_password = input("please enter the new student's password: ")
    student_ic = input("Please enter the new student's IC number: ")
    student_ic = re.fullmatch(r"^\d{6}-\d{2}-\d{4}$", student_ic)

    if not student_ic:
        print("Please enter a valid IC nnnnnn-nn-nnnn")
        return

    student_ic = student_ic.group()
    subjects_selected = set()
    for i in range(1, 4):
        available_subjects = list(set(other_subjects(subjects_selected)) - subjects_selected)
        for number, subject in enumerate(available_subjects):
            print(f'{number}) {subject}')
        subjects_selected.add(available_subjects[int(input("please select a subject: "))])
        print()
    level = int(input("please enter the student's level: "))
    fees = level * 1000
    add_student(student_name, student_email.group(), student_password, subjects_selected, level, student_ic, fees)
    print(f"added new student: {student_name} successfully!")


def delete_student():
    student_list = print_all_students()
    student_number = int(input("please enter the number of the student you want to delete: ")) - 1
    deletion_confirmation = input("Are you sure you want to delete this student: (N/Y): ")
    if deletion_confirmation == "Y":
        remove_user(student_list[student_number])
        print("deleted successfully")
    else:
        print("Cancelled!")


def manage_student_subject_requests(username):
    all_requests = view_subject_change_requests(username)
    for index, data in enumerate(all_requests):
        name, request = data
        if request:
            print(f'{index}- {name} ==> {request}')

    try:
        student_index = int(input("please enter the number of the request you want to handle (-1 to exit): "))
    except ValueError:
        return

    if student_index == -1 or student_index >= len(all_requests):
        return

    student_request = all_requests[student_index]
    name = student_request[0]
    old_subject, new_subject = student_request[1].split(">")
    print(f'{name} would like to change from {old_subject} to {new_subject}')
    accept_deny = input("do you aproove of this change? [n, y]: ")
    if 'y' in accept_deny:
        handle_subject_request(name, True)
        print("accepted successfully!")
    else:
        handle_subject_request(name, False)
        print("request denied")


def manage_student_payments():
    students_fees = view_fees()
    for i, data in enumerate(students_fees):
        name, fees, pending = data
        print(f"{i}- {name} ${fees} (payment status: {pending})")

    try:
        student_index = int(input("please enter the number of the request you want to handle (-1 to exit): "))
    except ValueError:
        return

    if student_index == -1 or student_index >= len(students_fees):
        return

    student_name = students_fees[student_index][0]
    accept_payment(student_name)
