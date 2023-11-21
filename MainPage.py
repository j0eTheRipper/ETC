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
                time = input('Enter class date and time (use dd/mm/yy hh:mm): ')
                tutor_name = userName
                add_class(tutor_name, time)
                print('Class added successfully.')
            case 2:
                SystemMenus.sub_update_class()
                c= int(input('Enter input: '))
                if c == 1:
                   vclass= view_classes(userName)
                   print('Your classes: ')
                   print(*vclass, sep='\n')
                if c == 2:
                    print('Class updated.')
                if c == 3:
                    print('Class deleted.')
                else:
                    print('Input 1, 2, 3 only.')
            case 3:
                tutor = userName
                print('Students under your subject: ')
                allstudent = view_all_students(tutor)
                print(*allstudent, sep='\n')
            case 4:
                SystemMenus.sub_update_profile()
                opt = int(input('Enter input: '))
                if opt == 1:
                    new_username = input('Enter new username: ')
                    change_profile(userName, new_username=new_username)
                elif opt == 2:
                    new_password = input('Enter new password: ')
                    change_profile(userName, new_password=new_password)
                else:
                    print('Wrong input. Choose either 1 or 2')
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
                username = input("Enter The Tutor You Want To delete: ")
                print(remove_user(username))
            elif suboption == "3":
                tutor_list = view_all_tutors()
                for tutor in tutor_list:
                    print("name: " + tutor[0], "subject:" + tutor[1], "Level:" + str(tutor[2]), "Salary:" + str(tutor[3]))
        elif option == '2':
            SystemMenus.receptionist_management_menu()
            print("Select Your Option:\n")
            option = input()
            if option == "1":
                username = input("Enter Your User Name:\n")
                password = input("Enter Your Password:\n")
                add_receptionist(username, password)
            elif option == "2":
                username = input("Enter The Receptionist you Want To Delete:\n")
                print(remove_user(username))
        elif option == "4":
            print("Please Scelect Option:\n")
            SystemMenus.sub_update_profile()
            option = int(input("Enter input : "))
            if option == 1:
                new_username = input('Enter new username: ')
                change_profile(userName, new_username=new_username)
            elif option == 2:
                new_password = input('Enter new password: ')
                change_profile(userName, new_password=new_password)
