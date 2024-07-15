


from requests import Response, get, patch
from bb_lib.auth import get_access_token
from bb_lib.core import ORG_DOMAIN
from bb_lib.logger import Logger
from bb_lib.user import BBUser, get_user


def update_grade_entry(course_id: str, column_id: str, user_id: str, new_value: str) -> None:
    """Updates a grade in a specific column 

    Args:
        course_id (str): _description_
        column_id (str): _description_
        user_id (str): The student in the course to update grade
        new_value (str): _description_
    """

    # Get column data for logs
    col_name = ""
    user: BBUser = get_user(username=user_id)
    _get_column_data = f"{ORG_DOMAIN}/learn/api/public/v2/courses/courseId:{course_id}/gradebook/columns/{column_id}"


    response2 = get(_get_column_data, headers={
    'Authorization': 'Bearer ' + get_access_token(),
    'Content-Type': 'application/json'
    })
    #print(response2.text)

    if response2.status_code == 200:
        data = response2.json()
        print(data["name"])
        col_name = data["name"]







    _data = {
    "text": f"{new_value}",
    #"score": 0,
    #"notes": "string",
    #"feedback": "string",
    #"exempt": false,
    }


   

    _update_grade = f"{ORG_DOMAIN}/learn/api/public/v2/courses/courseId:{course_id}/gradebook/columns/{column_id}/users/userName:{user_id}"
    #update_course = f"{ORG_DOMAIN}/learn/api/public/v3/courses/courseId:{course_ID}"



    response: Response = patch(_update_grade, headers={
    'Authorization': 'Bearer ' + get_access_token(),
    'Content-Type': 'application/json'
    }, json=_data)

    #print(response.text)


    if response.status_code == 200:
        ##data = res_user_data.json()
        Logger.info(msg=f"{col_name} for {user.first_name} {user.last_name} was updated to: {new_value}")
        #print(f"{col_name} for {user.first_name} {user.last_name} was updated to: {new_value}")
    else:
        try:
            error_message = response.json().get('message')  # Assuming error details are in JSON format
        except ValueError:
            error_message = response.text  # Fallback to plain text response if JSON parsing fails
    
        Logger.error(msg=f"Failed to update {col_name} for {user.first_name} {user.last_name}. Error: {error_message}")