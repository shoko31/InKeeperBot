# cmd_mute.py

import discord
from lang.lang import Lang
from datetime import datetime, timedelta
from cmds.cmd import ServerCmd
from user import User


async def cmd_mute(server, userid, channel, message):
    split_content = str(message.content).split()
    if len(message.mentions) < 1:
        await channel.send(f"{Lang.get('CMD_WRONG_SYNTAX', server.lang)}\r\n`{server.cmd_prefix}mute <users> (<time>)`")
        return False
    time = -1
    if len(split_content) > len(message.mentions) + 1:
        time = int(split_content[-1])
    for mention in message.mentions:
        if mention.id not in server.members.keys():
            raise Exception(f'Cannot find user ({ mention.id }) in server')
            pass
        server.members[mention.id].lock.acquire()
        server.members[mention.id].muted = True
        if mention.voice is not None:
            await mention.edit(mute=True)
        if time > 0:
            server.members[mention.id].muted_until = datetime.now() + timedelta(seconds=time)
            await channel.send(Lang.get('CMD_MUTE_TIME', server.lang).format(User.get_at_mention(mention.id), User.get_at_mention(userid), time))
        else:
            server.members[mention.id].muted_until = None
            await channel.send(Lang.get('CMD_MUTE', server.lang).format(User.get_at_mention(mention.id), User.get_at_mention(userid)))
        server.members[mention.id].lock.release()
    return True

MuteCmd = ServerCmd('mute', cmd_mute)
MuteCmd.required_perks = ['cmd.mute']
