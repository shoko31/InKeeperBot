# tft_trait.py

from json import dumps


class TFTTrait:

    def __init__(self, name, tier_current, tier_total, num_unit):
        self.name = name
        self.tier_current = tier_current
        self.tier_total = tier_total
        self.num_unit = num_unit

    def __str__(self):
        return 'TFTTrait ' + dumps({k: str(v) for k, v in self.__dict__.items()})
