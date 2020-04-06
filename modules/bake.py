
import dataset


async def cheat(self, c, n, m):
  if not await self.is_admin(n):
    await self.message(c,'{} was a bad bad bad. {} got sucked into the oven'.format(n,n))
  m = m.split(' ')
  if len(m) > 2:
    await message(c, 'i refuse.')
    return
  inv = self.db['inv']
  inv.insert(dict(name=m[0], item=m[1]))
  await self.message(c,'ok il allow this once')

async def bake(self, c, n, m):
  if len(m) < 1:
    await self.message(c, 'Dummy thicc you cant bake air!')
    return
  inv = self.db['inv']
  its = (inv.find(name=n, item=m))
  supp = len(list(its))
  if supp < 1:
    await self.message(c, 'You dont have any {}'.format(m))
    return
  await self.message(c, 'You bake one of your {}, and out pops a undefined!'.format(m))


async def init(self):
  self.db = dataset.connect('sqlite:///database.db')

  self.cmd['bake'] = bake
  self.cmd['cheat'] = cheat

