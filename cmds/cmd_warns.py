# cmd_warns.py

from cmds.cmd import ServerCmd
from user import User
import datetime


async def cmd_player_warns_display(server, userid, channel, message):
    if len(message.mentions) < 1:  # self displays warnings
        if userid not in server.members.keys():
            raise Exception(f'Cannot self display user warns ({userid}) : user id not found in this guild')
        await server.members[userid].display_warnings(channel)
    else:
        if server.guild.get_member(userid).guild_permissions.administrator is False:
            await channel.send(
                f":octagonal_sign: Désolé {User.get_at_mention(userid)}, mais tu n'as pas les permissions requises pour executer cette commande !")
        else:
            for mention in message.mentions:
                if mention.id not in server.members.keys():
                    raise Exception(f'Cannot display user warns ({mention.id}) : user id not found in this guild')
                await server.members[mention.id].display_warnings(channel)

WarnsCmd = ServerCmd('warns', cmd_player_warns_display)
