# cmd_stop_afk.py

from cmds.cmd import ServerCmd
from user import User


async def cmd_stop_afk(server, userid, channel, message):  # stop afk mentions (but keep admin logs)
    user = server.members[userid]
    user.afk_mentions = False
    await channel.send(f"C'est noté {User.get_at_mention(user.id)} ! Tu ne seras plus mentionné AFK!")
    await server.print_admin_log(f"{User.get_at_mention(user.id)} used !stopafk command.")

StopAfkCmd = ServerCmd('stopafk', cmd_stop_afk)
