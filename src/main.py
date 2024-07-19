from channel import Channel
from discordapi import API
from pymongo import MongoClient
from config import Config
import signal
import sys
import time

config = Config.load(sys.argv[1] if len(sys.argv) > 1 else "config.json")
api = API(config["token"])
db_client = MongoClient(config["mongo"]["uri"])
db = db_client[config["mongo"]["db"]]

def safe_exit():
    print("Exiting safely. Please wait...")
    db_client.close()
    sys.exit(0)

def signal_handler(sig, frame):
    safe_exit()

signal.signal(signal.SIGINT, signal_handler)

for channel_id in config["channels"]:
    channel = Channel(channel_id, api)
    persistence = db.persistence.find_one(
        { "id": channel.id }
    )

    if persistence != None:
        channel.restore(persistence)
        channel.n_msg = db.messages.count_documents({"channel_id": str(channel.id)})
        print(f"Restored channel {channel.object["name"]} from database")
    
    while True:
        try:
            n_msg, messages = channel.get_messages()
        except Exception as e:
            print(f"An exception occured: {e}. Retrying...")
            continue

        print(f"{channel.object["name"]}: {n_msg} messages dumped; {channel.n_msg} total")

        if n_msg == 0:
            break

        db.messages.insert_many(messages)
        db.persistence.update_one(
            { "id": channel.id },
            {"$set": {
                "last_message_id": channel.last_message_id
            }},
            True
        )