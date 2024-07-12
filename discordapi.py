import requests
import urllib
import time

class API:
    def __init__(self, token):
        self.token = token

    def _raw_request_channels(self, method: str, channel_id: int, section: str, params: dict = {}):
        method_table = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete,
            "PATCH": requests.patch
        }

        url = f"https://discord.com/api/v9/channels/{channel_id}/{section}?{urllib.parse.urlencode(params)}"

        resp = method_table[method.upper()](url, headers={
            "Authorization": self.token
        })

        resp.raise_for_status()

        return resp.json()

    def fetch_messages(self, channel_id, limit, before=None, after=None):
        params = {
            "limit": limit
        }
        if before != None:
            params["before"] = before
        if after != None:
            params["after"] = after

        resp = self._raw_request_channels("GET", channel_id, "messages", params)

        return resp
