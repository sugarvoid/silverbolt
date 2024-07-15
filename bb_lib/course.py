"""
This module provides functions for managing courses in an blackboard.

Functions in this module allow you to create, delete, and update course information,
as well as query details about existing courses. The primary goal of this module
is to facilitate course management operations for the platform administrators.

Author: David Durham

License: MIT
"""

from csv import DictReader, writer
from datetime import datetime
from time import sleep
from bb_lib.core import ORG_DOMAIN
from bb_lib.auth import get_access_token
from requests import delete, get, patch, post, put

from bb_lib.logger import Logger
from bb_lib.user import BBUser, create_user, does_user_exist, get_username_from_id


def format_date(date_string: str) -> str:
    """Takes in the date format blackboard uses and changes it to xx/xx/xxxx

    Args:
        date_string (str): Timestamp in ISO 8601. Example: "2024-06-27T14:15:14.634Z"

    Returns:
        str: Example "06/27/2024"
    """

    _datetime_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
        "%m-%d-%Y"
    )

    return _datetime_obj


class BBCourse:
    def __init__(
        self,
        course_id: str,
        name: str,
        created: str,
        last_updated: str,
        term: str,
    ) -> None:
        self.course_id = course_id
        self.name = name
        self.created = format_date(created)
        self.last_updated = format_date(last_updated)
        self.instructor: list
        self.term = get_term_from_raw_id(term)


SPRING_24 = ""
SUMMER_24 = "_273_1"
MASTER = "_26_1"
FALL_24 = "_268_1"


def get_term_from_code(term_code: str) -> str:
    if term_code == "0":
        return MASTER
    if term_code == "1":
        return SPRING_24
    if term_code == "2":
        return SUMMER_24
    if term_code == "3":
        return FALL_24


def get_term_from_raw_id(term_id: str) -> str:
    match term_id:
        case "_26_1":
            return "MASTER"
        case "_268_1":
            return "Fall 2024"
        case "_273_1":
            return "Summer 2024"
        case _:
            Logger.critical(f"Add this course: {term_id}")
            return "need to add"
    # TODO: Add the rest


def enroll_users_from_csv(csv_path: str):
    with open(csv_path, mode="r") as file:
        csvFile = DictReader(file)
        for u in csvFile:
            enroll_user(user_ID=u["user_id"], course_id=u["course_id"], role=u["role"])


def enroll_user(user_ID: str, course_id: str, role: str = "Student") -> None:
    #user: BBUser = BBUser()

    _data = {
        # "childCourseId": "string",
        # "dataSourceId": "string",
        "availability": {"available": "Yes"},
        "courseRoleId": role,
        # "displayOrder": 0
    }

   # x = "/learn/api/public/v1/courses/{courseId}/users/userName:{user_ID}"

    add_to_course = f"{ORG_DOMAIN}/learn/api/public/v1/courses/courseId:{course_id}/users/userName:{user_ID}"

    res_user_data = put(
        add_to_course,
        headers={
            "Authorization": "Bearer " + get_access_token(),
            "Content-Type": "application/json",
        },
        json=_data,
    )

    ##print(res_user_data.text)

    if res_user_data.status_code == 409:
        data = res_user_data.json()
        Logger.error(f"User {user_ID} is in course {course_id} already")

    if res_user_data.status_code == 201:
        data = res_user_data.json()
        Logger.info(f"{user_ID} has been added to {course_id}, as {role}")


def unenroll_user(user_id: str, course_id: str) -> None:
    """
    Remove a student from a course.

    Args:
        course_id (str):
    """
    # TODO: rename
    _remove_user = f"{ORG_DOMAIN}/learn/api/public/v1/courses/courseId:{course_id}/users/userName:{user_id}"

    _response = delete(
        _remove_user,
        headers={
            "Authorization": "Bearer " + get_access_token(),
            "Content-Type": "application/json",
        },
    )

    if _response.status_code == 204:
        Logger.info(f"{user_id} was removed from {course_id}.")
    else:
        print(f"Request failed, check logs. {Logger.get_file_path()}")
        Logger.error(f"Failed to remove {user_id} from course. {_response.text}")


# TODO: Add def to add child course

# TODO: Add def for bulk creation from csv file


def remove_by_role(course_id: str, role: str) -> None:
    my_guys = get_users_in_course(course_id=course_id, role=role)

    for u in my_guys:
        unenroll_user(
            get_username_from_id(user_id=u.get("userId")), course_id=course_id
        )


