from bot import *


@listener("INVITE")
async def on_invite(self, line):
    self.send(build("JOIN", [line.params[1]]))


async def init(self):
    pass
