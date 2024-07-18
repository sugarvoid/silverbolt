
import json
import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

WEBHOOK_URL = getenv("TESTING_TEAMS_WEBHOOK_URL")

def postTeamsMessage(text):
    # Message payload
    j_data = {
        

        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": "",
                "content": {
                    "type": "message",
                    "text": "butts"
                },
            }
        ],
    }

    # Headers
    headers = {"Content-Type": "application/json"}

    # Send the POST request
    response = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(j_data))

    # Check the response
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message:", response)


if __name__ == "__main__":
    postTeamsMessage("Testing notification from pc 3")


