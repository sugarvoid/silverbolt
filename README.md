# Silverbolt 

**This project is a work in progress. Get an understanding of the code and what it does before using**<br>
A python wrapper of the blackboard api to simplify admin tasks such as managing courses and users.  


# Setup 
### Needed in .env file
To use these functions, you will need a .env file with the following items. 
You can request access to the Blackboard REST APIs through the [Developer Portal](https://developer.blackboard.com/). You will need to create an application to get the needed keys. 
```javascript
APP_KEY="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
APP_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
ORG_DOMAIN="https://blackboard.your_org.edu"
```

# Example of using the library 
```python
from bb_lib.user import create_user, does_user_exist

if not does_user_exist("123456789") then:
    create_user(username="123456789", f_name="john", l_name="cena", email="youcantseeme@email.com")
```

# Current Capabilities  

## User
 ```python
 # Creates a user
create_user(username: str, f_name: str, l_name:str, email: str) -> None
```
Creates a user

```python
delete_user(username: str) -> int
```
[description]

```python
does_user_exist(username: str) -> bool
```
[description]

## Course<hr>

```python
enroll_user(user_ID: str, course_id: str, role: str = "Student") -> None
```
[description]
```python
enroll_users_from_csv(csv_path: str) -> None
```
[description]
```python
copy_courses_from_csv(csv_path: str) -> None
```
[description]
```python
create_empty_course(course_id: str, course_name: str) -> None:
```
[description]
```python
copy_course(master_id: str, copy_id: str, forum_option: str) -> None
```
[description]
#### `change_student_availability(student_id: str, course_id: str, available: str = "No")`
[description]
#### `get_user_courses(user_id: str) -> None:`
Creates a cvs file with a list of courses where user is an instructor 
#### `def get_users_in_course(course_id: str, role: str = "") -> list:`
Returns a list of users based on their role


## FVTC Specific


### `add_users_to_adjunct_training(list_file_path: str) -> None`
### `add_users_to_start_college_now(list_file_path: str) -> None`
### `run_course_copy(cvs_file_path: str) -> None`
Creates courses from a csv. <br>
Required headers:
- course_name,
- master_id,
- course_id,
- forum_option,
- term,
- instructor_1,
- instructor_2,
- instructor_3
