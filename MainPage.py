import MainSystemMenus as SystemMenus
from data_manager import *


SystemMenus.login_menu()

userName = input("Enter Your Username:\n")
password = input("Enter Your Password:\n")

user_data = login(userName, password)

if user_data:
    if user_data == 'tutor':
        SystemMenus.class_menu()
        choice = int(input('Please select an option: '))
        match choice:
            case 1:
                SystemMenus.sub_class_info()
            case 2:
                SystemMenus.sub_update_class()
            case 3:
                print('Students under your subject: ')
            case 4:
                username = input('Enter old username: ')
                new_username = input('Enter new username: ')
                new_password = input('Enter new password: ')
                change_profile(username, new_username, new_password)
    elif user_data == 'receptionist':
        SystemMenus.receptionist_main_menu()
    elif user_data == 'admin':
        SystemMenus.admin_menu()
        print("Please Select Option:\n")
        option = input()
        if option == '1':
            SystemMenus.tutor_management_menu()
            print("Please Select Option:\n")
            suboption = input()
            if suboption == "1":
                # UserList = view_all()
                username = input("Enter Your User name:\n")
                password = input("Enter Your Password:\n")
                subject = input("Enter Your Subject:\n")
                level = int(input("Enter your level:\n"))
                salary = int(input("Enter Your Salary:\n"))
                add_tutor(username, password, subject, level, salary)


        elif option == '2':
            SystemMenus.receptionist_management_menu()
