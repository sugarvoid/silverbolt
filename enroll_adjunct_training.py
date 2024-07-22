"""
    Description: This script adds adjuncts into their required training.
    Author: David Durham
    License: MIT

                                               README
    -----------------------------------------------------------------------------------------------------------
    Emails come in this format

    Name: Hank Hill
    ID: 123456789
    Dean/Associate Dean: Glen Pullman
    Mentor: Chris Cone
    Program: Human Relation
    Part 1: 8/15/2024
    Part 2:  1/15/2025

    Note: You may need to delete some text in the due dates, sometimes there are the word 'due date' in there.

    Paste that text in .txt file and run the script. It will:
        1 - Check to see if user has an account, if not will create it.
        2 - Enroll them into both Part 1 and Part 2 of the adjunct training
        3 - Add the required information in the gradebook

    If anything is was not successful, it will show up in the log file.

"""

#TODO: Move to fvtc.py inside the main lib

from csv import DictReader
import re
from csv import writer
from requests import patch, get, Response
from bb_lib.course import enroll_user
from bb_lib.grade import update_grade_entry
from time import sleep
from bb_lib.user import create_user, does_user_exist
from bb_lib.csv_templates import create_adjunct_training_csv
from bb_lib.logger import Logger


FILE_PATH = "data/adjunct_list.txt"
ADJUNCT_CSV = "data/adjunct_training.csv"
PART_1_COURSE_ID = "ADJPART12020"
PART_2_PARENT_ID = "AdjTrainingPART2D23"
PART_2_CURRENT_CHILD_ID = "AdjTrainingPART2-2024"

# TODO: Add part 3 and 4 ids
PART_3_ID = "AdjTrainingPART3"
PART_4_ID = "AdjTrainingPART4D24"

PART_1_GB_ID = {
    "dean": "_3203553_1",
    "mentor": "_3610506_1",
    "program": "_3506584_1",
    "due_date": "_3095852_1",
}

PART_2_GB_ID = {
    "dean": "_4460634_1",
    "mentor": "",
    "program": "_4460635_1",
    "due_date": "_4460232_1",
}

PART_3_GB_ID = {
    "dean" :"",
    "mentor": "",
    "program": "",
    "due_date": ""
}

PART_4_GB_ID = {
    "dean" :"",
    "mentor": "",
    "program": "",
    "due_date": ""
}


def is_date_format(date_str):
    # Define the regex pattern for the following date formats "x/x/xxxx", "xx/x/xxxx", "x/xx/xxxx", "xx/xx/xxxx"
    pattern = r"^\d{1,2}/\d{1,2}/\d{4}$"

    # Use re.match to check if the string matches the pattern
    if re.match(pattern, date_str):
        return True
    else:
        return False


class Adjunct:
    def __init__(self, first_name, last_name, id_number, supervisor, mentor, program, p1_due, p2_due, p3_due, p4_due:str):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = id_number
        self.supervisor = supervisor
        self.mentor = mentor
        self.program = program
        self.p1_due = parse_date(p1_due)
        self.p2_due = parse_date(p2_due)
        self.p3_due = parse_date(p3_due)
        self.p4_due = parse_date(p4_due)

        _dates = []

        for d in [self.p1_due, self.p2_due, self.p3_due, self.p4_due]:
            if d != "":  # Skip empty dates
                print(d)
                _dates.append(is_date_format(d))

        if all(_dates):
            # print("all dates good")
            _dates.clear()
        else:
            print("wrong format")


def parse_date(date_s: str) -> str:
    
    c_date = date_s.split(" ")
    if len(date_s) > 1:
        return date_s
    elif date_s == "Waived":
        return "Waived"
    else:
        return ""


def make_adjunct_obj(data) -> Adjunct:
    # Extract first name and last name from the 'Name' field
    f_name, l_name = data["Name"].split()
    # Create an Adjunct object and add it to the list
    return Adjunct(
        first_name=f_name,
        last_name=l_name,
        id_number=data["ID"],
        supervisor=data["Dean/Associate Dean"],
        mentor=data["Mentor"],
        program=data["Program"],
        p1_due=data.get("Part 1", ""),
        p2_due=data.get("Part 2", ""),
        p3_due=data.get("Part 3", ""),
        p4_due=data.get("Part 4", ""),
    )


