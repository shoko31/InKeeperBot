# cmd_prefix.py

from lang.lang import Lang
from cmds.cmd import ServerCmd
from user import User


async def cmd_set_lang(server, userid, channel, message):
    splited_message = str(message.content).split()
    new_lang = splited_message[1]
    server.lang = new_lang
    await channel.send(Lang.get('CMD_LANG_SET', server.lang).format(new_lang))
    return True


async def cmd_get_lang(server, userid, channel, message):
    await channel.send(Lang.get('CMD_LANG_GET', server.lang).format(server.lang))
    return True


async def cmd_lang(server, userid, channel, message):
    splited_message = str(message.content).split()
    if len(splited_message) == 1:  # No argument, display current server lang
        return await LangGetCmd.run_cmd(server, userid, channel, message)
    else:  # Argument found, changing the lang
        return await LangSetCmd.run_cmd(server, userid, channel, message)


LangGetCmd = ServerCmd('langget', cmd_get_lang)
LangGetCmd.required_perks = ['cmd.lang', 'cmd.lang.display']

LangSetCmd = ServerCmd('langset', cmd_set_lang)
LangSetCmd.required_perks = ['cmd.lang', 'cmd.lang.change']

LangCmd = ServerCmd('lang', cmd_lang)
LangCmd.required_perks = ['cmd.lang', 'cmd.lang.display', 'cmd.lang.change']
