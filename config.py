import os
import time

TOKEN = os.environ["token"]

CHANNELS = {
}

REQUEST_DELAY = 0
FAILED_REQUEST_DELAY = 0

DATABASE_FILE = f"dumps/{time.strftime("%Y%m%d-%H%M%S")}.json"