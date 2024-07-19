
import json
import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

WEBHOOK_URL = getenv("TESTING_TEAMS_WEBHOOK_URL")

def postTeamsMessage(text):
    j_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": [{"type": "TextBlock", "text": f"{text}"}],
                },
            }
        ],
    }
 
    headers = {"Content-Type": "application/json"}
    response = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(j_data))
    if response.status_code == 202:
        print("Message sent successfully")
    else:
        print("Failed to send message:", response)


if __name__ == "__main__":
    postTeamsMessage("Testing message 4")


