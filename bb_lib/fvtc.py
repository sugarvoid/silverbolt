
from bb_lib.course import enroll_user, unenroll_user

"""
This module provides functions specific to Fox Valley Technical College. 

Functions in this module allow you to create, delete, and update course information,
as well as query details about existing courses. The primary goal of this module
is to facilitate course management operations for the platform administrators.

Author: David Durham

License: MIT
"""

FILE_PATH = "data/adjunct_list.txt"
ADJUNCT_CSV = "data/adjunct_training.csv"
PART_1_COURSE_ID = "ADJPART12020"
PART_2_PARENT_ID = "AdjTrainingPART2D23"
PART_2_CURRENT_CHILD_ID = "AdjTrainingPART2-2024"

COURSE_ID = {
    "ADJUNCT_PART_1" : "",

}




#TODO: Move separate script files here. 

def add_users_to_adjunct_training(list_file_path: str) -> None:
    """Add adjunct instructors to training courses. (Part 1 and part 2 only)

    Args:
        list_file_path (str): The path to the .txt file with the list of instructors and their needed information. 
    """
    pass


def add_users_to_start_college_now(list_file_path: str) -> None:
    """Add students into the Start College Now course.

    Args:
        list_file_path (str): The path to the .txt file with the list of students and their needed information. 
    """
    pass

def add_rest_to_course_copy_csv(csv_path: str) -> None:
    """Add the '(Section X)' and -2024[semester] to the course copy csv file.  

    Args:
        csv_path (str): The file needing updating. 
    """

    #load file
    #loop though
        # update title based on section number in course ID
        # update course ID 
    # save file

    pass

def trent_enrollment(course_id: str, add: bool = True) -> None:
    if add:
        enroll_user(user_ID="200183336", course_id=course_id, role="Instructor")
    else:
        unenroll_user(user_id="200183336", course_id=course_id)