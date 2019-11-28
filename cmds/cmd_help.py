# cmd_help

import discord
from config import cfg
from cmds.cmd import ServerCmd
from user import User
from utils import bot_id, COLOR, simple_embed

HELP_HOME_EMOJI = '\u2754'
HELP_GAMES_EMOJI = '\N{VIDEO GAME}'
HELP_LANGUAGE_EMOJI = '\N{GLOBE WITH MERIDIANS}'
HELP_COMMANDS_EMOJI = '\u2755'


def replace_textfile_text_variables(server, message, msg):
    return msg.replace(cfg.get_value('TEXTFILE_USER_MENTION'), User.get_at_mention(message.author.id))\
        .replace(cfg.get_value('TEXTFILE_BOT_MENTION'), User.get_at_mention(bot_id[0]))\
        .replace(cfg.get_value('TEXTFILE_CMD_PREFIX_MENTION'), server.cmd_prefix)


async def cmd_help_page(server, message, page, reactions=[]):
    text = ""
    with open(f'./lang/{server.lang}/help/{page.lower()}.txt') as fp:
        text += fp.read()
    embed = simple_embed(title=f'Help - {page}', value=replace_textfile_text_variables(server, message, text),
                              color=COLOR.LIGHT_BLUE)
    await message.clear_reactions()
    await message.edit(embed=embed)
    for reaction in reactions:
        await message.add_reaction(reaction)
    return True


async def cmd_help_commands(server, userid, channel, message):
    return await cmd_help_page(server, message, 'Commands', [HELP_HOME_EMOJI])


async def cmd_help_languages(server, userid, channel, message):
    return await cmd_help_page(server, message, 'Languages', [HELP_HOME_EMOJI])


async def cmd_help_games(server, userid, channel, message):
    return await cmd_help_page(server, message, 'Games', [HELP_HOME_EMOJI])


async def cmd_help_home(server, userid, channel, message):
    return await cmd_help_page(server, message, 'Home', [HELP_GAMES_EMOJI, HELP_COMMANDS_EMOJI, HELP_LANGUAGE_EMOJI])


async def cmd_help(server, userid, channel, message):
    text = ""
    with open(f'./lang/{server.lang}/help/home.txt') as fp:
        text += fp.read()
    help_embed = simple_embed(title='Help', value=replace_textfile_text_variables(server, message, text), color=COLOR.LIGHT_BLUE)
    help_message = await message.channel.send(embed=help_embed)
    await help_message.add_reaction(HELP_GAMES_EMOJI)
    await help_message.add_reaction(HELP_COMMANDS_EMOJI)
    await help_message.add_reaction(HELP_LANGUAGE_EMOJI)
    return True


HelpGamesCmd = ServerCmd('help_games', cmd_help_games)
HelpGamesCmd.required_perks = ['cmd.help']

HelpCommandsCmd = ServerCmd('help_commands', cmd_help_commands)
HelpCommandsCmd.required_perks = ['cmd.help']

HelpLanguagesCmd = ServerCmd('help_languages', cmd_help_languages)
HelpLanguagesCmd.required_perks = ['cmd.help']

HelpHomeCmd = ServerCmd('help_home', cmd_help_home)
HelpHomeCmd.required_perks = ['cmd.help']

HelpCmd = ServerCmd('help', cmd_help)
HelpCmd.required_perks = ['cmd.help']
CommandsCmd = ServerCmd('commands', cmd_help)
CommandsCmd.required_perks = ['cmd.commands']
