import os
import time

TOKEN = os.environ["token"]
CHANNELS = {
}
REQUEST_DELAY = os.environ.get("request_delay", 0)
FAILED_REQUEST_DELAY = os.environ.get("failed_request_delay", 0)
DATABASE_FILE = os.environ.get("db_file", f"dumps/{time.strftime("%Y%m%d-%H%M%S")}.json")