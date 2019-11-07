# server.py

import os
from user import *
from discord.utils import find
import json
from utils import load_json_data

class Server:

    def __init__(self, guild):
        self.__guild = guild
        self.id = guild.id
        self.name = guild.name
        self.afk_channel_id = guild.afk_channel.id
        self.bot_text_channel_name = os.getenv('SRV_DEFAULT_BOT_TEXT_CHANNEL_NAME')
        self.log_text_channel_name = os.getenv('SRV_DEFAULT_LOGS_TEXT_CHANNEL_NAME')
        self.cmd_prefix = os.getenv('SRV_DEFAULT_CMD_PREFIX_NAME')
        self.admin_logs = bool(os.getenv('SRV_DEFAULT_DISPLAY_ADMIN_LOGS'))
        self.members = {}
        for member in guild.members:
            self.members[member.id] = User(member)

    def get_bot_text_channel(self):
        return find(lambda c: c.name == self.bot_text_channel_name, self.__guild.text_channels)

    def get_log_text_channel(self):
        return find(lambda c: c.name == self.log_text_channel_name, self.__guild.text_channels)

    async def user_voice_moved(self, userid, before, after):
        user = self.members[userid]
        if after.id == self.afk_channel_id:
            await self.print_admin_log(f'{user.get_at_mention()} ({ user.id }) moved from :sound:**{before.name}** and is now :zzz:**AFK**')
            if user.afk_mentions is True:
                await self.get_bot_text_channel().send(f"{user.get_at_mention()} est parti boire une p'tite bière :beer: !")
        elif before.id == self.afk_channel_id:
            await self.print_admin_log(f'{user.get_at_mention()} ({user.id}) moved to :loud_sound:**{after.name}** and is no longer ~~**afk**~~')
            if user.afk_mentions is True:
                await self.get_bot_text_channel().send(f"{user.get_at_mention()} Alors ? Elle était bonne cette :beer: ?")
        else:
            await self.print_admin_log(f"{user.get_at_mention()} ({user.id}) moved from :sound:**{before.name}** to :loud_sound:**{after.name}**")


    async def user_voice_connected(self, userid, channel):
        print(f"{userid} connected to {channel.name}")

    async def user_voice_disconnected(self, userid, channel):
        print(f"{userid} disconnected from {channel.name}")

    async def print_admin_log(self, msg):
        if self.admin_logs is True:
            log_channel = self.get_log_text_channel()
            await log_channel.send(msg)

    ### COMMANDS ###
    async def cmd_router(self, msg, userid, channel):
        if str(msg.content).startswith(self.cmd_prefix + "stopafk"):
            await self.cmd_stop_afk(userid, channel)
        elif str(msg.content).startswith((self.cmd_prefix + 'afk')):
            await self.cmd_afk(userid, channel)
        elif str(msg.content).startswith((self.cmd_prefix + 'prefix')):
            await self.cmd_get_set_prefix(userid, channel, msg)

    async def cmd_stop_afk(self, userid, channel): # stop afk mentions (but keep admin logs)
        user = self.members[userid]
        user.afk_mentions = False
        await channel.send(f"C'est noté { user.get_at_mention() } ! Tu ne seras plus mentionné AFK!")
        await self.print_admin_log(f"{ user.get_at_mention() } used !stopafk command.")

    async def cmd_afk(self, userid, channel): # stop afk mentions (but keep admin logs)
        user = self.members[userid]
        user.afk_mentions = True
        await channel.send(f"C'est noté { user.get_at_mention() } ! Tu seras de nouveau mentionné AFK!")
        await self.print_admin_log(f"{ user.get_at_mention() } used !afk command.")

    async def cmd_get_set_prefix(self, userid, channel, message):
        splitted_message = str(message.content).split()
        if len(splitted_message) == 1: # No argument, display current command prefix
            await channel.send(f"Le prefix actuel est `{ self.cmd_prefix }`.")
        else: # Argument, changing the prefix
            if self.__guild.get_member(userid).guild_permissions.administrator is True:
                self.cmd_prefix = splitted_message[1]
                await channel.send(f"Le prefix est maintenant `{splitted_message[1]}`.")
            else:
                await channel.send(f":octagonal_sign: Désolé { User.get_at_mention(userid) }, mais tu n'as pas les permissions requises pour executer cette commande !")

    ### SAVE AND LOAD ###
    @staticmethod
    def save(server):
        to_save = {
            'id': server.id,
            'name': server.name,
            'bot_text_channel_name': server.bot_text_channel_name,
            'log_text_channel_name': server.log_text_channel_name,
            'cmd_prefix': server.cmd_prefix,
            'admin_logs': server.admin_logs,
            'members': [User.to_json(member) for key, member in server.members.items()]
        }
        json_to_save = json.dumps(to_save)
        with open('./saves/' + str(server.id) + '.save', 'w') as fp:
            fp.write(json_to_save)

    @staticmethod
    def load(server):
        try:
            fp = open('./saves/' + str(server.id) + '.save', 'r')
            file = fp.read()
            fp.close()
            loaded_server = json.loads(file)
            if loaded_server['id'] != server.id:
                raise Exception(f"Can't load server {server.id} : IDs don't match !")
            server.bot_text_channel_name = load_json_data(loaded_server, 'bot_text_channel_name', os.getenv('SRV_DEFAULT_BOT_TEXT_CHANNEL_NAME'))
            server.log_text_channel_name = load_json_data(loaded_server, 'log_text_channel_name', os.getenv('SRV_DEFAULT_LOGS_TEXT_CHANNEL_NAME'))
            server.cmd_prefix = load_json_data(loaded_server, 'cmd_prefix', os.getenv('SRV_DEFAULT_CMD_PREFIX_NAME'))
            server.admin_logs = load_json_data(loaded_server, 'admin_logs', bool(os.getenv('SRV_DEFAULT_DISPLAY_ADMIN_LOGS')))
            for key, member in server.members.items():
                for json_member in load_json_data(loaded_server, 'members', []):
                    loaded_json_member = json.loads(json_member)
                    if load_json_data(loaded_json_member, 'id', -1) == member.id:
                        User.from_json(loaded_json_member, member)
                        break
            return True
        except FileNotFoundError:
            print(f'no save found for {server.id}')
            return False
