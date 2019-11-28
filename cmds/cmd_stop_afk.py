# cmd_stop_afk.py

from lang.lang import Lang
from config import cfg
from cmds.cmd import ServerCmd
from user import User

async def cmd_stop_afk(server, userid, channel, message):  # stop afk mentions (but keep admin logs)
    user = server.members[userid]
    user.afk_mentions = False
    await channel.send(Lang.get('CMD_STOPAFK', server.lang).replace(cfg.get_value('TEXTFILE_USER_MENTION'), User.get_at_mention(user.id)))
    return True

StopAfkCmd = ServerCmd('stopafk', cmd_stop_afk)
StopAfkCmd.required_perks = ['cmd.stopafk']
