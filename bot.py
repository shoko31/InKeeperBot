# bot.py
import os
import signal
import asyncio
import math
import threading
from config import cfg
from dotenv import load_dotenv
from datetime import datetime, timedelta
from time import sleep
from DiscordClient import DiscordClient
from lang.lang import Lang
from user import User

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
background_loop_thread = None
loop = asyncio.get_event_loop()
bot_loop = None
bot_client = None


def check_mute_user(server, member, current_time):
    global bot_loop
    if member.muted and member.muted_until is not None:
        if member.muted_until <= current_time:
            member.lock.acquire()
            srv_user = server.guild.get_member(member.id)
            member.muted_until = None
            member.muted = False
            if srv_user is not None and srv_user.voice is not None:
                unmute_result = asyncio.run_coroutine_threadsafe(srv_user.edit(mute=False), bot_loop)
                unmute_result.result()
            member.lock.release()


def check_deafen_user(server, member, current_time):
    global bot_loop
    if member.deaf and member.deaf_until is not None:
        if member.deaf_until <= current_time:
            member.lock.acquire()
            srv_user = server.guild.get_member(member.id)
            member.deaf_until = None
            member.deaf = False
            if srv_user is not None and srv_user.voice is not None:
                unmute_result = asyncio.run_coroutine_threadsafe(srv_user.edit(deafen=False), bot_loop)
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


def grant_connected_user_daily_reward(server, member):
    global bot_loop
    member.lock.acquire()
    if member.active_since is not None and member.check_daily_reward() is True:
        asyncio.run_coroutine_threadsafe(server.print_bot_message(Lang.get('DAILY_XP_REWARD_ACTIVE', server.lang).replace(cfg.get_value('TEXTFILE_USER_MENTION'), User.get_at_mention(member.id)).format(cfg.get_value('DAILY_REWARD_XP'))), bot_loop)
    member.lock.release()


def background_server_checks(server):
    current_time = datetime.now()
    for key, member in server.members.items():
        check_mute_user(server, member, current_time)
        check_deafen_user(server, member, current_time)
        grant_connected_user_xp(server, member, current_time)
        grant_connected_user_daily_reward(server, member)


def background_loop():
    while 1:
        if bot_client is not None and bot_client.is_ready():
            for key, server in bot_client.servers.items():
                background_server_checks(server)
        sleep(1)


def catch_sigterm(signum, frame):
    global bot_loop, bot_client, loop
    print('logout')
    future = asyncio.run_coroutine_threadsafe(bot_client.logout(), bot_loop)
    try:
        result = future.result(20)
    except asyncio.TimeoutError:
        print('The coroutine took too long, cancelling the task...')
        future.cancel()
    except Exception as exc:
        print(f'The coroutine raised an exception: {exc!r}')
    else:
        print(f'The coroutine returned: {result!r}')

    bot_loop.call_soon_threadsafe(bot_loop.stop)
    loop.call_soon_threadsafe(loop.stop)


def bot_launch():
    global bot_loop, bot_client
    bot_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(bot_loop)
    bot_client = DiscordClient()
    print('Client login')
    bot_loop.run_until_complete(bot_client.login(token))
    print('Client connect')
    bot_loop.run_until_complete(bot_client.connect())
    bot_loop.run_forever()


if __name__ == '__main__':

    print("starting in 30seconds...")
    sleep(30)
    print("starting now")

    signal.signal(signal.SIGTERM, catch_sigterm)

    bot_thread = threading.Thread(target=bot_launch, daemon=True)
    bot_thread.start()

    background_loop_thread = threading.Thread(target=background_loop, daemon=True)
    background_loop_thread.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        catch_sigterm(None, None)

    print("End of the program. I was killed gracefully :)")
