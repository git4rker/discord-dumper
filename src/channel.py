from discordapi import API
import datetime

class Channel:
    def __init__(self, id: int, api: API):
        self.id = id
        self.api = api

        self.last_message_id = None
        self.object = self._get_api_object()

    def _get_api_object(self):
        return self.api.request("GET", f"channels/{self.id}")

    def get_messages(self):
        params = {
            "limit": 100
        }

        if self.last_message_id != None:
            params["before"] = self.last_message_id

        resp = self.api.request("GET", f"channels/{self.id}/messages", params)

        if len(resp) != 0:
            self.last_message_id = min(resp, key = lambda m: datetime.datetime.fromisoformat(m["timestamp"]))["id"]

        return resp