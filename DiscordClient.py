# DiscordClient.py

import discord
from config import cfg
from dotenv import load_dotenv
from server import *
from discord.utils import find
from utils import bot_id


class DiscordClient(discord.Client):

    def __init__(self, shard_id=None, shard_count=None):
        load_dotenv()
        self.servers = {}
        self.textfile_user_mention_tag = cfg.get_value('TEXTFILE_USER_MENTION')
        self.textfile_bot_mention_tag = cfg.get_value('TEXTFILE_BOT_MENTION')
        self.dm_help_cmd = cfg.get_value('SRV_DEFAULT_CMD_PREFIX_NAME') + 'help'
        self.dm_commands_cmd = cfg.get_value('SRV_DEFAULT_CMD_PREFIX_NAME') + 'commands'
        self.dm_invite_cmd = cfg.get_value('SRV_DEFAULT_CMD_PREFIX_NAME') + 'invite'
        super(DiscordClient, self).__init__(shard_id=shard_id, shard_count=shard_count)
        activity = self.dm_help_cmd + ' and ' + self.dm_invite_cmd
        self.activity = discord.Activity(name=activity, details=activity, state=activity,
                                         type=discord.ActivityType.listening)

    async def send_dm_help(self, message):
        text = ""
        with open('./lang/en/dm_intro.txt') as fp:
            text += fp.read()
        with open('./lang/en/commands_help.txt') as fp:
            text += fp.read()
        await message.channel.send(
            text.replace(cfg.get_value('TEXTFILE_USER_MENTION'), User.get_at_mention(message.author.id))
                .replace(cfg.get_value('TEXTFILE_BOT_MENTION'), User.get_at_mention(bot_id[0]))
                .replace(cfg.get_value('TEXTFILE_CMD_PREFIX_MENTION'), cfg.get_value('SRV_DEFAULT_CMD_PREFIX_NAME')))

    async def send_dm_invite(self, message):
        text = ""
        with open('./lang/en/dm_invite.txt') as fp:
            text += fp.read()
        await message.channel.send(
            text.replace(cfg.get_value('TEXTFILE_USER_MENTION'), User.get_at_mention(message.author.id))
                .replace(cfg.get_value('TEXTFILE_BOT_MENTION'), User.get_at_mention(bot_id[0]))
                .replace(cfg.get_value('TEXTFILE_CMD_PREFIX_MENTION'), cfg.get_value('SRV_DEFAULT_CMD_PREFIX_NAME'))
                .replace(cfg.get_value('TEXTFILE_INVITE_URL'), cfg.get_value('INVITE_URL')))

    async def on_ready(self):
        print(f'Client is ready (shard id: {self.shard_id})')
        bot_id[0] = self.user.id
        for guild in self.guilds:
            print(f'{self.user} has connected to Discord: {guild.name}(id: {guild.id})')
            self.servers[guild.id] = Server(guild)
            if Server.load(self.servers[guild.id]) is False:
                Server.save(self.servers[guild.id])

    async def on_message(self, message):
        if self.user is not message.author:  # prevent bot sending message to himself
            if type(message.channel) is discord.DMChannel or type(message.channel) is discord.GroupChannel:  # DMs
                if str(message.content).startswith(self.dm_help_cmd) or str(message.content).startswith(self.dm_commands_cmd):
                    await self.send_dm_help(message)
                elif str(message.content).startswith(self.dm_invite_cmd):
                    await self.send_dm_invite(message)
            else:  # Message on a server
                if message.guild is not None:
                    server = self.servers.get(message.guild.id)
                    if server is not None:
                        await server.cmd_router(message, message.author.id, message.channel)

    async def on_raw_reaction_add(self, payload):
        if payload.guild_id is None or payload.channel_id is None or payload.user_id is None or payload.message_id is None:
            return
        if payload.user_id == self.user.id:  # Filter auto-reaction or bot reaction
            return
        server = self.servers.get(payload.guild_id)
        if server is None:
            raise Exception('server not found (add raw reaction)')
        channel = server.guild.get_channel(payload.channel_id)
        if channel is None:
            raise Exception('channel not found (add raw reaction)')
        message = await channel.fetch_message(payload.message_id)
        if message is None:
            raise Exception('message not found (add raw reaction)')
        if message.author.id != self.user.id:  # filter on bot's message reaction
            return
        await server.bot_message_get_reaction(message, payload.emoji, payload.user_id)

    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is None:
            return False

        if before.channel is None:
            after_channel = self.get_channel(after.channel.id)
            server = self.servers.get(after_channel.guild.id)
            if server is None:
                raise Exception("unknown server (voice state update)")
            user = find(lambda m: m.name == str(member).split('#')[0], self.users)
            await server.user_voice_connected(user.id, after_channel)

        elif after.channel is None:
            before_channel = self.get_channel(before.channel.id)
            server = self.servers.get(before_channel.guild.id)
            if server is None:
                raise Exception("unknown server (voice state update)")
            user = find(lambda m: m.name == str(member).split('#')[0], self.users)
            await server.user_voice_disconnected(user.id, before_channel)

        elif before.channel is not None and after.channel is not None and before.channel is not after.channel:
            before_channel = self.get_channel(before.channel.id)
            after_channel = self.get_channel(after.channel.id)
            server = self.servers.get(before_channel.guild.id)
            if server is None:
                raise Exception("unknown server (voice state update)")
            user = find(lambda m: m.name == str(member).split('#')[0], self.users)
            await server.user_voice_moved(user.id, before_channel, after_channel)

        elif before.channel is not None and after.channel is not None and before.channel is after.channel:
            before_channel = self.get_channel(before.channel.id)
            server = self.servers.get(before_channel.guild.id)
            if server is None:
                raise Exception("unknown server (voice state update)")
            user = find(lambda m: m.name == str(member).split('#')[0], self.users)
            await server.user_voice_state_updated(user.id, before_channel)

    async def on_member_join(self, member):
        if member is not None and member.guild is not None:
            server = self.servers.get(member.guild.id)
            if server is None:
                raise Exception("unknown server (member joined)")
            await server.user_joined(member.id)

    async def on_member_remove(self, member):
        if member is not None and member.guild is not None:
            server = self.servers.get(member.guild.id)
            if server is None:
                raise Exception("unknown server (member left)")
            await server.user_left(member.id)

    async def on_guild_join(self, guild):
        print(f'{self.user} has joined a new Discord: {guild.name}(id: {guild.id})')
        self.servers[guild.id] = Server(guild)
        if Server.load(self.servers[guild.id]) is False:
            Server.save(self.servers[guild.id])

    async def on_guild_remove(self, guild):
        print(f'{self.user} has left a Discord: {guild.name}(id: {guild.id})')
        server = self.servers.get(guild.id)
        if server is None:
            raise Exception(f"Could'nt find guild on guild update ({guild.id})")
        else:
            Server.save(server)
            del self.servers[guild.id]

    async def on_guild_update(self, before, after):
        guild = self.servers.get(after.id)
        if guild is None:
            raise Exception(f"Could'nt find guild on guild update ({after.id})")
        else:
            guild.guild = after
            # Check afk channel change
            if after.afk_channel is None:
                guild.afk_channel_id = -1
            elif after.afk_channel.id != guild.afk_channel_id:
                guild.afk_channel_id = after.afk_channel.id
            # Check name change
            if guild.name != after.name:
                guild.name = after.name

    async def on_disconnect(self):
        print('DISCONNECTING')
        for key, server in self.servers.items():
            Server.save(server)
