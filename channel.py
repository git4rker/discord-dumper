from enum import Enum

class Channel:
    class Status(Enum):
        NO_MESSAGES_LEFT = 1
    
    def __init__(self, name, channel_id, api):
        self.name = name
        self.id = channel_id
        self.last_msg = None
        self.msg_counter = 0
        self.api = api

    def update(self):
        messages = self.api.fetch_messages(self.id, before=self.last_msg, limit=100)

        msg_n = len(messages)
        self.msg_counter += msg_n

        if msg_n != 0:
            self.last_msg = messages[-1]["id"]

        return messages