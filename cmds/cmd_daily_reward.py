# cmd_daily_reward.py

from cmds.cmd import ServerCmd
from user import User
from datetime import datetime, timedelta
from math import floor
from lang.lang import Lang

async def cmd_daily_reward(server, userid, channel, message):
    if userid in server.members.keys():
        member = server.members[userid]
        now = datetime.now()
        daily_time = 86400 - (now - member.last_daily_reward).total_seconds()
        seconds = floor(daily_time % 60)
        minutes = floor(daily_time / 60)
        hours = floor(minutes / 60)
        minutes = minutes % 60
        display = f"{str(hours) + Lang.get('HOURS', server.lang) + ' ' if hours > 0 else ''}{str(minutes) + Lang.get('MINUTES', server.lang) + ' ' if minutes > 0 else ''}{str(seconds) + Lang.get('SECONDS', server.lang) + ' ' if seconds > 0 else ''}"
        await channel.send(Lang.get('NEXT_DAILY_XP_REWARD', server.lang).format(User.get_at_mention(userid), display))
        return True
    return False

DailyRewardCmd = ServerCmd('daily', cmd_daily_reward)
DailyRewardCmd.required_perks = ['cmd.daily_reward']

DailyRewardAliasCmd = ServerCmd('dailyreward', cmd_daily_reward)
DailyRewardAliasCmd.required_perks = ['cmd.daily_reward']
