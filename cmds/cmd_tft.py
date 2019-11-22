# cmd_tft.py

import discord
from datetime import datetime
from cmds.cmd import ServerCmd
from packages.riot.tft import TFTUser, TFTGame, TFTParticipant

loaded_tft_user = None


def load_tft_user(user):
    global loaded_tft_user
    if loaded_tft_user is not None and loaded_tft_user.name.lower() == user.lower():
        return True
    loaded_tft_user = TFTUser.fetch_by_summoner(user)
    if loaded_tft_user is None:
        return False

    loaded_tft_user.load_games()


async def cmd_tft(server, userid, channel, message):
    split_content = message.content.split()
    if len(split_content) < 2:
        await channel.send("Missing League of Legends username")
        return False

    msg = await channel.send(f":arrows_counterclockwise: *Loading TFT games for {split_content[1]}..*")
    load_tft_user(split_content[1])

    if len(loaded_tft_user.games) < 1:
        await msg.delete()
        await channel.send(f"No TFT game found for {loaded_tft_user.name}")
    else:
        games_count = len(loaded_tft_user.games)
        for i in range(0, min(5, games_count)):
            game = loaded_tft_user.games[i]
            if game.loaded is False:
                game.load()
        games_msg = f"Last 5 TFT games for {loaded_tft_user.name}"
        for i in range(0, min(5, games_count)):
            game = loaded_tft_user.games[i]
            participant = game.get_participant(loaded_tft_user.puuid)
            games_msg += "\r\n"
            games_msg += f"{i+1} - *[{game.game_time.strftime('%Y-%m-%d %H:%M:%S')}]*  **{participant.placement}/8 {':trophy:' if participant.placement == 1 else ''}**"
        await msg.delete()
        await channel.send(games_msg)
    return True


TFTCmd = ServerCmd('tft', cmd_tft)
TFTCmd.required_perks = ['cmd.tft']
