# cmd_accept.py

import discord
from lang.lang import Lang
from cmds.cmd import ServerCmd


async def cmd_accept(server, userid, channel, message):
    if server.use_accept_command is False:
        return False
    target_role = discord.utils.find(lambda r: r.name == server.accept_rank, server.guild.roles)
    user_roles = message.author.roles
    if target_role not in user_roles:
        await message.author.add_roles(target_role)
        await message.delete()
        return True
    await message.delete()
    return False


async def cmd_toggle_accept(server, userid, channel, message):
    server.use_accept_command = not server.use_accept_command
    accept = ':green_circle: ' + Lang.get('YES', server.lang)
    refuse = ':red_circle: ' + Lang.get('NO', server.lang)
    await channel.send(
        Lang.get('CMD_ACCEPT_TOGGLE', server.lang).format(accept if server.use_accept_command else refuse, server.cmd_prefix))
    return True


async def cmd_accept_group_set(server, userid, channel, message):
    if len(message.role_mentions) < 1:
        await channel.send(f"{Lang.get('CMD_WRONG_SYNTAX', server.lang)}\r\n`{server.cmd_prefix}acceptgroup <group>`")
        return False
    server.accept_rank = message.role_mentions[0].name
    await channel.send(Lang.get('CMD_ACCEPT_GROUP_SET', server.lang).format(message.role_mentions[0].mention, server.cmd_prefix))
    return True


ToggleAcceptCmd = ServerCmd('toggleaccept', cmd_toggle_accept)
ToggleAcceptCmd.required_perks = ['cmd.accept.toggle']

AcceptGroupCmd = ServerCmd('acceptgroup', cmd_accept_group_set)
AcceptGroupCmd.required_perks = ['cmd.accept.set']

AcceptCmd = ServerCmd('accept', cmd_accept)
