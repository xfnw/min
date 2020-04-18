#!/usr/bin/env python3


import pydle, asyncio, sys, os, time

class Oven(pydle.Client):
  async def on_connect(self):
    print('Connected!')

    self.modules = {}
    self.cmd = {}
    self.raw = {}
    self.help = {}

    self.timeout=time.time()+1

    print('loading modules...')
    await self.loadMods()
    print('joining channels')
    for i in self.chansjoin:
      await self.join(i)
    print('Done!')

  async def loadMods(self):
    for i in [s for s in os.listdir('modules') if ".py" in s]:
      i = i[:-3]
      print('loading', i)
      m = __import__("modules."+i)
      m = eval('m.'+i)
      await m.init(self)
      self.modules[i] = m

  async def on_invite(self, channel, by):
    print('{} invited me to {}!'.format(by, channel))
    await self.join(channel)


  async def on_message(self, chan, source, msg):
    if source != self.nickname:
      if msg == '!botlist':
        await self.message(chan, 'hoinlo im oven im owned by lickthecheese and bake stuff for you and other beep boop fun stuff')
      for i in self.raw:
        await self.raw[i](self, chan,source,msg)
      if msg[:len(self.prefix)] == self.prefix:
        if time.time() < self.timeout:
          self.timeout += 2
          print('messages are being sent too fast!')
          return

        if time.time()-1 < self.timeout:
          await self.message(chan, 'woah woah, slow it down there, or il get mad and wont bake your food')
        self.timeout = time.time()+0.5
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

  async def on_private_message(self, trash, source, msg):
    if source != self.nickname:
      await self.on_message(source, source, msg)


if __name__ == "__main__":
  client = Oven('oven', realname='Oven IRC Bot')
  client.admins = ['lickthecheese', 'ben', 'cmccabe']
  client.prefix = 'ov '
  client.run('team.tilde.chat', tls=True, tls_verify=False)

