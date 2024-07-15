# Silverbolt 

A python wrapper of the blackboard api to simplify admin tasks such as managing courses and users.  


## Setup 
### Needed in .env file
To use these functions, you will need a .env file with the following items. 
You can request access to the Blackboard REST APIs through the [Developer Portal](https://developer.blackboard.com/). You will need to create an application to get the needed keys. 
```
APP_KEY="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
APP_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
ORG_DOMAIN="https://blackboard.your_org.edu"
```

## Example of using the library 
```python
from bb_lib.user import create_user, does_user_exist

if not does_user_exist("123456789") then:
    create_user(username="123456789", f_name="john", l_name="cena", email="youcantseeme@email.com")
```

## Current Capabilities  

### User
```python
create_user(username: str, f_name: str, l_name:str, email: str) -> None
delete_user(username: str) -> int
does_user_exist(username: str) -> bool
```
### Course
```python
enroll_user(user_ID: str, course_id: str, role: str = "Student") -> None
```
### FVTC Specific 

#### Enroll Adjunct 
```python
add_users_to_adjunct_training(list_file_path: str) -> None
add_users_to_start_college_now(list_file_path: str) -> None
```
