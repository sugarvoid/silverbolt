import re
from bb_lib.csv_templates import create_new_hire_list_csv
from bb_lib.logger import Logger
from bb_lib.user import does_user_exist, create_user
from csv import DictReader, writer


FILE_PATH = "data/new_hires.txt"
NEW_HIRE_CVS = "data/new_hires.csv"
ALL_ROLES_LIST = "data/all_roles.txt"
file_path = 'employees.txt'  


def add_role_to_list(role: str) -> None:
    with open(ALL_ROLES_LIST, "a") as _file:
        _file.write(role + "\n")

# Define the Employee class
class Employee:
    def __init__(self, first_name, last_name, id_number, email, position):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = id_number
        self.email = email
        self.position = position
        add_role_to_list(position)

    def __repr__(self):
        return (f"Employee(first_name='{self.first_name}', last_name='{self.last_name}', "
                f"id_number='{self.user_id}', email='{self.email}', position='{self.position}')")

# Function to parse an individual employee data string
def parse_employee(data):
    # Extracting information using regular expressions
    name_match = re.search(r'Employee: (\w+), (\w+) \((\d+)\)', data)
    email_match = re.search(r'Email: (\S+)', data)
    position_match = re.search(r'Position: (.+)', data)

    if name_match and email_match and position_match:
        last_name = name_match.group(1)
        first_name = name_match.group(2)
        id_number = name_match.group(3)
        email = email_match.group(1)
        position = position_match.group(1)

        # Create and return an Employee object
        return Employee(first_name, last_name, id_number, email, position)
    else:
        raise ValueError("Invalid data format")

# Function to parse multiple employees from a file
def parse_employees_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Split the data by two newlines to separate different employee entries
    employee_data_entries = content.split('\n\n')

    employees = []
    for entry in employee_data_entries:
        entry = entry.strip()  # Remove any leading/trailing whitespace
        if entry:  # Ensure the entry is not empty
            try:
                employee = parse_employee(entry)
                employees.append(employee)
            except ValueError as e:
                print(f"Error parsing entry: {entry}\n{e}")

    return employees




## user_id,f_name,l_name,email,position
def main(): 
    create_new_hire_list_csv()
    employees = parse_employees_from_file(FILE_PATH)

    with open(NEW_HIRE_CVS, "a", newline="") as file:
        writer_object = writer(file)
        employee: Employee
        for employee in employees:
            _data = [employee.user_id, employee.first_name, employee.last_name, employee.email, employee.position]
            writer_object.writerow(_data)
        file.close()
    with open(NEW_HIRE_CVS, mode="r") as file:
        csvFile = DictReader(file)
        for n_hire in csvFile:
            if not does_user_exist(n_hire["user_id"]):
                Logger.info(f"User {n_hire["user_id"]} is not in system. Creating it now.")
                create_user(username=n_hire["user_id"], f_name=n_hire["f_name"], l_name=n_hire["f_name"], email=n_hire["email"])
            


if __name__ == "__main__":
    main()