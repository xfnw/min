#!/usr/bin/env python3


import pydle, asyncio

class Oven(pydle.Client):
  async def on_connect(self):
    print('Connected!')


    await self.join('#bots')
  async def on_message(self, chan, source, msg):
    if source != self.nickname:
      await self.message(chan, ' '.join(await self.whois(source).keys()))


if __name__ == "__main__":
  client = Oven('oven', realname='Oven IRC Bot')
  client.run('irc.tilde.chat', tls=True, tls_verify=False)

