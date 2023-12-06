from common_functions import print_all_students
from data_manager.data_manager import view_subject_change_requests, handle_pending_request, view_fees, \
    accept_payment
from data_manager.user_functions.user_management import remove_user
from data_manager.user_functions.add_by_role import add_student


def register_student():
    student_name = input("please enter the new student name: ")
    student_email = input("please enter the new student's email: ")
    student_password = input("please enter the new student's password: ")
    student_IC = input("Please enter the new student's IC number: ")
    print("please enter 3 subjects for the student:")
    subjects = set([input(f'Subject {i}: ') for i in range(1, 4)])
    level = int(input("please enter the student's level: "))
    fees = level * 1000
    add_student(student_name, student_email, student_password, subjects, level, student_IC, fees)
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
        print(f'{index}- {name} ==> {request}')

    student_index = int(input("please enter the number of the request you want to handle (-1 to exit): "))
    if student_index == -1 or student_index >= len(all_requests):
        return

    student_request = all_requests[student_index]
    name = student_request[0]
    old_subject, new_subject = student_request[1].old_subjects(">")
    print(f'{name} would like to change from {old_subject} to {new_subject}')
    accept_deny = input("do you aproove of this change? [n, y]: ")
    if 'y' in accept_deny:
        handle_pending_request(name, True)
        print("accepted successfully!")
    else:
        handle_pending_request(name, False)
        print("request denied")


def manage_student_payments():
    students_fees = view_fees()
    for i, data in enumerate(students_fees):
        name, fees, pending = data
        print(f"{i}- {name} ${fees} (payment status: {pending})")

    student_index = int(
        input("enter the number of the student you want to accept thier payment (-1 to exit): "))
    if student_index == -1:
        return
    elif student_index >= len(students_fees):
        print("Doesn't exist")
        return
    else:
        student_name = students_fees[student_index][0]
        accept_payment(student_name)
