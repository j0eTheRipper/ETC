# ETC

## Initial setup guid
1. Clone this repository
2. go to the directory in which you cloned the repository and run `main.py`

When you first run the main.py file, you will notice a new `data.sqlite` file in your folder.
This file contains all the data concerning your school, so **DON'T delete it unless you're willing to reset all the data.**

## developers guid.
### to get started: 
1. fork this repository
2. clone YOUR forked repository
3. start writing your code!

### To add your changes:
1. commit and push
2. go to github.com and add a pull request..

## data_management module.
1. `login(username, password)` takes the username and the password and returns the user's role. if the user's credentials are wrong, the function returns `False`
2. `add_student(name, password, subjects, icad, fees)` adds a new student to the database.
3. `add_tutor(name, password, subjects)` adds a new tutor.
4. add_receptionist
