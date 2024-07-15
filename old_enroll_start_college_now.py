
from time import sleep

from bb_lib.course import enroll_user
from bb_lib.user import BBUser, create_user, does_user_exist
#from bb_lib_old import enroll_user, does_user_exist, create_user, BBUser

users = []
COURSE_ID = "startcollegefall2408"



def _populate_students(_file_path: str) -> list:
    _users = []
    with open(_file_path, 'r') as file:
        i = 0
        _user = BBUser()
        for line in file.readlines():  # Iterate through each line of the text file
            line=line.strip()
            if i < 3 and line != "":
                if i == 0:
                    _user.user_ID = line
                   # print(f" user id = {line}")
                if i == 1:
                    _f_name = line.split(' ')
                    _user.first_name = _f_name[0]
                    _user.last_name = _f_name[1]
                # print(f" user f name = {_f_name[0]}")
                # print(f" user l name = {_f_name[1]}")
                if i == 2:
                    _user.email = line
                i+=1
            if i == 3:
                i = 0 
                _users.append(_user)
                _user = BBUser()
    return _users


if __name__ == "__main__":
    # Get users from txt file
    users = _populate_students()
    for u in users:
        if not does_user_exist(u.user_ID):
            create_user(username=u.user_ID, f_name=u.f_name, l_name=u.l_name, email=u.email)
            sleep(5)
        enroll_user(user_ID=u.user_ID, course_id=COURSE_ID, role="Student")

def enroll_start_college_now(txt_list_path: str) -> None:
    """Takes a .txt file with a list of students and enroll them into Start College Now course.\n
        Format:\n
            user_id\n
            full name (first last)\n
            email\n
            -SPACE-\n
            user_id\n
            full name (first last)\n
            email\n

    Args:
        txt_list_path (str): _description_
    """
    #users = []
    COURSE_ID: str = "startcollegefall2408"
    # Get users from txt file
    users: list = _populate_students(txt_list_path)
    for u in users:
        if not does_user_exist(u.user_ID):
            create_user(username=u.user_ID, f_name=u.f_name, l_name=u.l_name, email=u.email)
            sleep(5)
        enroll_user(user_ID=u.user_ID, course_id=COURSE_ID, role="Student")