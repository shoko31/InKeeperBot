# cmd_prefix.py

from cmds.cmd import ServerCmd
from user import User


async def cmd_set_prefix(server, userid, channel, new_prefix):
    if server.guild.get_member(userid).guild_permissions.administrator is True:
        server.cmd_prefix = new_prefix
        await channel.send(f"Le prefix est maintenant `{new_prefix}`.")
    else:
        await channel.send(
            f":octagonal_sign: Désolé {User.get_at_mention(userid)}, mais tu n'as pas les permissions requises pour executer cette commande !")


async def cmd_get_prefix(server, channel):
    await channel.send(f"Le prefix actuel est `{server.cmd_prefix}`.")


async def cmd_prefix(server, userid, channel, message):
    splited_message = str(message.content).split()
    if len(splited_message) == 1:  # No argument, display current command prefix
        await cmd_get_prefix(server, channel)
    else:  # Argument found, changing the prefix
        await cmd_set_prefix(server, userid, channel, splited_message[1])

PrefixCmd = ServerCmd('prefix', cmd_prefix)
