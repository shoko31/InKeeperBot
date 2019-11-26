# cmd_daily_reward.py

from cmds.cmd import ServerCmd
from user import User
from datetime import datetime, timedelta
from math import floor

async def cmd_daily_reward(server, userid, channel, message):
    if userid in server.members.keys():
        member = server.members[userid]
        now = datetime.now()
        daily_time = (now - member.last_daily_reward).total_seconds()
        seconds = daily_time % 60
        minutes = floor(daily_time / 60)
        hours = floor(minutes / 60)
        minutes = minutes % 60
        display = f"{str(hours) + 'hours ' if hours > 0 else ''}{str(minutes) + 'minutes ' if minutes > 0 else ''}{str(seconds) + 'seconds ' if seconds > 0 else ''}"
        await channel.send(f'Next daily reward for {User.get_at_mention(userid)} in `{display}`')
        return True
    return False

DailyRewardCmd = ServerCmd('daily', cmd_daily_reward)
DailyRewardCmd.required_perks = ['cmd.daily_reward']
