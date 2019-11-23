# cmd_xp.py

import discord
from user import User
from lang.lang import Lang
from cmds.cmd import ServerCmd


async def cmd_force_save(server, userid, channel, message):
    await channel.send('Saving server state..')
    server.save(server)
    await channel.send('Server saved !')
    return True


ForceSaveCmd = ServerCmd('forcesave', cmd_force_save)
ForceSaveCmd.required_perks = ['cmd.forcesave']
