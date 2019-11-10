# cmd_perm.py

from cmds.cmd import ServerCmd
from user import User
from perks import Perks


async def cmd_set_perm(server, userid, channel, message):
    perks = str(message.content).split()[len(message.role_mentions) + 1:]
    if not Perks.is_valid(perks):
        await channel.send("La ou les permissions sont incorrectes")
        return False
    else:
        for role in message.role_mentions:
            if str(role.id) in server.group_perks.keys():
                perks = server.group_perks[str(role.id)] + perks
            print(perks)
            server.group_perks[str(role.id)] = perks
        await channel.send(f"Permissions added for {' '.join([r.mention for r in message.role_mentions])}")
        return True


async def cmd_get_perms(server, userid, channel, message):
    for role in message.role_mentions:
        if str(role.id) in server.group_perks.keys():
            perks = server.group_perks[str(role.id)]
            if len(perks) == 0:
                await channel.send(f"{role.mention} ne possède aucune permission.")
            else:
                await channel.send(f"Permission(s) du rôle {role.mention} : {', '.join(perks)}")
        else:
            await channel.send(f"{role.mention} ne possède aucune permission.")
    return True


async def cmd_perm(server, userid, channel, message):
    if len(message.role_mentions) < 1:
        await channel.send(f"La syntaxe est incorrecte !")
        await channel.send(f"`{server.cmd_prefix}perm <roles> <permissions>`")
        return False
    else:
        if len(str(message.content).split()[len(message.role_mentions) + 1:]) < 1:
            return await cmd_get_perms(server, userid, channel, message)
        else:
            return await cmd_set_perm(server, userid, channel, message)

PermCmd = ServerCmd('perm', cmd_perm)
PermCmd.required_perks = ['cmd.perm', 'cmd.perm.display', 'cmd.perm.change']
