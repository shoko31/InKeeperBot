# server.py

from user import *
from config import cfg
from lang.lang import Lang
from discord.utils import find
import json
import os
from utils import load_json_data, myconverter
import threading
from db import db

from cmds.cmd_accept import AcceptCmd, ToggleAcceptCmd, AcceptGroupCmd
from cmds.cmd_version import VersionCmd
from cmds.cmd_help import HelpCmd, CommandsCmd
from cmds.cmd_warn import WarnCmd
from cmds.cmd_warns import WarnsCmd
from cmds.cmd_afk import AfkCmd
from cmds.cmd_stop_afk import StopAfkCmd
from cmds.cmd_prefix import PrefixCmd
from cmds.cmd_perm import PermCmd
from cmds.cmd_mute import MuteCmd
from cmds.cmd_unmute import UnmuteCmd
from cmds.cmd_deafen import DeafenCmd
from cmds.cmd_undeafen import UndeafenCmd
from cmds.cmd_lang import LangCmd
from cmds.cmd_xp import XpCmd
from cmds.cmd_tft import TFTCmd
from cmds.cmd_force_save import ForceSaveCmd
from cmds.cmd_daily_reward import DailyRewardCmd, DailyRewardAliasCmd


class Server:

    def __init__(self, guild):
        self.lock = threading.Lock()
        self.guild = guild
        self.id = guild.id
        self.name = guild.name
        self.lang = cfg.get_value('SRV_DEFAULT_LANG')
        self.afk_channel_id = guild.afk_channel.id
        self.bot_text_channel_name = cfg.get_value('SRV_DEFAULT_BOT_TEXT_CHANNEL_NAME')
        self.log_text_channel_name = cfg.get_value('SRV_DEFAULT_LOGS_TEXT_CHANNEL_NAME')
        self.cmd_prefix = cfg.get_value('SRV_DEFAULT_CMD_PREFIX_NAME')
        self.admin_logs = bool(cfg.get_value('SRV_DEFAULT_DISPLAY_ADMIN_LOGS'))
        self.members = {}
        self.group_perks = {}
        self.accept_rank = cfg.get_value('SRV_DEFAULT_ACCEPT_RANK')
        self.use_accept_command = bool(cfg.get_value('SRV_DEFAULT_USE_ACCEPT_COMMAND'))
        for member in guild.members:
            self.members[member.id] = User(member)

    def get_bot_text_channel(self):
        return find(lambda c: c.name == self.bot_text_channel_name, self.guild.text_channels)

    def get_log_text_channel(self):
        return find(lambda c: c.name == self.log_text_channel_name, self.guild.text_channels)

    async def user_voice_moved(self, userid, before, after):
        user = self.members[userid]
        if after.id == self.afk_channel_id:
            user.lock.acquire()
            user.last_active_xp = None
            user.active_since = None
            user.lock.release()
            await self.print_admin_log(f'{User.get_at_mention(user.id)} ({ user.id }) moved from :sound:**{before.name}** and is now :zzz:**AFK**')
            if user.afk_mentions is True:
                await self.get_bot_text_channel().send(Lang.get('USER_IS_AFK', self.lang).replace(cfg.get_value('TEXTFILE_USER_MENTION'), User.get_at_mention(user.id)))
        elif before.id == self.afk_channel_id:
            user.lock.acquire()
            user.last_active_xp = None
            user.active_since = datetime.datetime.now()
            user.lock.release()
            await self.print_admin_log(f'{User.get_at_mention(user.id)} ({user.id}) moved to :loud_sound:**{after.name}** and is no longer ~~**afk**~~')
            if user.afk_mentions is True:
                await self.get_bot_text_channel().send(Lang.get('USER_NO_MORE_AFK', self.lang).replace(cfg.get_value('TEXTFILE_USER_MENTION'), User.get_at_mention(user.id)))
        else:
            await self.print_admin_log(f"{User.get_at_mention(user.id)} ({user.id}) moved from :sound:**{before.name}** to :loud_sound:**{after.name}**")

    async def user_voice_connected(self, userid, channel):
        await self.print_admin_log(
            f'{User.get_at_mention(userid)} ({userid}) connected to :loud_sound:**{channel.name}**')
        if userid in self.members.keys():
            member = self.members[userid]
            member.lock.acquire()
            member.last_login = datetime.datetime.now()
            member.active_since = datetime.datetime.now()
            member.last_active_xp = None
            if member.check_daily_reward() is True:
                await self.get_bot_text_channel().send(Lang.get('DAILY_XP_REWARD_LOGIN', self.lang).replace(cfg.get_value('TEXTFILE_USER_MENTION'), User.get_at_mention(userid)).format(cfg.get_value('DAILY_REWARD_XP')))
            member.lock.release()
            if self.members[userid].muted is True:
                await self.guild.get_member(userid).edit(mute=True)
            else:
                await self.guild.get_member(userid).edit(mute=False)
            if self.members[userid].deaf is True:
                await self.guild.get_member(userid).edit(deafen=True)
            else:
                await self.guild.get_member(userid).edit(deafen=False)

    async def user_voice_disconnected(self, userid, channel):
        if userid in self.members.keys():
            user = self.members[userid]
            user.lock.acquire()
            user.active_since = None
            user.last_active_xp = None
            user.lock.release()
        await self.print_admin_log(
            f'{User.get_at_mention(userid)} ({userid}) disconnected from :sound:**{channel.name}**')

    async def user_voice_state_updated(self, userid, channel):
        if channel.id is not self.afk_channel_id and userid in self.members.keys():
            member = self.members[userid]
            guild_member = self.guild.get_member(userid)
            voice_state = guild_member.voice
            if voice_state.mute is False and member.muted is True:
                await self.guild.get_member(userid).edit(mute=True)
            if voice_state.deaf is False and member.deaf is True:
                await self.guild.get_member(userid).edit(deafen=True)

    async def print_admin_log(self, msg):
        if self.admin_logs is True:
            log_channel = self.get_log_text_channel()
            current_time = datetime.datetime.now()
            await log_channel.send(f"[{current_time.day}/{current_time.month}/{current_time.year} {current_time.hour}:{current_time.minute}:{current_time.second}] {msg}")

    ### COMMANDS ###
    async def cmd_router(self, msg, userid, channel):
        content = str(msg.content)
        commands = [ToggleAcceptCmd, AcceptGroupCmd, AcceptCmd,
                    VersionCmd,
                    HelpCmd, CommandsCmd,
                    AfkCmd, StopAfkCmd,
                    WarnsCmd, WarnCmd,
                    PrefixCmd,
                    PermCmd,
                    MuteCmd, UnmuteCmd,
                    DeafenCmd, UndeafenCmd,
                    LangCmd,
                    XpCmd,
                    TFTCmd,
                    ForceSaveCmd,
                    DailyRewardCmd, DailyRewardAliasCmd]

        found_valid_command = False
        for cmd in commands:
            if content == self.cmd_prefix + cmd.name or content.startswith(self.cmd_prefix + cmd.name + ' '):
                found_valid_command = True
                if await cmd.run_cmd(self, userid, channel, msg) is True:
                    await self.print_admin_log(
                        f"{User.get_at_mention(userid)} used **{self.cmd_prefix}{cmd.name}** command (||{msg.content}||)")
                else:
                    await self.print_admin_log(
                        f"{User.get_at_mention(userid)} tried to use **{self.cmd_prefix}{cmd.name}** command but failed (||{msg.content}||)")
                break
        if not found_valid_command and content.startswith(self.cmd_prefix):
            await channel.send(Lang.get('UNKNOWN_CMD', self.lang).format(content, self.cmd_prefix))

    ### SAVE AND LOAD ###
    @staticmethod
    def save(server):
        to_save = {
            'id': server.id,
            'name': server.name,
            'lang': server.lang,
            'bot_text_channel_name': server.bot_text_channel_name,
            'log_text_channel_name': server.log_text_channel_name,
            'cmd_prefix': server.cmd_prefix,
            'admin_logs': server.admin_logs,
            'group_perks': server.group_perks,
            'use_accept': server.use_accept_command,
            'accept_rank': server.accept_rank,
            'members': [json.loads(User.to_json(member)) for key, member in server.members.items()]
        }
        json_to_save = json.dumps(to_save, default=myconverter)
        db.update_server(server.id, json_to_save)

    @staticmethod
    def load(server):
        loaded_server = db.get_server(server.id)
        if loaded_server is None:
            print(f'no save found for {server.id}')
            return False
        if loaded_server['id'] != server.id:
            raise Exception(f"Can't load server {server.id} : IDs don't match !")
        server.lang = load_json_data(loaded_server, 'lang', cfg.get_value('SRV_DEFAULT_LANG'))
        server.bot_text_channel_name = load_json_data(loaded_server, 'bot_text_channel_name', cfg.get_value('SRV_DEFAULT_BOT_TEXT_CHANNEL_NAME'))
        server.log_text_channel_name = load_json_data(loaded_server, 'log_text_channel_name', cfg.get_value('SRV_DEFAULT_LOGS_TEXT_CHANNEL_NAME'))
        server.cmd_prefix = load_json_data(loaded_server, 'cmd_prefix', cfg.get_value('SRV_DEFAULT_CMD_PREFIX_NAME'))
        server.admin_logs = load_json_data(loaded_server, 'admin_logs', bool(cfg.get_value('SRV_DEFAULT_DISPLAY_ADMIN_LOGS')))
        server.group_perks = load_json_data(loaded_server, 'group_perks', {})
        server.use_accept_command = load_json_data(loaded_server, 'use_accept', bool(cfg.get_value('SRV_DEFAULT_USE_ACCEPT_COMMAND')))
        server.use_accept_command = load_json_data(loaded_server, 'accept_rank', cfg.get_value('SRV_DEFAULT_ACCEPT_RANK'))
        for key, member in server.members.items():
            for json_member in load_json_data(loaded_server, 'members', []):
                if load_json_data(json_member, 'id', -1) == member.id:
                    User.from_json(json_member, member)
                    break
        return True
