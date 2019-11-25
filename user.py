# user.py

import json
from config import cfg
from utils import load_json_data, myconverter
import datetime
import threading

class User:

    def __init__(self, discord_user):
        self.lock = threading.Lock()
        self.__discord_user = discord_user
        self.id = discord_user.id
        self.name = discord_user.name
        self.nick = discord_user.nick
        self.discriminator = discord_user.discriminator
        self.afk_mentions = True
        self.xp = 0
        self.muted = False
        self.muted_until = None
        self.deaf = False
        self.deaf_until = None
        self.active_since = None
        if discord_user.voice is not None and discord_user.voice.afk is False:
            self.active_since = datetime.datetime.now()
        self.last_active_xp = None
        self.last_login = None
        self.last_daily_reward = None
        self.warnings = []

    def get_display_name(self):
        if self.nick != None:
            return self.nick
        return self.name

    async def display_warnings(self, channel):
        if len(self.warnings) == 0:
            await channel.send(f"{User.get_at_mention(self.id)} n'a recu aucun warning :thumbsup: !")
        else:
            await channel.send(f"{User.get_at_mention(self.id)} a recu un total de {len(self.warnings)} warning(s)")
            for warning in self.warnings:
                await channel.send(f"- {warning}")

    def check_daily_reward(self):
        now = datetime.datetime.now()
        if self.last_daily_reward is None or (now - self.last_daily_reward).total_seconds() >= 86400:
            self.last_daily_reward = now
            self.xp += cfg.get_value('DAILY_REWARD_XP')
            return True
        return False

    @staticmethod
    def get_at_mention(userid):
        return '<@' + str(userid) + '>'

    ### SAVE & LOAD ###
    @staticmethod
    def to_json(user):
        save_user = {
            'id': user.id,
            'name': user.name,
            'display_name': user.get_display_name(),
            'discriminator': user.discriminator,
            'afk_mentions': user.afk_mentions,
            'xp': user.xp,
            'last_login': user.last_login,
            'last_daily_reward': user.last_daily_reward,
            'last_active_xp': user.last_active_xp,
            'muted': user.muted,
            'muted_until': user.muted_until,
            'deaf': user.deaf,
            'deaf_until': user.deaf_until,
            'warnings': user.warnings
        }
        return json.dumps(save_user, default=myconverter)

    @staticmethod
    def from_json(json_object, user):
        if json_object['id'] != user.id:
            raise Exception(f"Can't load user {user.id} : IDs don't match !")
        user.afk_mentions = load_json_data(json_object, 'afk_mentions', True)
        user.xp = load_json_data(json_object, 'xp', 0)
        user.last_login = load_json_data(json_object, 'last_login', None)
        user.last_daily_reward = load_json_data(json_object, 'last_daily_reward', None)
        if user.active_since is not None:
            user.last_active_xp = load_json_data(json_object, 'last_active_xp', None)
        user.muted = bool(load_json_data(json_object, 'muted', False))
        user.muted_until = load_json_data(json_object, 'muted_until', None)
        user.deaf = bool(load_json_data(json_object, 'deaf', False))
        user.deaf_until = load_json_data(json_object, 'deaf_until', None)
        if user.last_login is not None:
            user.last_login = datetime.datetime.strptime(user.last_login, '%a %b %d %H:%M:%S %Y')
        if user.last_daily_reward is not None:
            user.last_daily_reward = datetime.datetime.strptime(user.last_daily_reward, '%a %b %d %H:%M:%S %Y')
        if user.last_active_xp is not None:
            user.last_active_xp = datetime.datetime.strptime(user.last_active_xp, '%a %b %d %H:%M:%S %Y')
        if user.muted_until is not None:
            user.muted_until = datetime.datetime.strptime(user.muted_until, '%a %b %d %H:%M:%S %Y')
        if user.deaf_until is not None:
            user.deaf_until = datetime.datetime.strptime(user.deaf_until, '%a %b %d %H:%M:%S %Y')
        user.warnings = load_json_data(json_object, 'warnings', [])
        return user
