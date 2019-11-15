# cmd_version

import discord
from config import cfg
from cmds.cmd import ServerCmd
from user import User
from utils import bot_id


async def cmd_version(server, userid, channel, message):
    text = '{} is running under version `{}`'
    await message.channel.send(
        text.format(User.get_at_mention(bot_id[0]), cfg.BOT_VERSION))
    return True


VersionCmd = ServerCmd('version', cmd_version)
VersionCmd.required_perks = ['cmd.version']
