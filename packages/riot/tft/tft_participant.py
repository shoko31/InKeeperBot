# tft_participant.py

from json import dumps


class TFTParticipant:

    def __init__(self, puuid, placement, level, last_round, units, traits):
        self.puuid = puuid
        self.placement = placement
        self.level = level
        self.last_round = last_round
        self.units = units
        self.traits = traits

    def __str__(self):
        return 'TFTParticipant ' + dumps({k: str(v) for k, v in self.__dict__.items()})

    @staticmethod
    def from_json(p):
        units = None
        traits = None
        return TFTParticipant(p['puuid'], p['placement'], p['level'], p['last_round'], units, traits)
