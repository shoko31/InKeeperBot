# lang.py

import json


class Lang:

    def __init__(self):
        self.langs = {}
        self.load_lang('fr')
        self.load_lang('en')

    def load_lang(self, lang_key):
        with open(f'./lang/{lang_key}/{lang_key}.lang') as fp:
            lines = fp.read()
        self.langs[lang_key] = json.loads(lines)

    @staticmethod
    def get(key, lang):
        if lang not in instance.langs.keys():
            raise Exception(f'Lang "{lang}" does not exist')
        if key not in instance.langs[lang].keys():
            raise Exception(f'Lang key "{key}" does not exist for lang "{lang}"')
        return instance.langs[lang][key]


instance = Lang()
