# cmd_accept.py

import discord
from cmds.cmd import ServerCmd


async def cmd_accept(server, userid, channel, message):
    target_role = discord.utils.find(lambda r: r.name == "Member", server.guild.roles)
    user_roles = message.author.roles
    if target_role not in user_roles:
        await message.author.add_roles(target_role)
        await message.delete()
        return True
    await message.delete()
    return False


AcceptCmd = ServerCmd('accept', cmd_accept)
