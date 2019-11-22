# bot.py
import os
import signal
import asyncio
import math
import discord
import threading
from config import cfg
from dotenv import load_dotenv
from server import *
from discord.utils import find
from utils import bot_id
from datetime import datetime, timedelta
from time import sleep

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
textfile_user_mention_tag = cfg.get_value('TEXTFILE_USER_MENTION')
textfile_bot_mention_tag = cfg.get_value('TEXTFILE_BOT_MENTION')
client = discord.Client()
servers = {}
background_loop_thread = None

dm_help_cmd = cfg.get_value('SRV_DEFAULT_CMD_PREFIX_NAME') + 'help'
dm_commands_cmd = cfg.get_value('SRV_DEFAULT_CMD_PREFIX_NAME') + 'commands'
client.activity = discord.Activity(name=dm_help_cmd, details=dm_help_cmd, state=dm_help_cmd, type=discord.ActivityType.listening)

loop = asyncio.get_event_loop()

def check_mute_user(server, member, current_time):
    if member.muted and member.muted_until is not None:
        if member.muted_until <= current_time:
            member.lock.acquire()
            srv_user = server.guild.get_member(member.id)
            member.muted_until = None
            member.muted = False
            if srv_user is not None and srv_user.voice is not None:
                unmute_result = asyncio.run_coroutine_threadsafe(srv_user.edit(mute=False), loop)
                unmute_result.result()
            member.lock.release()

def check_deafen_user(server, member, current_time):
    if member.deaf and member.deaf_until is not None:
        if member.deaf_until <= current_time:
            member.lock.acquire()
            srv_user = server.guild.get_member(member.id)
            member.deaf_until = None
            member.deaf = False
            if srv_user is not None and srv_user.voice is not None:
                unmute_result = asyncio.run_coroutine_threadsafe(srv_user.edit(deafen=False), loop)
                unmute_result.result()
            member.lock.release()

def grant_connected_user_xp(server, member, current_time):
    if member.active_since is not None:
        differ_time = member.last_active_xp
        if member.last_active_xp is None:
            differ_time = member.active_since
        diff_since_last_xp = math.floor((current_time - differ_time).total_seconds() / 3600.0)
        if diff_since_last_xp >= 1:
            member.lock.acquire()
            member.xp = member.xp + (diff_since_last_xp * cfg.get_value('HOUR_ACTIVITY_REWARD_XP'))
            differ_time = differ_time + timedelta(hours=diff_since_last_xp)
            member.last_active_xp = differ_time
            member.lock.release()


def background_server_checks(server):
    current_time = datetime.now()
    for key, member in server.members.items():
        check_mute_user(server, member, current_time)
        check_deafen_user(server, member, current_time)
        grant_connected_user_xp(server, member, current_time)


def background_loop():
    while 1:
        for key, server in servers.items():
            background_server_checks(server)
        sleep(1)


async def send_dm_help(message):
    text = ""
    with open('./lang/en/dm_intro.txt') as fp:
        text += fp.read()
    with open('./lang/en/commands_help.txt') as fp:
        text += fp.read()
    await message.channel.send(
        text.replace(cfg.get_value('TEXTFILE_USER_MENTION'), User.get_at_mention(message.author.id))
            .replace(cfg.get_value('TEXTFILE_BOT_MENTION'), User.get_at_mention(bot_id[0]))
            .replace(cfg.get_value('TEXTFILE_CMD_PREFIX_MENTION'), cfg.get_value('SRV_DEFAULT_CMD_PREFIX_NAME')))


@client.event
async def on_ready():
    bot_id[0] = client.user.id
    for guild in client.guilds:
        print(f'{client.user} has connected to Discord: {guild.name}(id: {guild.id})')
        servers[guild.id] = Server(guild)
        if Server.load(servers[guild.id]) is False:
            Server.save(servers[guild.id])
    # start clock for user checks
    background_loop_thread = threading.Thread(target=background_loop, daemon=True)
    background_loop_thread.start()


@client.event
async def on_message(message):
    if client.user is not message.author: # prevent bot sending message to himself
        if type(message.channel) is discord.DMChannel or type(message.channel) is discord.GroupChannel: # DMs
            if str(message.content).startswith(dm_help_cmd) or str(message.content).startswith(dm_commands_cmd):
                await send_dm_help(message)
        else: # Message on a server
            if message.guild is not None:
                server = servers.get(message.guild.id)
                await server.cmd_router(message, message.author.id, message.channel)

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is None:
        return False

    if before.channel is None:
        after_channel = client.get_channel(after.channel.id)
        server = servers.get(after_channel.guild.id)
        if server is None:
            raise Exception("unknown server")
        user = find(lambda m: m.name == str(member).split('#')[0], client.users)
        await server.user_voice_connected(user.id, after_channel)

    if after.channel is None:
        before_channel = client.get_channel(before.channel.id)
        server = servers.get(before_channel.guild.id)
        if server is None:
            raise Exception("unknown server")
        user = find(lambda m: m.name == str(member).split('#')[0], client.users)
        await server.user_voice_disconnected(user.id, before_channel)

    if before.channel is not None and after.channel is not None and before.channel is not after.channel:
        before_channel = client.get_channel(before.channel.id)
        after_channel = client.get_channel(after.channel.id)
        server = servers.get(before_channel.guild.id)
        if server is None:
            raise Exception("unknown server")
        user = find(lambda m: m.name == str(member).split('#')[0], client.users)
        await server.user_voice_moved(user.id, before_channel, after_channel)

@client.event
async def on_disconnect():
    print('DISCONNECTING')
    for key, server in servers.items():
        Server.save(server)

#client.run(token)


def catch_sigterm(signum, frame):
    loop.run_until_complete(client.logout())
    loop.close()
    print('Exited carefully')


signal.signal(signal.SIGTERM, catch_sigterm)

try:
    loop.run_until_complete(client.login(token))
    loop.run_until_complete(client.connect())
    while True:
        pass
except KeyboardInterrupt:
    loop.run_until_complete(client.logout())
    # cancel all tasks lingering
finally:
    loop.close()