# Function to parse the text file and extract user information
def parse_adjunct_txt(file_path: str) -> list:
    with open(file_path, "r") as file:
        lines = file.readlines()

    all_users: list = []
    current_user_dict: dict = {}

    # Process each line in the file
    for line in lines:
        # Strip leading/trailing whitespace from the line
        line = line.strip()

        if line:  # If line is not empty
            # Split each line into key and value based on the first occurrence of ':'
            key, value = line.split(":", 1)
            # Remove leading and trailing whitespace from key and value
            key = key.strip()
            value = value.strip()
            # Store the key-value pair in the current_adjunct_dict dictionary
            current_user_dict[key] = value
        else:  # If line is empty, it indicates end of current student's data
            if current_user_dict:  # If current_adjunct_dict is not empty
                # Create a Student object for the current adjunct and add it to students list
                _adjunct = make_adjunct_obj(current_user_dict)
                all_users.append(_adjunct)
                # Clear data for next user
                current_user_dict = {}

    # If there is remaining data after the last student
    if current_user_dict:
        all_users.append(make_adjunct_obj(current_user_dict))

    return all_users


def add_adjuncts_to_csv(a_list: list) -> None:
    with open(ADJUNCT_CSV, "a", newline="") as file:
        writer_object = writer(file)
        # Print all employee objects
        adjunct: Adjunct
        for adjunct in a_list:
            print(f"part 1 due date: {adjunct.p1_due}")
            _data = [adjunct.first_name, adjunct.last_name, adjunct.user_id,
                     adjunct.supervisor, adjunct.mentor, adjunct.program, adjunct.p1_due, 
                     adjunct.p2_due, adjunct.p3_due, adjunct.p4_due]
            writer_object.writerow(_data)
        
        file.close()


def loop_csv() -> None:
    with open(ADJUNCT_CSV, mode="r") as file:
        csvFile = DictReader(file)
        for user in csvFile:
            if not does_user_exist(user["user_id"]):
                Logger.info(f"User{user["user_id"]} was not found. Creating account now")
                create_user(user_ID=user["user_id"], f_name=user["f_name"], l_name=user["l_name"], email=f"{user["user_id"]}@fvtc.edu")
                sleep(2)


            # Enroll into part 1
            enroll_user(user_ID=user["user_id"], course_id=PART_1_COURSE_ID, role="Student")
            update_grade_entry(course_id=PART_1_COURSE_ID, column_id=PART_1_GB_ID["due_date"], user_id=user["user_id"], new_value=user["p1_due"])
            update_grade_entry(course_id=PART_1_COURSE_ID, column_id=PART_1_GB_ID["mentor"], user_id=user["user_id"], new_value=user["mentor"])
            update_grade_entry(course_id=PART_1_COURSE_ID, column_id=PART_1_GB_ID["dean"], user_id=user["user_id"], new_value=user["supervisor"])
            update_grade_entry(course_id=PART_1_COURSE_ID, column_id=PART_1_GB_ID["program"], user_id=user["user_id"], new_value=user["program"])
            sleep(2)
            # Enroll into part 2
            enroll_user(user_ID=user["user_id"], course_id=PART_2_CURRENT_CHILD_ID, role="Student")
            update_grade_entry(course_id=PART_2_PARENT_ID, column_id=PART_2_GB_ID["due_date"], user_id=user["user_id"], new_value=user["p2_due"])
            update_grade_entry(course_id=PART_2_PARENT_ID, column_id=PART_2_GB_ID["dean"], user_id=user["user_id"], new_value=user["supervisor"])
            update_grade_entry(course_id=PART_2_PARENT_ID, column_id=PART_2_GB_ID["program"], user_id=user["user_id"], new_value=user["program"])
            
            # print(f"first name: {user["f_name"]}")
            # print(f"last name: {user["l_name"]}")
            # print(f"id: {user["user_id"]}")
            # print(f"supervisor: {user["supervisor"]}")
            # print(f"mentor: {user["mentor"]}")
            # print(f"program: {user["program"]}")
            # print(f"p1: {user["p1_due"]}")
            # print(f"p2: {user["p2_due"]}")
            # print(f"p3: {user["p3_due"]}")
            # print(f"p4: {user["p4_due"]}")


if __name__ == "__main__":
    create_adjunct_training_csv()
    adjuncts = parse_adjunct_txt(file_path=FILE_PATH)
    add_adjuncts_to_csv(a_list=adjuncts)
    loop_csv()