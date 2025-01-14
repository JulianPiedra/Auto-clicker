import json
import os

CONFIG_FILE = "resources/config.json"
DEFAULT_CONFIG = {
    "start": "<f1>",
    "stop": "<f2>",
    "mod": ""
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    else:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config_data):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_data, file)
