from channel import Channel
from discordapi import API
from montydb import MontyClient, set_storage
from config import Config
import signal
import sys
import time

config = Config.load(sys.argv[1] if len(sys.argv) > 1 else "config.json")
api = API(config["token"])

set_storage(
    repository=config["storage"]["path"],
    storage="sqlite", # it looks like flat-file loads the entire DB into memory for operation :skull:
    journal_mode="WAL",
    check_same_thread=False
)
db_client = MontyClient(config["storage"]["path"])
db = db_client[config["storage"]["db_name"]]

def safe_exit():
    print("Exiting safely. Please wait...")
    db_client.close()
    sys.exit(0)

def signal_handler(sig, frame):
    safe_exit()

signal.signal(signal.SIGINT, signal_handler)

for channel_id in config["channels"]:
    channel = Channel(channel_id, api)
    channel_pers = db.channels.find_one(
        {"id": channel.id}
    )
    n_msg_total = 0

    if channel_pers != None:
        channel.last_message_id = channel_pers["last_message_id"]
        n_msg_total = channel_pers["n_msg_total"]

    print(f"Restored channel {channel.object["name"]} from database")

    while True:
        try:
            messages = channel.get_messages()
        except Exception as e:
            print(f"An exception occured: {e}. Retrying...")
            continue

        n_msg = len(messages)

        if n_msg == 0:
            break

        n_msg_total += n_msg

        print(f"{channel.object["name"]}: {n_msg} messages dumped; {n_msg_total} total")

        db.messages.insert_many(messages)
        db.channels.update_one(
            {"id": channel.id},
            {"$set": {
                "last_message_id": channel.last_message_id,
                "n_msg_total": n_msg_total
            }},
            True
        )