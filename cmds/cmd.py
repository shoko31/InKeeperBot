# cmd.py

from lang.lang import Lang
from config import cfg
from user import User
from perks import Perks

class ServerCmd:

    def __init__(self, name, act):
        self.name = name
        self.action = act
        self.required_perks = []

    def can_execute(self, server, userid):
        if len(self.required_perks) == 0:
            return True

        server_user = server.guild.get_member(userid)
        if server_user.guild_permissions.administrator is True:
            return True

        user_roles = server_user.roles
        for role in user_roles:
            if str(role.id) in server.group_perks.keys():
                group_perk = server.group_perks[str(role.id)]
                for perk in group_perk:
                    if str(perk).startswith('group.'): # group perm
                        if len(list(set(Perks.groups[perk]) & set(self.required_perks))) > 0:
                            return True
                    elif str(perk) in self.required_perks:
                        return True
        return False

    async def run_cmd(self, server, userid, channel, message):
        if not self.can_execute(server, userid):
            await channel.send(
                Lang.get('MISSING_PERM', server.lang).replace(cfg.get_value('TEXTFILE_USER_MENTION'), User.get_at_mention(userid)))
            return False
        else:
            return await self.action(server, userid, channel, message)
