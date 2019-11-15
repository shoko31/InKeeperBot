# cmd_help

import discord
from config import cfg
from cmds.cmd import ServerCmd
from user import User
from utils import bot_id

async def cmd_help(server, userid, channel, message):
    text = ""
    with open(f'./lang/{server.lang}/server_intro.txt') as fp:
        text += fp.read()
    with open(f'./lang/{server.lang}/commands_help.txt') as fp:
        text += fp.read()
    await message.channel.send(
        text.replace(cfg.get_value('TEXTFILE_USER_MENTION'), User.get_at_mention(message.author.id))
            .replace(cfg.get_value('TEXTFILE_BOT_MENTION'), User.get_at_mention(bot_id[0]))
            .replace(cfg.get_value('TEXTFILE_CMD_PREFIX_MENTION'), server.cmd_prefix))
    return True

HelpCmd = ServerCmd('help', cmd_help)
HelpCmd.required_perks = ['cmd.help']
CommandsCmd = ServerCmd('commands', cmd_help)
CommandsCmd.required_perks = ['cmd.commands']
