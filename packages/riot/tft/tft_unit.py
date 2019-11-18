# tft_unit.py

from json import dumps


class TFTUnit:

    def __init__(self, id, name, tier, rarity, items):
        self.id = id
        self.name = name
        self.tier = tier
        self.rarity = rarity
        self.items = items

    def __str__(self):
        return 'TFTUnit ' + dumps({k: str(v) for k, v in self.__dict__.items()})
