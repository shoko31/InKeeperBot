# cmd_version

import discord
from config import cfg
from cmds.cmd import ServerCmd
from user import User
from utils import bot_id, simple_embed, COLOR


async def cmd_version(server, userid, channel, message):
    text = '{} is running under version `{}`'.format(User.get_at_mention(bot_id[0]), cfg.BOT_VERSION)
    embed = simple_embed(value=text, color=COLOR.LIGHT_BLUE)
    await message.channel.send(embed=embed)
    return True


VersionCmd = ServerCmd('version', cmd_version)
VersionCmd.required_perks = ['cmd.version']
