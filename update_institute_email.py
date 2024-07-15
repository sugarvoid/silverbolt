
from time import sleep
import requests
#from token_manager import TokenManager
from csv import DictReader, writer
from bb_lib.core import ORG_DOMAIN
from bb_lib.auth import get_access_token


LIST_FILE = "data/add_i_email.csv"
#token_manager = TokenManager()

page_num = 1

user_list = []

def make_user_csv() -> None:
    
    
    
    get_users = f"{ORG_DOMAIN}/learn/api/public/v1/users?page={page_num}&limit=6"


    response = requests.get(get_users, headers={
    'Authorization': 'Bearer ' + get_access_token(),
    'Content-Type': 'application/json'
    })

    #print(response.json())


    if response.status_code == 200:
        data = response.json()
        for user in data["results"]:
            #print(user["name"]["given"])
            _username = user["userName"]
            if len(_username) == 9 and _username.isnumeric():
                _inst_email = f"{_username}@fvtc.edu"
                print(_username)
                user_list.append([_username, _inst_email])
            else:
                # not valid id"
                pass
            ## print(user["contact"]["institutionEmail"])
    
    user_list_clean = list(filter(None, user_list))
           
    with open("data/all_users.csv", "a", newline="") as file:
        writer_obj = writer(file)
        
        for user_obj in user_list_clean:
            writer_obj.writerow([user_obj[0], user_obj[1]])
        file.close()

def set_institution_email(user_id: str) -> None:
    if len(user_id) == 9 and user_id.isnumeric():
        i_email = f"{user_id}@fvtc.edu"
        _data = {
            "contact": {
                "institutionEmail": f"{i_email}",
            },
        }
        update_i_email = f"{ORG_DOMAIN}/learn/api/public/v1/users/userName:{user_id}"

        response = requests.patch(update_i_email, headers={
        'Authorization': 'Bearer ' + get_access_token(),
        'Content-Type': 'application/json'
        }, json=_data)

        #print(response.text)

        if response.status_code == 200:
            ##data = res_user_data.json()
            print("email was updated")
    else:
                # not valid id"
        pass

    
        
if __name__ == '__main__':
    with open(LIST_FILE, mode ='r') as file:    
        csvFile = DictReader(file)
        for u in csvFile:
                set_institution_email(u['username'])
                sleep(5)