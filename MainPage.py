import MainSystemMenus as SystemMenus
from common_functions import print_all_students, update_profile_interface
from data_manager.class_functions import *
from data_manager.fees_functions import view_fees, pay_fees, view_income
from data_manager.subject_functions import get_subject, request_subject_change, view_subject_change_requests, \
    handle_subject_request, other_subjects
from data_manager.user_functions.user_management import login, remove_user, initialize_admin
from data_manager.user_functions.role_specific_functions import add_tutor, add_receptionist, view_all_tutors, \
    view_all_students
from receptionist_functions import register_student, delete_student, manage_student_subject_requests, \
    manage_student_payments
from os import system
from os.path import exists

SystemMenus.login_menu()

if not exists("data.sqlite"):
    initialize_admin()

x = 0
user_data = None
while x < 3 and not user_data:
    if x > 0:
        print("please check your username and password")
    try:
        prompt = input("Enter Your Username or email:\n")
        password = input("Enter Your Password:\n")
    except KeyboardInterrupt:
        print("goodbye")
        exit()

    if "@" in prompt:
        user_data = login(password, email=prompt)
    else:
        user_data = login(password, username=prompt)

    if user_data:
        user_data, userName = user_data
    x += 1


while user_data:
    system("cls")
    if user_data == 'tutor':
        SystemMenus.class_menu()
        choice = int(input('Please select an option: '))
        match choice:
            case 1:
                time = input('Enter class date and time (use dd/mm/yy hh:mm): ')
                add_class(userName, time)
                print('Class added successfully.')
            case 2:
                SystemMenus.sub_update_class()
                c = int(input('Enter input: '))
                if c == 1:
                    vclass = view_classes(userName)
                    print('Your classes: ')
                    print(*vclass, sep='\n')
                elif c == 2:
                    vclass = view_classes(userName)
                    print('Your classes: ')
                    print(*vclass, sep='\n')
                    print("------------------------------\n")
                    class_id = int(input("Enter Class ID: "))
                    new_date = input("Enter new class date and time (use dd/mm/yy hh:mm): ")
                    update_class(class_id, new_date)
                    print('Class updated.')
                elif c == 3:
                    vclass = view_classes(userName)
                    print('Your classes: ')
                    print(*vclass, sep='\n')
                    print("------------------------------\n")
                    class_id = int(input("Enter Class ID to be deleted: "))
                    new_date = None
                    update_class(class_id, new_date)
                    print('Class deleted.')
                else:
                    print('Input 1, 2, 3 only.')
            case 3:
                tutor = userName
                print('Students under your subject: ')
                allstudent = view_all_students(tutor)
                print(*allstudent, sep='\n')
            case 4:
                update_profile_interface(userName)
            case 5:
                exit()
    elif user_data == 'receptionist':
        SystemMenus.receptionist_main_menu()
        choice = input("please select an option: ")
        if choice == "1":
            register_student()
        elif choice == '2':
            delete_student()
        elif choice == '3':
            manage_student_subject_requests(userName)
        elif choice == '4':
            manage_student_payments()
        elif choice == '5':
            update_profile_interface(userName)
        elif choice == '6':
            print_all_students()
        elif choice == '0':
            exit()
    elif user_data == "student":
        SystemMenus.student_menu()
        stu_choice = input("Please select an option: \n")
        if stu_choice == "1":
            print("Your classes are: " "\n")
            classes_list = view_classes(userName)
            for classes in classes_list:
                for class_ in classes:
                    print("Class: ", class_[0], "\nTutor: ", class_[1], "\nDate&Time: ", class_[2])
                    print()
            BackTo_menu = input("\nPlease Enter (menu) to back: \n").lower()
            print()
            if BackTo_menu == "menu":
                continue
            else:
                print("Wrong choice")

        elif stu_choice == "2":
            print()
            x = 1
            old_subjects = get_subject(userName).split("-")
            for subjects_change in old_subjects:
                print(f"{x}) {subjects_change}")
                x += 1
            stu_change = int(input("Please chose the subjects you want to change: "))
            print()
            o_subjects = other_subjects(get_subject(userName))

            y = 1
            for o in o_subjects:
                print(f"{y}) {o}")
                y += 1

            stu_add = int(input("Please chose the subjects you want to add: "))

            x = request_subject_change(userName, old_subjects[stu_change - 1], o_subjects[stu_add - 1])
            if x:
                print(x)

        elif stu_choice == "3":
            stu_request = view_subject_change_requests(userName)[0][1]
            if stu_request is not None:
                stu_delete_ = input(
                    f"Your request change is {stu_request}\n\nPress Y if you want to delete the request: ").upper()
                if stu_delete_ == "Y":
                    handle_subject_request(userName, False)
                    print("\nRequest has been deleted")
            else:
                print("\nYou have no pending requests.")
        elif stu_choice == "4":
            fees, status = view_fees(userName)
            if status is None:
                print(f"\nYou need to pay {fees}\n")
                payment = input("Press Y if you want to pay fees: ").upper()
                if payment == "Y":
                    pay_fees(userName)
            elif status == "pending":
                print(f"**** Your payment is pending ****\n")
            else:
                print("You don't need to pay")
        elif stu_choice == "5":
            update_profile_interface(userName)
            print("\n******  The profile has updated  ****** \n")
        elif stu_choice == "0":
            exit()
    elif user_data == 'admin':
        SystemMenus.admin_menu()
        print("Please Select Option:\n")
        option = input()
        if option == '1':
            SystemMenus.tutor_management_menu()
            print("Please Select Option:\n")
            suboption = input()
            if suboption == "1":
                username = input("Enter new tutor username:\n")
                email = input("Enter the new tutor's email: \n")
                password = input("Enter new tutor password:\n")
                subject = input("Enter new tutor's subject:\n")
                level = int(input("Enter new tutor's level:\n"))
                salary = level * 2000
                add_tutor(username, email, password, subject, level, salary)
            elif suboption == "2":
                username = input("Enter The Tutor You Want To delete: ")
                print(remove_user(username))
            elif suboption == "3":
                tutor_list = view_all_tutors()
                for tutor in tutor_list:
                    print("name: " + tutor[0], "subject:" + tutor[1], "Level:" + str(tutor[2]),
                          "Salary:" + str(tutor[3]))
        elif option == '2':
            SystemMenus.receptionist_management_menu()
            print("Select Your Option:\n")
            option = input()
            if option == "1":
                username = input("Enter the receptionist's User Name:\n")
                email = input("enter the receptionist's email , example@mail.domain: ")
                password = input("Enter the receptionist's password Password:\n")
                add_receptionist(username, email, password)
            elif option == "2":
                username = input("Enter The Receptionist you Want To Delete:\n")
                print(remove_user(username))
        elif option == "3":
            print("Please Select Option:\n")
            update_profile_interface(userName)
        elif option == "4":
            print("1) View students fees\n2) View tutor salaries\n3) View all")
            option = input("Please select an option: ")
            student_fees, salaries = view_income()
            if option == '1':
                print(f"total student fees payed: {student_fees} RM")
            elif option == '2':
                print(f"total salaries payed: {salaries} RM")
            elif option == '3':
                print(f'total income: {student_fees - salaries}')
        elif option == '5':
            print("Goodbye")
            exit()

    input("Enter to continue...")
