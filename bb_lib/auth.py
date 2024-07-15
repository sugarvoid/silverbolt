import time
import requests
import json
import os
from dotenv import load_dotenv

from bb_lib.core import ORG_DOMAIN
from bb_lib.logger import Logger


load_dotenv()


## CLIENT_ID = os.getenv("APP_KEY")
## client_secret = os.getenv("SECRET")

class TokenManager(object):
    token_file = "data/token_cache.json"
    def __new__(cls):
        obj = super().__new__(cls)
        obj.token = None
        obj.expiry_time = 0
        obj.load_token()
        return obj
    
    def __str__(self) -> str:
        return f"Token = {self.token}. Expiration time = {self.expiry_time}"

    def get_token(self):
        current_time = time.time()
        if not self.token or current_time >= self.expiry_time:
            self.request_new_token()
            self.save_token()
        return self.token

    def request_new_token(self):
        _client_id = os.getenv("APP_KEY")
        _client_secret = os.getenv("SECRET")
        _token_url =f'{ORG_DOMAIN}/learn/api/public/v1/oauth2/token'
        _token_response = requests.post(_token_url, data={
            "grant_type": "client_credentials"},
            auth=(_client_id,_client_secret))
        match _token_response.status_code:
            #TODO: Add other cases
            case 200:
                Logger.info("A new token was generated.")
                self.token = _token_response.json()['access_token']
                _expires_in = _token_response.json()['expires_in']
                self.expiry_time = time.time() + _expires_in - 60  # Subtracting 60 seconds to ensure the token is refreshed a bit before it actually expires
            case _:
                Logger.critical(f"Failed to get a token. {_token_response.text}")
            

    def load_token(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as file:
                data = json.load(file)
                self.token = data.get('token')
                self.expiry_time = data.get('expiry_time', 0)


    def save_token(self):
        data = {
            'token': self.token,
            'expiry_time': self.expiry_time
        }
        with open(self.token_file, 'w') as file:
            json.dump(data, file)


def get_access_token() -> str:
    token_manager = TokenManager()
    return token_manager.get_token()