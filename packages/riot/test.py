# test.py

from tft import TFTUser

user = TFTUser.fetch_by_summoner('death0064')
user.load_games()
user.games[0].load()
print('LAST GAME')
print(user.games[0])
#print(user)
