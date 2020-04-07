
import dataset
import random


async def cheat(self, c, n, m):
  if not await self.is_admin(n):
    await self.message(c,'{} was a bad bad bad. {} got sucked into the oven'.format(n,n))
  m = m.split(' ')
  if len(m) < 2:
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
  its = (inv.find_one(name=n, item=m))
  if its == None:
    await self.message(c, 'You dont have any {}'.format(m))
    return
  
  # if item has value, use that, else use a okay value
  if m in list(self.bakedGoods.keys()):
    value = self.bakedGoods[m]
  else:
    value = 15
  
  # consume the item
  inv.delete(id=its['id'])
  
  # oooo randomize what will pop out
  value += random.uniform(-20, 20)
  
  # choose the output
  while value not in list(self.bakedPrice.keys()):
    value = int(value - 1)
    if value < 0:
      await self.message(c, 'you notice some smoke, shouldint have put that {} in the oven!'.format(m))
      return

  newitem = self.bakedPrice[value]

  inv.insert(dict(name=n, item=newitem))

  await self.message(c, 'You bake your {}, and out pops a {}!'.format(m, newitem))

async def invsee(self, c, n, m):
  if len(m) < 1:
    m = n
  inv = self.db['inv']
  it = [ i['item'] for i in inv.find(name=m) ]
  if len(it) < 1:
    await self.message(c, 'you look through your kitchen and see nothing')
  else:
    await self.message(c, 'you look through your kitchen and see {}, with a combined value of ${}'.format(' '.join(it), sum([self.bakedGoods[i] for i in it if i in self.bakedGoods])/10))

async def generate(self, c, n, m):
  if int(random.uniform(0,30)) == 1:
    inv = self.db['inv']
    inv.insert(dict(name=n, item=random.choice(list(self.bakedGoods.keys()))))
    qed = self.db['qed']
    if qed.find_one(name=n) == None:
      qed.insert(dict(name=n))
      await self.message(n, 'Ding! you left some stuff in the oven! (you were lucky and found an item!!!) check out what you have with "ov items" and you can do cool stuff like bake them! (i will not query you again, so periodically check for new items!)')

async def init(self):
  self.db = dataset.connect('sqlite:///database.db')

  self.cmd['bake'] = bake
  self.cmd['cheat'] = cheat
  self.cmd['inv'] = invsee
  self.cmd['items'] = invsee
  self.cmd['goods'] = invsee

  self.help['bake'] = ['bake <item> - bake some stuff', 'dont dirty the oven!']
  self.help['cheat'] = ['cheat <user> <item> - you are bad if you use it', 'bad bad bad bad']
  self.help['items'] = ['items - show the stuff in your inventory (more for aliases)', 'aliases for items include: inv, goods']

  self.raw['genGoods'] = generate

  self.bakedGoods = {
    'cheese': 50,
    'wheat': 1,
    'turd': 0,
    'flour': 10,
    'bread': 30,
    'crispy': 15,
    'tortilla': 35,
    'egg': 20,
    'bird': 32,
    'erotic': 69,
    'phallic': 65,
    'pizza': 34,
    'hairball': 6,
    'cookie': 44
  }
  self.bakedPrice = dict((v,k) for k,v in self.bakedGoods.items())

