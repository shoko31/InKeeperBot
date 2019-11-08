# cmd_afk.py

from cmds.cmd import ServerCmd
from user import User


async def cmd_afk(server, userid, channel, message):  # stop afk mentions (but keep admin logs)
    user = server.members[userid]
    user.afk_mentions = True
    await channel.send(f"C'est noté {User.get_at_mention(user.id)} ! Tu seras de nouveau mentionné AFK!")
    await server.print_admin_log(f"{User.get_at_mention(user.id)} used !afk command.")

AfkCmd = ServerCmd('afk', cmd_afk)
