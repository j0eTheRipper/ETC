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
                tutor = userName
                print('Students under your subject: ')
                view_all_students(tutor)
            case 4:
                SystemMenus.sub_update_profile()
                opt = int(input('Enter input: '))
                if opt == 1:
                    new_username = input('Enter new username: ')
                elif opt == 2:
                    new_password = input('Enter new password: ')
                else:
                    print('Wrong input. Choose either 1 or 2')
                change_profile(userName, new_username, new_password)
            case 5:
                print('Exitted succesfully.')

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
            elif suboption == "2":
                username = input("Enter The Tutor You Want To delet: ")
                remove_user(username)
                print("The tutor Has Been Successfully Deleted:")
        elif option == '2':
            SystemMenus.receptionist_management_menu()
            print("Select Your Option:\n")
            option = input()
            if option == "1":
                username = input("Enter Your User Name:\n")
                password = input("Enter Your Password:\n")
                add_receptionist(username, password)
            elif option == "2":
                username = input("Enter The Receptionist you Want To Delet:\n")
                remove_user(username)
                print("The Receptionist Has Been Seccessfully Deleted")
