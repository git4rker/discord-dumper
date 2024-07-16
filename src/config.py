from types import SimpleNamespace
import json

class Config(dict):
    @staticmethod
    def load(filename):
        with open(filename, "r") as config_file:
            return json.load(config_file)