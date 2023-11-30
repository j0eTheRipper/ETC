import MainSystemMenus as SystemMenus
from data_manager import view_all_students, change_profile


def print_all_students():
    student_list = view_all_students()
    for number, student in enumerate(student_list):
        print(f"{number + 1} - {student}")
    return student_list


def update_profile_interface(username):
    SystemMenus.sub_update_profile()
    option = int(input("Enter input : "))
    if option == 1:
        new_username = input('Enter new username: ')
        change_profile(username, new_username=new_username)
    elif option == 2:
        new_email = input('Enter new email: ')
        change_profile(username, new_email=new_email)
    elif option == 3:
        new_password = input('Enter new password: ')
        change_profile(username, new_password=new_password)
