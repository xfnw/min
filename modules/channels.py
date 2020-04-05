

async def init(self):
  self.chansjoin = ['#bots']
  
  print('joining channels', ' '.join(self.chansjoin))
  for i in self.chansjoin:
    await self.join(i)



