# tft_user.py

import requests
from json import dumps
from .tft_config import USER_ENDPOINT, API_KEY, USER_GAMES_ENDPOINT
from .tft_game import TFTGame

class TFTUser:

    def __init__(self, puuid, name, level, account_id, id, profile_icon_id):
        self.puuid = puuid
        self.name = name
        self.level = level
        self.account_id = account_id
        self.id = id
        self.profile_icon_id = profile_icon_id
        self.games = None

    def __str__(self):
        return 'TFTUser ' + dumps({k: str(v) for k, v in self.__dict__.items()})

    def load_games(self):
        response = requests.get(USER_GAMES_ENDPOINT + '/by-puuid/' + self.puuid + '/ids?api_key=' + API_KEY)
        if response is not None and response.ok is True:
            json_games = response.json()
            games = []
            for game_id in json_games:
                games.append(TFTGame(game_id))
            self.games = games
            return games
        return None

    @staticmethod
    def fetch_by_summoner(summoner_name):
        response = requests.get(USER_ENDPOINT + '/by-name/' + summoner_name + '?api_key=' + API_KEY)
        if response is not None and response.ok is True:
            json_user = response.json()
            return TFTUser(json_user['puuid'], json_user['name'], json_user['summonerLevel'], json_user['accountId'], json_user['id'], json_user['profileIconId'])
        return None
