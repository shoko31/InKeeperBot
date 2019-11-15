# config.py

import json
from utils import load_json_data


class Config:
    CONFIG_FILE = 'bot.config'
    BOT_VERSION = '0.0.4'

    def __init__(self):
        self.values = {}
        self.__load()

    def get_value(self, value):
        return self.values[value]

    def __load(self):
        with open(self.CONFIG_FILE, 'r') as fp:
            lines = fp.read()
        try:
            values = json.loads(lines)
            self.values = values
        except json.JSONDecodeError:
            print('Unable to load the config file')


cfg = Config()
