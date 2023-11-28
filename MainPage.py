import MainSystemMenus as SystemMenus
from data_manager import *

SystemMenus.login_menu()

try:
    userName = input("Enter Your Username:\n")
    password = input("Enter Your Password:\n")
except KeyboardInterrupt:
    print("goodbye")
    exit()

user_data = login(userName, password)


def print_all_students():
    student_list = view_all_students()
    for number, student in enumerate(student_list):
        print(f"{number + 1} - {student}")
    return student_list


while user_data:
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
                c = int(input('Enter input: '))
                if c == 1:
                    vclass = view_classes(userName)
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
            case 5:
                user_data = None
    elif user_data == 'receptionist':
        SystemMenus.receptionist_main_menu()
        choice = input("please select an option: ")
        if choice == "1":
            student_name = input("please enter the new student_index name: ")
            student_password = input("please enter the new student_index's password: ")
            student_IC = input("Please enter the new student_index's IC number: ")
            print("please enter 3 subjects for the student_index:")
            subjects = set([input(f'Subject {i}: ') for i in range(1, 4)])
            level = int(input("please enter the student_index's level: "))
            fees = level * 1000

            add_student(student_name, student_password, subjects, level, student_IC, fees)
            print(f"added new student_index: {student_name} successfully!")
        elif choice == '2':
            student_list = print_all_students()
            student_number = int(input("please enter the number of the student_index you want to delete: ")) - 1
            deletion_confirmation = input("Are you sure you want to delete this student_index: (N/Y): ")
            if deletion_confirmation == "Y":
                remove_user(student_list[student_number])
                print("deleted successfully")
            else:
                print("Cancelled!")
        elif choice == '3':
            all_requests = view_subject_change_requests()
            for index, name, request in enumerate(all_requests):
                print(f'{index}- {name} ==> {request}')

            student_index = int(input("please enter the number of the request you want to handle (-1 to exit): "))
            if student_index == -1 or student_index >= len(all_requests):
                continue

            student_request = all_requests[student_index]
            name = student_request[0]
            old_subject, new_subject = student_request[1].split(">")
            print(f'{name} would like to change from {old_subject} to {new_subject}')
            accept_deny = input("do you aproove of this change? [n, y]: ")
            if 'y' in accept_deny:
                handle_pending_request(name, True)
                print("accepted successfully!")
            else:
                handle_pending_request(name, False)
                print("request denied")
        elif choice == '4':
            students_fees = view_fees()
            for i, name, fees, pending in enumerate(students_fees):
                print(f"{i}- {name} ${fees} (pending payment: {pending})")

            student_index = int(input("enter the number of the student_index you want to accept thier payment (-1 to exit): "))
            if student_index == -1:
                continue
            elif student_index >= len(students_fees):
                print("Doesn't exist")
                continue
            else:
                student_name = students_fees[student_index]
                accept_payment(student_name)
        elif choice == '5':
            print("1) update username")
            print("2) update password")
            x = input("select item: ")
            if x == "1":
                change_profile(userName, new_username=input("please enter the new username: "))
            elif x == '2':
                change_profile(userName, new_password=input("please enter the new password: "))
        elif choice == '6':
            print_all_students()
        elif choice == '0':
            user_data = None
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
                username = input("Enter new tutor username:\n")
                password = input("Enter new tutor password:\n")
                subject = input("Enter new tutor's subject:\n")
                level = int(input("Enter your level:\n"))
                salary = int(input("Enter Your Salary:\n"))
                add_tutor(username, password, subject, level, salary)
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
                username = input("Enter Your User Name:\n")
                password = input("Enter Your Password:\n")
                add_receptionist(username, password)
            elif option == "2":
                username = input("Enter The Receptionist you Want To Delete:\n")
                print(remove_user(username))
        elif option == "4":
            print("Please Select Option:\n")
            SystemMenus.sub_update_profile()
            option = int(input("Enter input : "))
            if option == 1:
                new_username = input('Enter new username: ')
                change_profile(userName, new_username=new_username)
            elif option == 2:
                new_password = input('Enter new password: ')
                change_profile(userName, new_password=new_password)
