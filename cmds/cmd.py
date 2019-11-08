# cmd.py

class ServerCmd:

    def __init__(self, name, act):
        self.name = name
        self.action = act

    def can_execute(self):
        return True

    async def run_cmd(self, server, userid, channel, message):
        await self.action(server, userid, channel, message)