def create_empty_course(course_id: str, course_name: str) -> None:
    """Creates an empty course. Used for when it will be a child course

    Args:
        course_id (str): The ID of the course.
        course_name (str): The name of the course. 
    """
    _data = {
        # "externalId": "string",
        # "dataSourceId": "string",
        "courseId": f"{course_id}",
        "name": f"{course_name}",
        # "description": "",
        "organization": False,
        "ultraStatus": "Classic",
        "allowGuests": True,
        "allowObservers": True,
        # "closedComplete": true,
        # "termId": "string",
        "availability": {
            "available": "No",
            "duration": {
                "type": "Continuous",
            },
        },
        "enrollment": {
            "type": "InstructorLed",
        },
    }

    make_course = f"{ORG_DOMAIN}/learn/api/public/v3/courses"

    response = post(
        make_course,
        headers={
            "Authorization": "Bearer " + get_access_token(),
            "Content-Type": "application/json",
        },
        json=_data,
    )

    # TODO: Add other possible response codes

    if response.status_code == 201:
        ##data = res_user_data.json()
        print(f"Empty original course: {course_id} was created")
        Logger.info(f"Empty original course: {course_id} was created")

    else:
        Logger.error(response.text)


def copy_courses_from_csv(csv_path: str):
    with open(csv_path, mode="r") as file:
        csvFile = DictReader(file)
        for c in csvFile:
            copy_course(
                master_id=c["master_id"],
                copy_id=c["course_id"],
                forum_option=c["forum_option"],
            )
            sleep(5)
            if c["forum_option"] == "a":
                Logger.info(f"Removing old students from{c["course_id"]}")
                remove_by_role(course_id=c["course_id"], role="Student")
            # print(c['course_name'])


# TODO: Make forum choice an option in args
def copy_course(master_id: str, copy_id: str, forum_option: str) -> None:
    if forum_option not in ("a", "f", "fs"):
        raise ValueError(
            "The forum option only takes in 'a'(all), 'f'(forums), or 'fs(forums+starter)' "
        )
        return

    _data = {
        "targetCourse": {
            "courseId": f"{copy_id}",
            # "id": {}
        }
    }

    if forum_option in ("f", "fs"):
        _forums = ""
        if forum_option == "f":
            _forums = "ForumsOnly"
            Logger.info(f"Copying only the forums for course {copy_id}")
        elif forum_option == "fs":
            _forums = "ForumsAndStarterPosts"
            Logger.info(f"Copying the forums and starter post for course {copy_id}")

        _data["copy"] = {
            "adaptiveReleaseRules": True,
            "announcements": True,
            "assessments": True,
            "blogs": True,
            "calendar": True,
            "contacts": True,
            "contentAlignments": True,
            "contentAreas": True,
            "discussions": f"{_forums}",
            "glossary": True,
            "gradebook": True,
            "groupSettings": True,
            "journals": True,
            "retentionRules": True,
            "rubrics": True,
            "settings": {
                "availability": False,
                "bannerImage": True,
                "duration": True,
                "enrollmentOptions": True,
                "guestAccess": True,
                "languagePack": True,
                "navigationSettings": True,
                "observerAccess": True,
            },
            "tasks": True,
            "wikis": True,
        }
    else:
        Logger.info(f"Copying all posts from the discussion board in course {copy_id}")

    copy_course = f"{ORG_DOMAIN}/learn/api/public/v2/courses/courseId:{master_id}/copy"

    response = post(
        copy_course,
        headers={
            "Authorization": "Bearer " + get_access_token(),
            "Content-Type": "application/json",
        },
        json=_data,
    )

    if response.status_code == 202:
        ##data = res_user_data.json()
        print(f"course: {copy_id} was created")
        Logger.info(f"course: {copy_id} was successfully created from: {master_id}")

    else:
        print(f"course: {copy_id} failed to was not created. Check log for details. {Logger.get_file_path()}")
        Logger.error(response.text)


def change_student_availability(student_id: str, course_id: str, available: str = "No"):
    """Update a student's availability in a course 

    Args:
        student_id (str): _description_
        course_id (str): _description_
        available (str, optional): _description_. Defaults to "No".
    """

    _data = {
    #"dataSourceId": "string",
    "availability": {
        "available": {available}
    },
    #"courseRoleId": "Instructor",
    #"displayOrder": 0
    }
    
    update_course = f"{ORG_DOMAIN}/learn/api/public/v1/courses/courseId:{course_id}/users/userName:{student_id}"

    response = patch(update_course, headers={
    'Authorization': 'Bearer ' + get_access_token(),
    'Content-Type': 'application/json'
    }, json=_data)



    if response.status_code == 200:
        ##data = res_user_data.json()
        Logger.info(f"{student_id} has been made unavailable in course {course_id}")



def override_course(old_course_id: str, source_id: str) -> None:
    """Deletes an old course and recopies it from a source course. 

    Args:
        old_course_id (str): The course ID of the course to override.
        source_id (str): The course ID of the course to use to make new copy
    """
    #TODO: Finish this
    # Delete the old master
    # Copy over desired_course --> new master 
    # Rename course
    # Add instructor to new master 
    # Change term to master 


