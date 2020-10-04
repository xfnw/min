
async def action(self,c,n,m):
    await self.message(c,'\x01ACTION {}\x01'.format(m[:400]))


async def echo(self,c,n,m):
    await self.message(c,'[\x036channels\x0f] {}'.format(m[:400]))

async def init(self):
  self.chansjoin = ['#bots']
  
  self.cmd['echo']=echo
  self.cmd['action']=action
  


