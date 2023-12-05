import MainSystemMenus as SystemMenus
from common_functions import print_all_students, update_profile_interface
from data_manager import *

SystemMenus.login_menu()

try:
    userName = input("Enter Your Username:\n")
    password = input("Enter Your Password:\n")
except KeyboardInterrupt:
    print("goodbye")
    exit()

user_data = login(userName, password)

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
                user_data = None
    elif user_data == 'receptionist':
        SystemMenus.receptionist_main_menu()
        choice = input("please select an option: ")
        if choice == "1":
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
        elif choice == '2':
            student_list = print_all_students()
            student_number = int(input("please enter the number of the student you want to delete: ")) - 1
            deletion_confirmation = input("Are you sure you want to delete this student: (N/Y): ")
            if deletion_confirmation == "Y":
                remove_user(student_list[student_number])
                print("deleted successfully")
            else:
                print("Cancelled!")
        elif choice == '3':
            all_requests = view_subject_change_requests(userName)
            for index, data in enumerate(all_requests):
                name, request = data
                print(f'{index}- {name} ==> {request}')

            student_index = int(input("please enter the number of the request you want to handle (-1 to exit): "))
            if student_index == -1 or student_index >= len(all_requests):
                continue

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
        elif choice == '4':
            students_fees = view_fees()
            for i, data in enumerate(students_fees):
                name, fees, pending = data
                print(f"{i}- {name} ${fees} (payment status: {pending})")

            student_index = int(input("enter the number of the student you want to accept thier payment (-1 to exit): "))
            if student_index == -1:
                continue
            elif student_index >= len(students_fees):
                print("Doesn't exist")
                continue
            else:
                student_name = students_fees[student_index][0]
                accept_payment(student_name)
        elif choice == '5':
            update_profile_interface(userName)
        elif choice == '6':
            print_all_students()
        elif choice == '0':
            exit()
#STUDENT LOOP
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
            if stu_request != None:
                stu_delete_ = input(f"Your request change is {stu_request}\n\nPress Y if you want to delete the request: ").upper()
                if stu_delete_ == "Y":
                    handle_pending_request(userName, False)
                    print("\nRequest has deleted")
            elif stu_request == None:
                print("\nYou didn't send any request!")
            elif stu_request > 1:
                print("\nWait for the pending!")
            else:
                print("\nSorry you cannot delete, The request has been accepted!")


        elif stu_choice == "4":
            fees, status = view_fees(userName)
            if status == None:
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
                # UserList = view_all()
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
                email = input("enter the receptionist's email: ")
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
        elif option == '5':
            print("Goodbye")
            exit()
else:
    print('Please check your username and password')