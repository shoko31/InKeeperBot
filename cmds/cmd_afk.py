# cmd_afk.py

from lang.lang import Lang
from config import cfg
from cmds.cmd import ServerCmd
from user import User


async def cmd_afk(server, userid, channel, message):  # stop afk mentions (but keep admin logs)
    user = server.members[userid]
    user.afk_mentions = True
    await channel.send(Lang.get('CMD_AFK', server.lang).replace(cfg.get_value('TEXTFILE_USER_MENTION'), User.get_at_mention(user.id)))
    return True

AfkCmd = ServerCmd('afk', cmd_afk)
AfkCmd.required_perks = ['cmd.afk']
