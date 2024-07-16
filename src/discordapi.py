import requests
import urllib

class API:
    def __init__(self, token):
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": token
        })

    def request(self, method: str, target: str, params: dict = {}):
        url = f"https://discord.com/api/v9/{target}?{urllib.parse.urlencode(params)}"

        resp = self._session.request(method, url)
        resp.raise_for_status()

        return resp.json()