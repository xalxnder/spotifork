import requests
import base64
import os

# Obtained from your app dashboard
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
# Obtained after the initial user authorization request
CODE = os.getenv("CODE")
STATE = os.getenv("STATE")
# Obtained in the response body when requesting the access token
ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

AUTH_URL = "https://accounts.spotify.com/api/token"


class SpotifyConnector:
    def get_auth_base64(self, id, secret):
        """Used to encode our Client ID and Client Secret when retriving your refresh token"""
        message = f"{id}:{secret}"
        message_bytes = message.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("ascii")
        auth_header = {"Authorization": "Basic" + " " + base64_message}
        return auth_header

    def getToken(self, CLIENT_ID, CLIENT_SECRET):
        """Used to retrieve your access token AFTER the user initially accepts your request"""
        message = f"{CLIENT_ID}:{CLIENT_SECRET}"
        message_bytes = message.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("ascii")
        auth_header = {"Authorization": "Basic" + " " + base64_message}
        auth_data = {
            "grant_type": "authorization_code",
            "code": CODE,
            "redirect_uri": "https://example.com",
        }
        r = requests.post(AUTH_URL, headers=auth_header, data=auth_data)
        response = r.json()

    def get_refresh_token(self):
        """Used to generate a refresh token"""
        refresh_body = {
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN,
        }
        headers = self.get_auth_base64(CLIENT_ID, CLIENT_SECRET)
        token = requests.post(AUTH_URL, headers=headers, data=refresh_body).json()
        return token["access_token"]
