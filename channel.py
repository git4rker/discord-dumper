class Channel:
    def __init__(self, name, channel_id):
        self.name = name
        self.id = channel_id
        self.last_msg = None
        self.msg_counter = 0
        self.enabled = True