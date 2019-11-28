# cmd_xp.py

import discord
from user import User
from lang.lang import Lang
from cmds.cmd import ServerCmd
from utils import COLOR, simple_embed
import psycopg2

async def cmd_force_save(server, userid, channel, message):
    saving_embed = simple_embed(value='Saving server state..', color=COLOR.ORANGE)
    saved_embed = simple_embed(value='Server saved !', color=COLOR.LIGHT_GREEN)
    save_error_embed = simple_embed(value='Server save failed !', color=COLOR.RED)
    msg = await channel.send(embed=saving_embed)
    try:
        server.save(server)
    except psycopg2.OperationalError:
        await msg.edit(embed=save_error_embed)
        return False
    except psycopg2.Error:
        await msg.edit(embed=save_error_embed)
        return False
    await msg.edit(embed=saved_embed)
    #await channel.send('Server saved !')
    return True


ForceSaveCmd = ServerCmd('forcesave', cmd_force_save)
ForceSaveCmd.required_perks = ['cmd.forcesave']
