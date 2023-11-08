import MainSystemMenus as SystemMenus
from data_manager import *


SystemMenus.loginMenu()

userName = input("Enter Your Username:\n")
password = input("Enter Your Password:\n")

user_data = login(userName, password)

if user_data:
    if user_data == 'tutor':
        SystemMenus.classmenu()
        choice= int(input('Please select an option: '))
        match choice:#submenu
            case 1:
                SystemMenus.subclassinfo()
            case 2:
                SystemMenus.subupdateclass()
            case 3:
                print('Students under your class:') #not finished
            case 4:
                username= input('Enter old username: ')
                new_username= input('Enter new username: ')
                new_password= input('Enter new password: ')
                change_profile(username, new_username, new_password) #not finished
    elif user_data == 'reciption':
        SystemMenus.ReceptionManagementMenu()
    elif user_data == 'admin':
        SystemMenus.AdminMenu()
        print("Please Select Option:\n")
        option = input()
        if option == '1':
            SystemMenus.TutorManagementMenu()
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
            SystemMenus.ReceptionManagementMenu()













