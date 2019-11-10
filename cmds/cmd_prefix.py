# cmd_prefix.py

from cmds.cmd import ServerCmd
from user import User


async def cmd_set_prefix(server, userid, channel, message):
    splited_message = str(message.content).split()
    new_prefix = splited_message[1]
    server.cmd_prefix = new_prefix
    await channel.send(f"Le prefix est maintenant `{new_prefix}`.")
    return True


async def cmd_get_prefix(server, userid, channel, message):
    await channel.send(f"Le prefix actuel est `{server.cmd_prefix}`.")
    return True


async def cmd_prefix(server, userid, channel, message):
    splited_message = str(message.content).split()
    if len(splited_message) == 1:  # No argument, display current command prefix
        return await PrefixGetCmd.run_cmd(server, userid, channel, message)
    else:  # Argument found, changing the prefix
        return await PrefixSetCmd.run_cmd(server, userid, channel, message)


PrefixGetCmd = ServerCmd('prefixget', cmd_get_prefix)
PrefixGetCmd.required_perks = ['cmd.prefix', 'cmd.prefix.display']

PrefixSetCmd = ServerCmd('prefixset', cmd_set_prefix)
PrefixSetCmd.required_perks = ['cmd.prefix', 'cmd.prefix.change']

PrefixCmd = ServerCmd('prefix', cmd_prefix)
PrefixCmd.required_perks = ['cmd.prefix', 'cmd.prefix.display', 'cmd.prefix.change']