def update_course_post_copy(
    course_id: str, term_id: str, new_name: str, instructors: list = []
) -> None:
    _data = {
        "name": f"{new_name}",
        "termId": f"{term_id}",
        "availability": {
            "available": "No",
            "duration": {
                "type": "Continuous",
            },
        },
    }

    update_course = f"{ORG_DOMAIN}/learn/api/public/v3/courses/courseId:{course_id}"

    response = patch(
        update_course,
        headers={
            "Authorization": "Bearer " + get_access_token(),
            "Content-Type": "application/json",
        },
        json=_data,
    )

    # print(response.text)

    if response.status_code == 200:
        ##data = res_user_data.json()
        Logger.info(
            f"Course {course_id} has been renamed to {new_name} and put in {get_term_from_raw_id(term_id)} term"
        )
        for i in instructors:
            enroll_user(user_ID=i, course_id=course_id, role="Instructor")


def update_courses_from_csv(csv_path: str) -> None:
    with open(csv_path, mode="r") as file:
        csvFile = DictReader(file)
        for c in csvFile:
            _instructors = []
            _instructors.append(c["instructor_1"])
            _instructors.append(c["instructor_2"])
            _instructors.append(c["instructor_3"])
            _instructors = list(filter(None, _instructors))
            _term = get_term_from_code(c["term"])
            update_course_post_copy(
                course_id=c["course_id"],
                term_id=_term,
                new_name=c["course_name"],
                instructors=_instructors,
            )
            sleep(10)


# TODO: remove modified date, not accurate
def get_course(course_id: str) -> BBCourse:
    get_course_data = f"{ORG_DOMAIN}/learn/api/public/v3/courses/{course_id}"

    res_user_data = get(
        get_course_data,
        headers={
            "Authorization": "Bearer " + get_access_token(),
            "Content-Type": "application/json",
        },
    )

    if res_user_data.status_code == 200:
        course = res_user_data.json()
        course_obj: BBCourse = BBCourse(
            course.get("externalId"),
            course.get("name"),
            course.get("created"),
            course.get("modified"),
            course.get("termId"),
        )
        return course_obj


def get_course_report(c_ids: list, username: str) -> None:
    _courses = []
    _headers = [["Course ID", "Name", "Created", "Updated", "Term"]]
    for c in c_ids:
        _courses.append(get_course(c))

    with open(f"outbox/courses_{username}.csv", mode="w", newline="") as file:
        _writer = writer(file)
        _writer.writerows(_headers)

    c_obj: BBCourse
    for c_obj in _courses:
        cvs_row = [
            c_obj.course_id,
            c_obj.name,
            c_obj.created,
            c_obj.last_updated,
            c_obj.term,
        ]
        with open(f"outbox/courses_{username}.csv", "a", newline="") as file:
            writer_object = writer(file)
            writer_object.writerow(cvs_row)
            file.close()


def get_user_courses(user_id: str) -> None:
    get_courses_data = (
        f"{ORG_DOMAIN}/learn/api/public/v1/users/userName:{user_id}/courses"
    )
    _all_course_ids = []

    res_user_data = get(
        get_courses_data,
        headers={
            "Authorization": "Bearer " + get_access_token(),
            "Content-Type": "application/json",
        },
    )

    if res_user_data.status_code == 200:
        courses = res_user_data.json().get("results", [])
        for course in courses:
            _all_course_ids.append(course["courseId"])
            # print(course['courseId'])

    get_course_report(_all_course_ids, user_id)


def get_users_in_course(course_id: str, role: str = "") -> list:
    get_list = f"{ORG_DOMAIN}/learn/api/public/v1/courses/externalId:{course_id}/users"
    _all_users = []
    _selected_role = []

    res_user_data = get(
        get_list,
        headers={
            "Authorization": "Bearer " + get_access_token(),
            "Content-Type": "application/json",
        },
    )

    if res_user_data.status_code == 200:
        _all_users = res_user_data.json().get("results", [])

    for user in _all_users:
        if user.get("courseRoleId") == role:
            _selected_role.append(user)

    return _selected_role


def delete_course(course_id: str) -> None:
    """
    Delete a course from the database.

    Args:
        course_id (str): The unique identifier of the course to be deleted.
    """
    _delete_course = f"{ORG_DOMAIN}/learn/api/public/v3/courses/courseId:{course_id}"

    _response = delete(
        _delete_course,
        headers={
            "Authorization": "Bearer " + get_access_token(),
            "Content-Type": "application/json",
        },
    )

    if _response.status_code == 202:
        Logger.info(f"{course_id} was deleted.")
    else:
        print(f"Request failed, check logs. {Logger.get_file_path()}")
        Logger.error(f"Failed to delete course {course_id}. {_response.text}")



def run_course_copy(csv_path: str) -> None:
    copy_courses_from_csv("data/course_copy.csv")
    sleep(60)
    update_courses_from_csv("data/course_copy.csv")

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