# cmd_xp.py

import discord
from user import User
from lang.lang import Lang
from cmds.cmd import ServerCmd


async def cmd_user_xp_get_self(server, userid, channel, message):
    if userid not in server.members.keys():
        raise Exception(f'Cannot self display user xp ({userid}) : user id not found in this guild')
    await channel.send(Lang.get('CMD_XP_SELF', server.lang).format(User.get_at_mention(userid), server.members[userid].xp))
    return True


async def cmd_user_xp_get_other(server, userid, channel, message):
    if len(message.mentions) < 1:
        await channel.send(f"{Lang.get('CMD_WRONG_SYNTAX', server.lang)}\r\n`{server.cmd_prefix}xp <users>`")
        return False
    display = ""
    for mention in message.mentions:
        if mention.id in server.members.keys():
            display += f"{Lang.get('CMD_XP_OTHER', server.lang)}\r\n".format(User.get_at_mention(mention.id), server.members[mention.id].xp)
    await channel.send(display)
    return True

async def cmd_user_xp_give(server, userid, channel, message):
    if len(message.mentions) < 1:
        await channel.send(f"{Lang.get('CMD_WRONG_SYNTAX', server.lang)}\r\n`{server.cmd_prefix}xp <users> <value>`")
        return False
    amount_to_give = int(message.content.split()[-1])
    display = ""
    for mention in message.mentions:
        if mention.id in server.members.keys():
            server.members[mention.id].xp += amount_to_give
            display += f"{Lang.get('CMD_XP_GIVE', server.lang)}\r\n".format(User.get_at_mention(mention.id), amount_to_give, User.get_at_mention(userid), server.members[mention.id].xp)
    await channel.send(display)
    return True


async def cmd_xp(server, userid, channel, message):
    split_message = message.content.split()
    if len(split_message) > 1 and len(split_message) - len(message.mentions) == 2:
        return await XpGiveCmd.run_cmd(server, userid, channel, message)
    elif len(split_message) > 1 and len(message.mentions) > 0:
        return await XpDisplayOtherCmd.run_cmd(server, userid, channel, message)
    else:
        return await XpDisplaySelfCmd.run_cmd(server, userid, channel, message)


XpDisplaySelfCmd = ServerCmd('xpself', cmd_user_xp_get_self)
XpDisplaySelfCmd.required_perks = ['cmd.xp', 'cmd.xp.display', 'cmd.xp.self']

XpDisplayOtherCmd = ServerCmd('xpother', cmd_user_xp_get_other)
XpDisplayOtherCmd.required_perks = ['cmd.xp', 'cmd.xp.display', 'cmd.xp.display.other']

XpGiveCmd = ServerCmd('xpgive', cmd_user_xp_give)
XpGiveCmd.required_perks = ['cmd.xp', 'cmd.xp.give']

XpCmd = ServerCmd('xp', cmd_xp)
XpCmd.required_perks = ['cmd.xp', 'cmd.xp.give', 'cmd.xp.display', 'cmd.xp.display.other', 'cmd.xp.display.self']
