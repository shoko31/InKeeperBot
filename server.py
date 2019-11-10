# server.py

import os
from user import *
from discord.utils import find
import json
from utils import load_json_data, myconverter

from cmds.cmd_accept import AcceptCmd
from cmds.cmd_help import HelpCmd, CommandsCmd
from cmds.cmd_warn import WarnCmd
from cmds.cmd_warns import WarnsCmd
from cmds.cmd_afk import AfkCmd
from cmds.cmd_stop_afk import StopAfkCmd
from cmds.cmd_prefix import PrefixCmd
from cmds.cmd_perm import PermCmd
from cmds.cmd_mute import MuteCmd


class Server:

    def __init__(self, guild):
        self.guild = guild
        self.id = guild.id
        self.name = guild.name
        self.afk_channel_id = guild.afk_channel.id
        self.bot_text_channel_name = os.getenv('SRV_DEFAULT_BOT_TEXT_CHANNEL_NAME')
        self.log_text_channel_name = os.getenv('SRV_DEFAULT_LOGS_TEXT_CHANNEL_NAME')
        self.cmd_prefix = os.getenv('SRV_DEFAULT_CMD_PREFIX_NAME')
        self.admin_logs = bool(os.getenv('SRV_DEFAULT_DISPLAY_ADMIN_LOGS'))
        self.members = {}
        self.group_perks = {}
        for member in guild.members:
            self.members[member.id] = User(member)

    def get_bot_text_channel(self):
        return find(lambda c: c.name == self.bot_text_channel_name, self.guild.text_channels)

    def get_log_text_channel(self):
        return find(lambda c: c.name == self.log_text_channel_name, self.guild.text_channels)

    async def user_voice_moved(self, userid, before, after):
        user = self.members[userid]
        if after.id == self.afk_channel_id:
            await self.print_admin_log(f'{User.get_at_mention(user.id)} ({ user.id }) moved from :sound:**{before.name}** and is now :zzz:**AFK**')
            if user.afk_mentions is True:
                await self.get_bot_text_channel().send(f"{User.get_at_mention(user.id)} est parti boire une p'tite bière :beer: !")
        elif before.id == self.afk_channel_id:
            await self.print_admin_log(f'{User.get_at_mention(user.id)} ({user.id}) moved to :loud_sound:**{after.name}** and is no longer ~~**afk**~~')
            if user.afk_mentions is True:
                await self.get_bot_text_channel().send(f"{User.get_at_mention(user.id)} Alors ? Elle était bonne cette :beer: ?")
        else:
            await self.print_admin_log(f"{User.get_at_mention(user.id)} ({user.id}) moved from :sound:**{before.name}** to :loud_sound:**{after.name}**")

    async def user_voice_connected(self, userid, channel):
        await self.print_admin_log(
            f'{User.get_at_mention(userid)} ({userid}) connected to :loud_sound:**{channel.name}**')
        if userid in self.members.keys() and self.members[userid].muted is True:
            await self.guild.get_member(userid).edit(mute=True)

    async def user_voice_disconnected(self, userid, channel):
        await self.print_admin_log(
            f'{User.get_at_mention(userid)} ({userid}) disconnected from :sound:**{channel.name}**')

    async def print_admin_log(self, msg):
        if self.admin_logs is True:
            log_channel = self.get_log_text_channel()
            current_time = datetime.datetime.now()
            await log_channel.send(f"[{current_time.day}/{current_time.month}/{current_time.year} {current_time.hour}:{current_time.minute}:{current_time.second}] {msg}")

    ### COMMANDS ###
    async def cmd_router(self, msg, userid, channel):
        content = str(msg.content)
        commands = [AcceptCmd,
                    HelpCmd, CommandsCmd,
                    AfkCmd, StopAfkCmd,
                    WarnsCmd, WarnCmd,
                    PrefixCmd,
                    PermCmd,
                    MuteCmd]

        for cmd in commands:
            if content.startswith(self.cmd_prefix + cmd.name):
                if await cmd.run_cmd(self, userid, channel, msg) is True:
                    await self.print_admin_log(
                        f"{User.get_at_mention(userid)} used **{self.cmd_prefix}{cmd.name}** command (||{msg.content}||)")
                else:
                    await self.print_admin_log(
                        f"{User.get_at_mention(userid)} tried to use **{self.cmd_prefix}{cmd.name}** command but failed (||{msg.content}||)")
                break

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
            'group_perks': server.group_perks,
            'members': [json.loads(User.to_json(member)) for key, member in server.members.items()]
        }
        json_to_save = json.dumps(to_save, default=myconverter)
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
            server.group_perks = load_json_data(loaded_server, 'group_perks', {})
            for key, member in server.members.items():
                for json_member in load_json_data(loaded_server, 'members', []):
                    if load_json_data(json_member, 'id', -1) == member.id:
                        User.from_json(json_member, member)
                        break
            return True
        except FileNotFoundError:
            print(f'no save found for {server.id}')
            return False
