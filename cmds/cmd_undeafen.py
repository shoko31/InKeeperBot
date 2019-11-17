# cmd_undeafen.py

import discord
from lang.lang import Lang
from cmds.cmd import ServerCmd
from user import User


async def cmd_undeafen(server, userid, channel, message):
    split_content = str(message.content).split()
    if len(message.mentions) < 1:
        await channel.send(Lang.get('CMD_WRONG_SYNTAX', server.lang))
        await channel.send(f"`{server.cmd_prefix}undeafen <users>`")
        return False
    for mention in message.mentions:
        if mention.id not in server.members.keys():
            raise Exception(f'Cannot find user ({ mention.id }) in server')
            pass
        server.members[mention.id].lock.acquire()
        server.members[mention.id].deaf = False
        server.members[mention.id].deaf_until = None
        if mention.voice is not None:
            await mention.edit(deafen=False)
        await channel.send(
            f"{User.get_at_mention(mention.id)} has been undeafen by {User.get_at_mention(userid)}")
        server.members[mention.id].lock.release()
    return True

UndeafenCmd = ServerCmd('undeafen', cmd_undeafen)
UndeafenCmd.required_perks = ['cmd.undeafen']
