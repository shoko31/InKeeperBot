# cmd_warn.py

from cmds.cmd import ServerCmd
from user import User
import datetime


async def cmd_warn_player(server, userid, channel, message):
    splitted_message = str(message.content).split()
    mentions = message.mentions
    if len(mentions) < 1 or len(splitted_message) < len(mentions) + 2:
        await channel.send(f"La syntaxe est incorrecte !")
        await channel.send(f"`{server.cmd_prefix}warn <users> <reason>`")
        return False
    else:
        warn_giver = server.guild.get_member(userid)
        reason = " ".join(splitted_message[1 + len(mentions):])
        currenttime = datetime.datetime.now()
        for mention in mentions:
            if mention.id not in server.members.keys():
                raise Exception(f'Cannot warn user ({mention.id}) : user id not found in this guild')
            server.members[mention.id].warnings.append(
                f"[{currenttime.day}/{currenttime.month}/{currenttime.year} {currenttime.hour}:{currenttime.minute}] {reason} (given by {warn_giver.name}#{warn_giver.discriminator})")
            await channel.send(
                f"{User.get_at_mention(mention.id)} just received a warning (total: {len(server.members[mention.id].warnings)}) from {User.get_at_mention(userid)} : {reason}.")
        return True


WarnCmd = ServerCmd('warn', cmd_warn_player)
WarnCmd.required_perks = ['cmd.warn']
