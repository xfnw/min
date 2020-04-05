
import importlib


async def commit(self, chan, source, msg):
  await self.quit('{} told me to commit {}'.format(source,msg))

async def quit(self, chan, source, msg):
  await self.quit('{} told me to {}'.format(source,msg))



async def reloadmods(self, chan, source, msg):
  await self.message(chan, 'reloading modules...')
  self.cmd = {}
  self.raw = {}
  self.help = {}
  for i in self.modules:
    importlib.reload(self.modules[i])
    await self.modules[i].init(self)
  await self.message(chan, 'done! did something break? if so you might need to restart')



commands = {
  'quit': quit,
  'reload': reloadmods,
  'commit': commit
}

async def adminHandle(self, chan, source, msg):
  if await self.is_admin(source):
    msg = msg.split(' ')
    if len(msg) < 1 or not msg[0] in commands:
      await self.message(chan, 'you press the wrong button on the oven and it burns you')
      return
    print('[ADMIN MODULE] {} told me to {}!!!'.format(source,msg[0]))
    await commands[msg.pop(0)](self, chan, source, ' '.join(msg))
  else:
    await self.message(chan, 'you try to open it, but the oven is locked')


async def init(self):
  self.cmd['admin'] = adminHandle
