# tft_game.py

from json import dumps
from datetime import datetime
from .tft_config import USER_GAMES_ENDPOINT, API_KEY
import requests
from .tft_participant import TFTParticipant


class TFTGame:

    def __init__(self, id):
        self.id = id
        self.loaded = False
        self.participants = None
        self.game_time = None
        self.game_length = -1.0

    def __str__(self):
        return 'TFTGame ' + dumps({k: str(v) for k, v in self.__dict__.items()})

    def get_participant(self, puuid):
        participant = list(filter(lambda p: p.puuid == puuid, self.participants))
        if len(participant) > 0:
            return participant[0]
        return None

    def load(self):
        response = requests.get(USER_GAMES_ENDPOINT + '/' + self.id + '?api_key=' + API_KEY)
        if response is not None and response.ok is True:
            json_game = response.json()
            game_infos = json_game['info']
            self.game_time = datetime.utcfromtimestamp(game_infos['game_datetime'] / 1000.0)
            self.game_length = game_infos['game_length']
            participants = []
            for participant in game_infos['participants']:
                participants.append(TFTParticipant.from_json(participant))
            self.participants = participants
            self.loaded = True
            return True
        return False
