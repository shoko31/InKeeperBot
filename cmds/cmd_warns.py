# cmd_warns.py

from cmds.cmd import ServerCmd
from user import User
import datetime


async def cmd_player_self_warns_display(server, userid, channel, message):
    if userid not in server.members.keys():
        raise Exception(f'Cannot self display user warns ({userid}) : user id not found in this guild')
    await server.members[userid].display_warnings(channel)
    return True


async def cmd_player_other_warns_display(server, userid, channel, message):
    for mention in message.mentions:
        if mention.id not in server.members.keys():
            raise Exception(f'Cannot display user warns ({mention.id}) : user id not found in this guild')
        await server.members[mention.id].display_warnings(channel)
    return True


async def cmd_player_warns_display(server, userid, channel, message):
    if len(message.mentions) < 1:  # self displays warnings
        return await WarnsSelfCmd.run_cmd(server, userid, channel, message)
    else:
        return await WarnsOtherCmd.run_cmd(server, userid, channel, message)


WarnsSelfCmd = ServerCmd('warnsself', cmd_player_self_warns_display)
WarnsSelfCmd.required_perks = ['cmd.warns', 'cmd.warns.self']

WarnsOtherCmd = ServerCmd('warnsother', cmd_player_other_warns_display)
WarnsOtherCmd.required_perks = ['cmd.warns', 'cmd.warns.other']

WarnsCmd = ServerCmd('warns', cmd_player_warns_display)
WarnsCmd.required_perks = ['cmd.warns', 'cmd.warns.self', 'cmd.warns.other']
