# cmd_perm.py

from cmds.cmd import ServerCmd
from user import User
from perks import Perks


async def cmd_set_perm(server, userid, channel, message):
    perks = str(message.content).split()[len(message.role_mentions) + 1:]
    if not Perks.is_valid([perk[1:] if perk.startswith(('+', '-')) else perk for perk in perks]):
        await channel.send("La ou les permissions sont incorrectes")
        return False
    else:
        for role in message.role_mentions:
            remove_perks = [perk[1:] for perk in perks if perk.startswith('-')]
            add_perks = [perk.replace('+', '') for perk in perks if not perk.startswith('-') and perk.replace('+', '') not in remove_perks]
            if str(role.id) in server.group_perks.keys():
                old_perks = [perk for perk in server.group_perks[str(role.id)] if perk not in add_perks and perk not in remove_perks]
                add_perks = old_perks + add_perks
            server.group_perks[str(role.id)] = add_perks
        await channel.send(f"Permissions updated for {' '.join([r.mention for r in message.role_mentions])}")
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
