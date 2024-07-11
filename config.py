import os
import time

TOKEN = os.environ["token"]
CHANNELS = {
    os.environ["channel_name"]: os.environ["channel_id"],
}
REQUEST_DELAY = os.environ.get("request_delay", 0)
FAILED_REQUEST_DELAY = os.environ.get("failed_request_delay", 0)
DATABASE_FILE = os.environ.get("db_file", "db.json")