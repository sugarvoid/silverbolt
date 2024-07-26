
import json
import requests
from dotenv import load_dotenv
from os import getenv
from urllib.parse import urlparse, parse_qs

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


def _get_external_id(url: str) -> str:
    url = url 
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    course_id = query_params.get('course_id', [None])[0]

    return course_id



if __name__ == "__main__":
    #postTeamsMessage("Testing message 4")
    url = "https://blackboard.fvtc.edu/webapps/blackboard/execute/courseMain?course_id=_124909_1"
    print(_get_external_id("https://blackboard.fvtc.edu/webapps/blackboard/execute/announcement?method=search&context=course&course_id=_67414_1&handle=cp_announcements&mode=cpview"))


