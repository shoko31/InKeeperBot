# DiscordClient.py

import discord
from config import cfg
from dotenv import load_dotenv
from server import *
from discord.utils import find
from utils import bot_id


class DiscordClient(discord.Client):

    def __init__(self):
        load_dotenv()
        self.servers = {}
        self.textfile_user_mention_tag = cfg.get_value('TEXTFILE_USER_MENTION')
        self.textfile_bot_mention_tag = cfg.get_value('TEXTFILE_BOT_MENTION')
        self.dm_help_cmd = cfg.get_value('SRV_DEFAULT_CMD_PREFIX_NAME') + 'help'
        self.dm_commands_cmd = cfg.get_value('SRV_DEFAULT_CMD_PREFIX_NAME') + 'commands'
        super(DiscordClient, self).__init__()
        self.activity = discord.Activity(name=self.dm_help_cmd, details=self.dm_help_cmd, state=self.dm_help_cmd,
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

    async def on_ready(self):
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
            else:  # Message on a server
                if message.guild is not None:
                    server = self.servers.get(message.guild.id)
                    if server is not None:
                        await server.cmd_router(message, message.author.id, message.channel)

    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is None:
            return False

        if before.channel is None:
            after_channel = self.get_channel(after.channel.id)
            server = self.servers.get(after_channel.guild.id)
            if server is None:
                raise Exception("unknown server")
            user = find(lambda m: m.name == str(member).split('#')[0], self.users)
            await server.user_voice_connected(user.id, after_channel)

        elif after.channel is None:
            before_channel = self.get_channel(before.channel.id)
            server = self.servers.get(before_channel.guild.id)
            if server is None:
                raise Exception("unknown server")
            user = find(lambda m: m.name == str(member).split('#')[0], self.users)
            await server.user_voice_disconnected(user.id, before_channel)

        elif before.channel is not None and after.channel is not None and before.channel is not after.channel:
            before_channel = self.get_channel(before.channel.id)
            after_channel = self.get_channel(after.channel.id)
            server = self.servers.get(before_channel.guild.id)
            if server is None:
                raise Exception("unknown server")
            user = find(lambda m: m.name == str(member).split('#')[0], self.users)
            await server.user_voice_moved(user.id, before_channel, after_channel)

        elif before.channel is not None and after.channel is not None and before.channel is after.channel:
            before_channel = self.get_channel(before.channel.id)
            server = self.servers.get(before_channel.guild.id)
            if server is None:
                raise Exception("unknown server")
            user = find(lambda m: m.name == str(member).split('#')[0], self.users)
            await server.user_voice_state_updated(user.id, before_channel)

    async def on_member_join(self, member):
        print(f'Member joined: {member}')

    async def on_member_remove(self, member):
        print(f'Member left: {member}')

    async def on_guild_join(self, guild):
        print(f'JOINED {guild.name}')

    async def on_guild_remove(self, guild):
        print(f'LEFT {guild.name}')

    async def on_guild_update(self, before, after):
        guild = self.servers.get(after.id)
        if guild is None:
            raise Exception(f"Could'nt find guild on guild update ({after.id})")
        else:
            guild.guild = after
            # Check afk channel change
            if after.afk_channel.id != guild.afk_channel_id:
                guild.afk_channel_id = after.afk_channel.id
            # Check name change
            if guild.name != after.name:
                guild.name = after.name

    async def on_disconnect(self):
        print('DISCONNECTING')
        for key, server in self.servers.items():
            Server.save(server)
