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

api = API(config.TOKEN)
db = TinyDB(config.DATABASE_FILE, storage=CachingMiddleware(JSONStorage))

channels = []

for channel_name, channel_id in config.CHANNELS.items():
    channels.append(
        Channel(channel_name, channel_id, api)
    )

    if db.count(Query()["channel_id"] == str(channels[-1].id)) == 0:
        continue

    last_msg = max(
        db.search(Query()["channel_id"] == str(channels[-1].id)),
        key = lambda x: x["timestamp"]
    )

    channels[-1].last_msg = messages[0]["id"]
    channels[-1].msg_counter = len(messages)

    print(f"Restored channel {channel_name}.")

def sigint_handler(sig, frame):
    print("\nExiting. Please wait...")
    db.close()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

while True:
    channels_n = len(channels)
    
    if channels_n == 0:
        print("Done.")
        db.close()
        sys.exit(0)

    for channel in channels:
        while True:
            try:
                messages = channel.update()
                # print("m")
            except Exception as e:
                print(f"An exception occurred: {e}; retrying...")
                time.sleep(config.FAILED_REQUEST_DELAY)
                continue
            
            break

        messages_n = len(messages)

        if messages_n == 0:
            print(f"No messages left in channel {channel.name}.")
            channels.remove(channel)
            continue

        db.insert_multiple(messages)
        print(f"Saved {messages_n} messages from channel {channel.name}.")

        time.sleep(config.REQUEST_DELAY)