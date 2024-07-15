
from datetime import datetime
from dotenv import load_dotenv
from requests import get, post
from os import getenv
from bb_lib.auth import get_access_token
from bb_lib.core import ORG_DOMAIN
from bb_lib.logger import Logger

load_dotenv()


DEFAULT_PASSWORD = getenv("DEFAULT_PASSWORD")


class BBUser:
    user_ID: str
    first_name: str 
    last_name: str
    email: str
    roles: list
    lastLogin: datetime.date

    
def create_user(username: str, f_name: str, l_name:str, email: str) -> None:
    """Creates a user.

    Args:
        username (str): New user's ID number
        f_name (str): New user's first name
        l_name (str): New user's last name
        email (str): New user's email address

    Returns:
        int: _description_
    """
    username = username.strip()
    f_name = f_name.strip()
    l_name = l_name.strip()
    email = email.strip()


    if not all([username, f_name, l_name]):
        raise ValueError("All parameters (user_ID, f_name, l_name, email) must be non-empty strings.")
    
    make_user = f"{ORG_DOMAIN}/learn/api/public/v1/users"
    data = {
        'userName': f"{username}",
        "password": f"{DEFAULT_PASSWORD}",
        "availability": {
            "available": "Yes"
        },
        "name": {
            "given": f"{f_name}",
            "family": f"{l_name}",
            "preferredDisplayName": "GivenName"
        },
        "contact": {
            "email": f"{email}",
        },
    }

    response = post(make_user, headers={
    'Authorization': 'Bearer ' + get_access_token(),
    'Content-Type': 'application/json'
    }, json=data)

    match response.status_code:
        case 201:
            Logger.info(f"User {username}, was created successfully")
        case 403:
            Logger.error("The currently authenticated user has insufficient privileges to create a new user.")
        case 409:
            Logger.error(f"A user with the ID of {username} already exists.")
        case 400:
            Logger.error(f"An error occurred while creating the new user. {response.text}")
    
    
    #return response.status_code

def delete_user(username: str) -> int:
    """
    Delete a user from the system.

    Args:
        username (str): The unique user ID of the user to be deleted. 

    Returns:
        int: _description_
    """
    # TODO: Maybe return status code?? 
    #TODO: Create this function
    pass

def get_user(username: str) -> BBUser:
    """
    Gets a user from the system and loads their data in BBUser object. 

    Args:
        username (str): The unique user ID of the user to be gathered. 

    Returns:
        BBUser: _description_
    """

    user: BBUser = BBUser()

    get_user_data = f"{ORG_DOMAIN}/learn/api/public/v1/users/userName:{username}"


    res_user_data = get(get_user_data, headers={
    'Authorization': 'Bearer ' + get_access_token(),
    'Content-Type': 'application/json'
    })

    if res_user_data.status_code == 200:
        data = res_user_data.json()
        user.roles = (data["institutionRoleIds"])
        user.first_name = (data["name"]["given"])
        user.last_name = (data["name"]["family"])

        return user
    

def get_username_from_id(user_id: str) -> BBUser:
    """
    Gets a user from the system and loads their data in BBUser object. 

    Args:
        username (str): The unique user ID of the user to be gathered. 

    Returns:
        BBUser: _description_
    """


    get_user_data = f"{ORG_DOMAIN}/learn/api/public/v1/users/{user_id}"


    res_user_data = get(get_user_data, headers={
    'Authorization': 'Bearer ' + get_access_token(),
    'Content-Type': 'application/json'
    })

    if res_user_data.status_code == 200:
        data = res_user_data.json()
        
        return data.get("userName", "")


def does_user_exist(username: str) -> bool:
    """Checks to see if a user is already added to the system. 

    Args:
        username (str): _description_

    Returns:
        bool: True if user is already in the system.
    """
    get_user = f"{ORG_DOMAIN}/learn/api/public/v1/users/userName:{username}"
    response = get(get_user, headers={'Authorization': 'Bearer ' + get_access_token()})
    #print(response.text)
    if response.status_code == 200:
        return True
    else:
        return False


def get_needed_roles(position: str) -> list:
    match position:
        case "k_12":
            return ['K-12', 'Faculty']
        case "adjunct":
            return ['Faculty']
        case "ncjtc":
            return ['Faculty','NCJTICCJ','NCJTCICAC','NCJTCPublic']
        case "support":
            return ['Student']
        case "instructor":
            return ['Faculty']
        case _:
            return []