# cmd_xp.py

import discord
from user import User
from lang.lang import Lang
from cmds.cmd import ServerCmd


async def cmd_user_xp_get(server, userid, channel, message):
    if userid not in server.members.keys():
        raise Exception(f'Cannot self display user xp ({userid}) : user id not found in this guild')
    await channel.send(f"{User.get_at_mention(userid)}'s xp: `{server.members[userid].xp}`")
    return True


async def cmd_xp(server, userid, channel, message):
    return await XpDisplaySelfCmd.run_cmd(server, userid, channel, message)


XpDisplaySelfCmd = ServerCmd('xpself', cmd_user_xp_get)
XpDisplaySelfCmd.required_perks = ['cmd.xp', 'cmd.xp.display', 'cmd.xp.self']

XpCmd = ServerCmd('xp', cmd_xp)
XpCmd.required_perks = ['cmd.xp', 'cmd.xp.give', 'cmd.xp.display', 'cmd.xp.display.other', 'cmd.xp.display.self']
