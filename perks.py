# perks.py


class PerksClass:

    def __init__(self):
        self.perks = [
            'cmd.afk', 'cmd.stopafk',
            'cmd.help', 'cmd.commands'
            'cmd.perm', 'cmd.perm.display', 'cmd.perm.change',
            'cmd.prefix', 'cmd.prefix.display', 'cmd.prefix.change',
            'cmd.warn',
            'cmd.warns', 'cmd.warns.self', 'cmd.warns.other',
            'cmd.mute'
        ]

        self.groups = {
            'group.admin': ['cmd.afk', 'cmd.stopafk', 'cmd.help', 'cmd.commands', 'cmd.perm', 'cmd.prefix', 'cmd.warn', 'cmd.warns', 'cmd.mute'],
            'group.moderator': ['cmd.afk', 'cmd.stopafk', 'cmd.help', 'cmd.commands', 'cmd.prefix.display', 'cmd.warn', 'cmd.warns', 'cmd.mute'],
            'group.user': ['cmd.afk', 'cmd.stopafk', 'cmd.help', 'cmd.commands', 'cmd.prefix.display', 'cmd.warns.self'],
            'group.guest': ['cmd.help', 'cmd.commands']
        }

    def is_valid(self, data):
        if type(data) is list:
            for perk in data:
                if self.__check_perk(perk) is False:
                    return False
            return True
        else:
            return self.__check_perk(data)

    def __check_perk(self, perk):
        if perk not in self.perks and perk not in self.groups.keys():
            return False
        return True


Perks = PerksClass()
