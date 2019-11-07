# bot.py
import os
import asyncio
import discord
from dotenv import load_dotenv
from server import *
from discord.utils import find

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
textfile_user_mention_tag = os.getenv('TEXTFILE_USER_MENTION')
textfile_bot_mention_tag = os.getenv('TEXTFILE_BOT_MENTION')

client = discord.Client()
servers = {}

client.activity = discord.Activity(name='!!help', details='!!help', state='!!help', type=discord.ActivityType.listening)

def get_help():
    with open('help_cmd_content.txt') as fp:
        text = fp.read()
    return text

@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'{client.user} has connected to Discord: {guild.name}(id: {guild.id})')
        servers[guild.id] = Server(guild)
        if Server.load(servers[guild.id]) is False:
            Server.save(servers[guild.id])


@client.event
async def on_message(message):
    if client.user is not message.author: # prevent bot sending message to himself
        if type(message.channel) is discord.DMChannel or type(message.channel) is discord.GroupChannel: # DMs
            if str(message.content).startswith('!!help') or str(message.content).startswith('!!commands'):
                await message.channel.send(get_help().replace(textfile_user_mention_tag, User.get_at_mention(message.author.id)).replace(textfile_bot_mention_tag, User.get_at_mention(client.user.id)))
        else: # Message on a server
            if message.guild is not None:
                if str(message.content).startswith('!!help') or str(message.content).startswith('!!commands'):
                    await message.channel.send(get_help().replace('#USER', f'<@{message.author.id}>').replace('#BOT', f'<@{client.user.id}>'))
                    pass
                else:
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

    if before.channel is not None and after.channel is not None:
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

loop = asyncio.get_event_loop()
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