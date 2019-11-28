# perks.py


class PerksClass:

    def __init__(self):
        self.perks = [
            'cmd.version',
            'cmd.accept.toggle', 'cmd.accept.set'
            'cmd.afk', 'cmd.stopafk',
            'cmd.help', 'cmd.commands'
            'cmd.perm', 'cmd.perm.display', 'cmd.perm.change',
            'cmd.prefix', 'cmd.prefix.display', 'cmd.prefix.change',
            'cmd.warn',
            'cmd.warns', 'cmd.warns.self', 'cmd.warns.other',
            'cmd.mute', 'cmd.unmute',
            'cmd.deafen', 'cmd.undeafen',
            'cmd.lang', 'cmd.lang.display', 'cmd.lang.change',
            'cmd.xp', 'cmd.xp.give', 'cmd.xp.display', 'cmd.xp.display.other', 'cmd.xp.display.self',
            'cmd.tft',
            'cmd.forcesave',
            'cmd.daily_reward',
            'cmd.dice'
        ]

        self.groups = {
            'group.admin': [
                'cmd.version', 'cmd.accept.toggle', 'cmd.accept.set', 'cmd.afk', 'cmd.stopafk', 'cmd.help', 'cmd.commands', 'cmd.perm',
                'cmd.prefix', 'cmd.warn', 'cmd.warns', 'cmd.mute', 'cmd.unmute', 'cmd.deafen', 'cmd.undeafen', 'cmd.lang', 'cmd.xp',
                'cmd.tft', 'cmd.forcesave', 'cmd.daily_reward', 'cmd.dice'
            ],
            'group.moderator': [
                'cmd.afk', 'cmd.stopafk', 'cmd.help', 'cmd.commands', 'cmd.prefix.display', 'cmd.warn', 'cmd.warns',
                'cmd.mute', 'cmd.unmute', 'cmd.deafen', 'cmd.undeafen', 'cmd.lang.display', 'cmd.xp.display', 'cmd.daily_reward',
                'cmd.dice'
            ],
            'group.user': [
                'cmd.afk', 'cmd.stopafk', 'cmd.help', 'cmd.commands', 'cmd.prefix.display',
                'cmd.warns.self', 'cmd.xp.display.self', 'cmd.daily_reward'
            ],
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
