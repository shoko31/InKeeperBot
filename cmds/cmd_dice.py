# cmd_dice.py

from cmds.cmd import ServerCmd
from utils import simple_embed, COLOR
import random


async def cmd_dice(server, userid, channel, message):
    split_message = message.content.split()
    num_dice = 1
    if len(split_message) > 1:
        try:
            num_dice = int(split_message[1])
            if num_dice < 1:
                num_dice = 1
            elif num_dice > 9:
                num_dice = 9
        except ValueError:
            num_dice = 1
    dice_embed = simple_embed(color=COLOR.LIGHT_PURPLE)
    dice_embed.clear_fields()
    for i in range(num_dice):
        dice_embed.add_field(name=':game_die:', value='\32' + str(random.randint(1, 6)), inline=True)
    await channel.send(embed=dice_embed)

DiceCmd = ServerCmd('dice', cmd_dice)
DiceCmd.required_perks = ['cmd.dice']
