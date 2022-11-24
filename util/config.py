import json
from pathlib import Path
import os
config_file = os.path.join(os.path.split(__file__)[0], Path(
    __file__).resolve().parents[1], 'config', 'config.json')
f = open(config_file, encoding='utf-8')
config = json.load(f)



def get_client(name):

    for client in config['clients']:
        if client['name'] == name:
            return client

    return None


def get_credential(key):
    return config["credentials"][key]
