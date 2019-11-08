# cmd_help

import os
import discord
from cmds.cmd import ServerCmd
from user import User
from utils import bot_id

async def cmd_help(server, userid, channel, message):
    text = ""
    with open('./lang/fr/server_intro.txt') as fp:
        text += fp.read()
    with open('./lang/fr/commands_help.txt') as fp:
        text += fp.read()
    await message.channel.send(
        text.replace(os.getenv('TEXTFILE_USER_MENTION'), User.get_at_mention(message.author.id))
            .replace(os.getenv('TEXTFILE_BOT_MENTION'), User.get_at_mention(bot_id[0]))
            .replace(os.getenv('TEXTFILE_CMD_PREFIX_MENTION'), server.cmd_prefix))

HelpCmd = ServerCmd('help', cmd_help)
CommandsCmd = ServerCmd('commands', cmd_help)
