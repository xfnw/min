
import importlib, time, asyncio, pydle

async def commit(self, chan, source, msg):
  await self.quit('{} told me to commit {}'.format(source,msg))

async def quit(self, chan, source, msg):
  await self.quit('{} told me to {}'.format(source,msg))



async def reloadmods(self, chan, source, msg):
  await self.message(chan, '[\x036admin\x0f] reloading modules...')
  self.oldcmd = self.cmd
  self.cmd = {}
  self.raw = {}
  self.help = {}
  try:
    for i in self.modules:
      importlib.reload(self.modules[i])
      await self.modules[i].init(self)
      #await self.message(chan, '[\x036admin\x0f] load {} sucess!'.format(i))
    await self.message(chan, '[\x036admin\x0f] done! {} modules reloaded!'.format(len(self.modules)))
  except:
    await self.message(chan, '[\x036admin\x0f] reload failed... attempting to recover...')
    self.cmd = self.oldcmd
  

async def part(self, chan, source, msg):
  await self.message(chan, '[\x036admin\x0f] bye {}'.format(msg))
  await self.part(msg)

async def join(self, chan, source, msg):
  self.t = time.time()+1
  await self.message(chan, '[\x036admin\x0f] joined {}'.format(msg))
  await self.join(msg)

async def joins(self, chan, source, msg):
  await self.message(chan, '[\x036admin\x0f] I will drop commands for some seconds to ignore chanhistory...')
  for i in self.chandb.all():
    self.t = time.time() + 2
    try:
        await self.join(i['name'])
        await asyncio.sleep(2)
        print('joined {}'.format(i['name']))
    except pydle.client.AlreadyInChannel:
        print('I am already in {}'.format(i['name']))
  await asyncio.sleep(2)
  await self.message(chan, '[\x036admin\x0f] Sucess!')

async def aexec(self, code):
    # Make an async function with the code and `exec` it
    exec(
        f'async def __ex(self): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )

    # Get `__ex` from local variables, call it and return the result
    return await locals()['__ex'](self)


async def ev(self, chan, source, msg):
  msg = msg.split(' ')
  try:
    await self.message(chan, '[\x036admin\x0f] ok, output: {}'.format(
        str(await aexec(self, ' '.join(msg)))[:400]
      ))
  except:
    await self.message(chan, '[\x036admin\x0f] exception in eval!')

async def send(self, c, n, m):
  msg = m.split(' ')
  await self.message(msg.pop(0), ' '.join(msg))
  await self.message(c, '[\x036admin\x0f] sent')

async def shut(self, c, n, m):
  self.qtime[c] = time.time()+(60*10)
  await self.message(c, '[\x036admin\x0f] Ok, il be back in 10 minutes')

async def schans(self, c, n, m):
  self.chandb.delete()
  for i in self.channels:
      self.chandb.insert(dict(name=i))
  await self.message(c, '[\x036admin\x0f] Ok')




commands = {
  'quit': quit,
  'reload': reloadmods,
  'commit': commit,
  'part': part,
  'join': join,
  'eval': ev,
  'send': send,
  'joins': joins,
  'shut': shut,
  'schans': schans
}

async def adminHandle(self, chan, source, msg):
  if await self.is_admin(source):
    msg = msg.split(' ')
    if len(msg) < 1 or not msg[0] in commands:
      await self.message(chan, '[\x036admin\x0f] Invalid command')
      return
    print('[ADMIN MODULE] {} told me to {}!!!'.format(source,msg[0]))
    await commands[msg.pop(0)](self, chan, source, ' '.join(msg))
  else:
    await self.message(chan, '[\x036admin\x0f] You do not have permission to do this')


async def init(self):
  self.chandb = self.db['chan']
  self.cmd['admin'] = adminHandle
  
  self.help['admin'] = ['admin - various bot owner commands (more for subcommands)', 'sub-commands of admin, for more info do help admin <command>: quit reload commit part join joins eval send']
  self.help['admin quit'] = ['admin quit <message> - make the bot disconnect','no']
  self.help['admin reload'] = ['admin reload - reload the modules and configs', 'nothing to see here']
  self.help['admin commit'] = ['admin commit <action> - oh no (more)', 'suggested with <3 by khux']
  self.help['admin part'] = ['admin part <channel> - leave a channel', ':o']
  self.help['admin join'] = ['admin join <channel> - make the bot join a channel','...']
  self.help['admin joins'] = ['admin joins - join more channels', 'dont reconnect to a bunch of chans when the bots crashing etc']
  self.help['admin eval'] = ['admin eval <command> - absolute power corrupts absolutely', 'lmao']
  self.help['admin send'] = ['admin send <channel> <message> - send a message', 'lmao']
  self.help['admin schans'] = ['admin schans - save the commands to join',';p;']



