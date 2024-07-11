import os
import time

TOKEN = os.environ["token"]
CHANNELS = {
    "rules-and-roles": 357673249309589516,
    "announcements": 860960627060899880,
    "welcome": 402181205451210753,
    "powdertoy": 311697121914912768,
    "save-ids": 311697677136035850,
    "help": 311697706764730369,
    "suggestions": 444971814863634453,
    "tptmp": 329325204306395136,
    "tpt-mods": 555623815485456384,
    "development": 939734727265488896,
    "chat": 373908559945269248,
    "images": 423263161337249806,
    "minecraft": 474022450535858197,
    "other-games": 968668443366789140,
    "bermudatrianglebrush": 399990509290127389,
    "bot-commands": 349770616007557122,
    "vc-general": 311697121914912769,
    "voice-text-chat": 680986162227314719
}
REQUEST_DELAY = os.environ.get("request_delay", 0)
FAILED_REQUEST_DELAY = os.environ.get("failed_request_delay", 0)
DATABASE_FILE = os.environ.get("db_file", f"dumps/{time.strftime("%Y%m%d-%H%M%S")}.json")