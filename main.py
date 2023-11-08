from data_manager import *
print("""
========================WELCOME TO ETC==============================================
""")
username = input("Please enter your username: ")
password = input("please enter your password: ")
role = login(username, password)
# (tutor, receptionist, admin, student) (wrong password)
if role == "wrong password":
    print("wrong password")
elif role == 'admin':
    """Ali Writes menu for admin"""
elif role == 'student':
    """Ammar writes menu for student"""
elif role == 'receptionist':
    """Youssef writes menu for receptionist"""
elif role == 'tutor':
    '''Adlina writes menu for tutor'''

