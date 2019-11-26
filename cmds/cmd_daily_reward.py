# cmd_daily_reward.py

from cmds.cmd import ServerCmd
from user import User
from datetime import datetime, timedelta

async def cmd_daily_reward(server, userid, channel, message):
    if userid in server.members.keys():
        member = server.members[userid]
        now = datetime.now()
        await channel.send(f'Next daily reward for {User.get_at_mention(userid)} in `{(now - member.last_daily_reward).strftime("%H:%M:%S")}`')
        return True
    return False

DailyRewardCmd = ServerCmd('daily', cmd_daily_reward)
DailyRewardCmd.required_perks = ['cmd.daily_reward']
