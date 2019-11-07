# user.py

import json
from utils import load_json_data


class User:

    def __init__(self, discord_user):
        self.__discord_user = discord_user
        self.id = discord_user.id
        self.name = discord_user.name
        self.nick = discord_user.nick
        self.discriminator = discord_user.discriminator
        self.afk_mentions = True
        self.xp = 0

    def get_display_name(self):
        if self.nick != None:
            return self.nick
        return self.name

    def get_at_mention(self):
        return User.get_at_mention(self.id)

    @staticmethod
    def get_at_mention(userid):
        return '<@' + str(userid) + '>'

    ### SAVE & LOAD ###
    @staticmethod
    def to_json(user):
        save_user = {
            'id': user.id,
            'afk_mentions': user.afk_mentions,
            'xp': user.xp
        }
        return json.dumps(save_user)

    @staticmethod
    def from_json(json_object, user):
        if json_object['id'] != user.id:
            raise Exception(f"Can't load user {user.id} : IDs don't match !")
        user.afk_mentions = load_json_data(json_object, 'afk_mentions', True)
        user.xp = load_json_data(json_object, 'xp', 0)
        return user
