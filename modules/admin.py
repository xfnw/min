
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

  

async def part(self, chan, source, msg):
  await self.message(chan, 'bye {}'.format(msg))
  await self.part(msg)

async def join(self, chan, source, msg):
  await self.message(chan, 'joined {}'.format(msg))
  await self.join(msg)

async def joins(self, chan, source, msg):
  for i in self.joins:
    await self.join(i)

async def ev(self, chan, source, msg):
  msg = msg.split(' ')
  exec(' '.join(msg))
  await self.message(chan, 'ok')

commands = {
  'quit': quit,
  'reload': reloadmods,
  'commit': commit,
  'part': part,
  'join': join,
  'eval': ev,
  'joins': joins
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
  self.joins = ["#chaos", "#lickthecheese", "#windowsloser", "#cminecraft", "#team", "#meta", "#rscmakerspace", "#archlinux", "#tildetel", "#one", "#starlanes"]
  
  self.help['admin'] = ['admin - various bot owner commands (more for subcommands)', 'sub-commands of admin, for more info do help admin <command>: quit reload commit part join joins eval']
  self.help['admin quit'] = ['admin quit <message> - make the bot disconnect','no']
  self.help['admin reload'] = ['admin reload - reload the modules and configs', 'nothing to see here']
  self.help['admin commit'] = ['admin commit <action> - oh no (more)', 'suggested with <3 by khux']
  self.help['admin part'] = ['admin part <channel> - leave a channel', ':o']
  self.help['admin join'] = ['admin join <channel> - make the bot join a channel','...']
  self.help['admin joins'] = ['admin joins - join more channels', 'dont reconnect to a bunch of chans when the bots crashing etc']
  self.help['admin eval'] = ['admin eval <command> - absolute power corrupts absolutely', 'lmao']



