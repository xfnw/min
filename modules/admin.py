

async def adminHandle(self, chan, source, msg):
  await self.message(chan, msg)


async def init(self):
  self.cmd['admin'] = adminHandle
