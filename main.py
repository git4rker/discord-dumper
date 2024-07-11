from tinydb import TinyDB, Query, where
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage
import signal
import requests
import sys
import time
from discordapi import API
from channel import Channel
import config

api = API(config.TOKEN, config.FAILED_REQUEST_DELAY)
db = TinyDB(config.DATABASE_FILE, storage=CachingMiddleware(JSONStorage))

channels = []

for channel_name, channel_id in config.CHANNELS.items():
    channels.append(Channel(channel_name, channel_id))
    messages = sorted(db.search(where("channel_id") == str(channels[-1].id)), key=lambda k: k["timestamp"])

    if len(messages) == 0:
        continue

    channels[-1].last_msg = messages[0]["id"]
    channels[-1].msg_counter = len(messages)

    print(f"Restored channel {channel_name}")

def sigint_handler(sig, frame):
    print("\nExiting. Please wait...")
    db.close()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

def update_channel(channel):
    messages = api.fetch_messages(channel.id, before=channel.last_msg, limit=100)

    msg_n = len(messages)

    channel.msg_counter += msg_n

    if msg_n == 0:
        channel.enabled = False
        print(f"No messages left in the channel {channel.name}.")
        return
    else:
        channel.last_msg = messages[-1]["id"]

    # print(messages)
    print(messages[-1]["timestamp"])
    db.insert_multiple(messages)
    print(f"Saved {msg_n} messages from {channel.name} ({channel.msg_counter} total)")
    time.sleep(config.REQUEST_DELAY)

while True:
    for channel in channels:
        if not channel.enabled:
            continue

        update_channel(channel)