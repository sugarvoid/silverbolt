"""
This script updates the institution email for users.

Author: David Durham
Date: 7/19/2024
License: MIT

"""

from time import sleep
from requests import patch
from csv import DictReader
from bb_lib.core import ORG_DOMAIN
from bb_lib.auth import get_access_token
from bb_lib.logger import Logger


LIST_FILE = "data/full_list_users_part.csv"

def update_institution_email(user_id: str) -> None:
    if len(user_id) == 9 and user_id.isnumeric():
        i_email = f"{user_id}@fvtc.edu"
        _data = {
            "contact": {
                "institutionEmail": f"{i_email}",
            },
        }
        update_i_email = f"{ORG_DOMAIN}/learn/api/public/v1/users/userName:{user_id}"

        response = patch(
            update_i_email,
            headers={
                "Authorization": "Bearer " + get_access_token(),
                "Content-Type": "application/json",
            },
            json=_data,
        )

        # print(response.text)

        if response.status_code == 200:
            Logger.info(f"{user_id}'s institution email was updated to {i_email}")
        else:
            Logger.error(f"Updating {user_id}'s institution email failed. {response}")
    else:
        Logger.info(f"Skipping {user_id}. Not correct format.")


if __name__ == "__main__":
    with open(LIST_FILE, mode="r") as file:
        csvFile = DictReader(file)
        for u in csvFile:
            update_institution_email(u["username"])
            sleep(1)
