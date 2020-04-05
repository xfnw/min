#!/usr/bin/env python3


import pydle, asyncio, sys, os

class Oven(pydle.Client):
  async def on_connect(self):
    print('Connected!')

    self.modules = {}
    self.cmd = {}
    self.raw = {}
    self.help = {}

    print('loading modules...')
    await self.loadMods()
    print('Done!')

  async def loadMods(self):
    for i in [s for s in os.listdir('modules') if ".py" in s]:
      i = i[:-3]
      print('loading', i)
      m = __import__("modules."+i)
      m = eval('m.'+i)
      await m.init(self)
      self.modules[i] = m




  async def on_message(self, chan, source, msg):
    if source != self.nickname:
      if msg == '!botlist':
        await self.message(chan, 'hoinlo im oven im owned by lickthecheese and bake stuff for you')
      for i in self.raw:
        await self.raw[i](self, chan,source,msg)
      if msg[:len(self.prefix)] == self.prefix:
        msg = msg[len(self.prefix):]
        cmd = msg.split(' ')[0]
        msg = msg[len(cmd)+1:]
        if cmd in self.cmd:
          await self.cmd[cmd](self, chan, source, msg)
  async def is_admin(self, nickname):
    admin = False

    # Check the WHOIS info to see if the source has identified with NickServ.
    # This is a blocking operation, so use yield.
    if nickname in self.admins:
      info = await self.whois(nickname)
      admin = info['identified']

    return admin



if __name__ == "__main__":
  client = Oven('oven', realname='Oven IRC Bot')
  client.admins = ['lickthecheese']
  client.prefix = 'ov '
  client.run('team.tilde.chat', tls=True, tls_verify=False)

