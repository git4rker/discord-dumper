from discordapi import API
import datetime

class Channel:
    def __init__(self, id: int, api: API):
        self.id = id
        self.api = api
        self.last_message_id = None
        self.object = self._get_api_object()
        self.n_msg = 0

    def _get_api_object(self):
        return self.api.request("GET", f"channels/{self.id}")

    def restore(self, data):
        self.last_message_id = data["last_message_id"]
        self.n_msg = data["n_msg"]

    def get_messages(self):
        params = {
            "limit": 100
        }

        if self.last_message_id != None:
            params["before"] = self.last_message_id

        resp = self.api.request("GET", f"channels/{self.id}/messages", params)

        n_msg = len(resp)
        self.n_msg += n_msg

        if n_msg != 0:
            self.last_message_id = min(resp, key = lambda m: datetime.datetime.fromisoformat(m["timestamp"]))["id"]

        return n_msg, resp