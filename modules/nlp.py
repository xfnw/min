
import dataset
import random

async def rec(self, m):
  prew = self.db['prew']
  noch = self.db['noun']
  beg = self.db['beg']
  end = self.db['end']
  pre = ''
  words = m.split(' ')
  if words[0] == 'admin':
    return
  for w in words:
    if pre == '':
      beg.insert(dict(word=w))
    else:
      prew.insert(dict(pre=pre, pro=w))
    pre = w
    noch.insert(dict(word=w))
  end.insert(dict(word=pre))
  
async def getNoun(self, words):
  nouns = [i['word'] for i in self.db['noun'].find()]
  out = {}
  for i in words:
    out[i] = nouns.count(i)
  return min(out, key=out.get)
  
async def genOut(self, noun):
  prew = self.db['prew']
  beg = [ i['word'] for i in self.db['beg'].find() ]
  end = [ i['word'] for i in self.db['end'].find() ]
  iter=0
  out = [noun]
  while out[0] not in beg and iter < 7:
    out = [ random.choice(list(prew.find(pro=out[0])))['pre'] ] + out
    iter += 1
  iter = 0
  while out[-1] not in end and iter < 7:
    out.append(random.choice(list(prew.find(pre=out[-1])))['pro'])
    iter += 1
  return out


async def filter(self, c, n, m):
  if m[:5] == 'kim: ':
    m = m[5:]
    await rec(self, m)
    words = m.split(' ')
    if words[0] == 'admin':
      return
    await self.message(c, ' '.join(await genOut(self, await getNoun(self, words))))

async def init(self):
  self.db = dataset.connect('sqlite:///database.db')

  self.raw['nlp'] = filter

