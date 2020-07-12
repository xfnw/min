
import dataset
import random
import time

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
      prew.insert_ignore(dict(pre=pre, pro=w),['id'])
    pre = w
    noch.insert(dict(word=w))
  end.insert(dict(word=pre))
  
async def getNoun(self, words, c):
    if c in self.cstate:
        oldnoun = self.cstate[c]
    else:
        oldnoun = None
    nouns = [i['word'] for i in self.db['noun'].find()]
    out = {}
    for i in words:
        out[i] = nouns.count(i)
    noun = min(out, key=out.get)

    conversation = self.db['conver']
    if oldnoun != None:
        print("adding", [oldnoun,noun])
        conversation.insert_ignore(dict(pre=oldnoun,pro=noun),['id'])

    nextnoun = [i['pro'] for i in conversation.find(pre=noun)]
    print("nextnoun:",nextnoun)
    if len(nextnoun) > 0:
        noun = random.choice(nextnoun)
    self.cstate[c] = noun
    return noun
  
async def genOut(self, noun):
  prew = self.db['prew']
  beg = [ i['word'] for i in self.db['beg'].find() ]
  end = [ i['word'] for i in self.db['end'].find() ]
  nouns = [i['word'] for i in self.db['noun'].find()]
  iter=0
  out = [noun]
  while (out[0] not in beg or nouns.count(out[0])-1 > iter * self.enmul) and iter < 7:
    try:
      out = [ random.choice(list(prew.find(pro=out[0])))['pre'] ] + out
    except IndexError:
      iter += 69
    iter += 1
  iter = 0
  while (out[-1] not in end or nouns.count(out[-1])-1 > iter * self.enmul) and iter < 7:
    
    try:
      out.append(random.choice(list(prew.find(pre=out[-1])))['pro'])
    except IndexError:
      iter += 69
    iter += 1
  return out


async def filter(self, c, n, m):
  if c in self.qtime and self.qtime[c] > time.time():
    return
  if m[:len(self.prefix)] == self.prefix:
    m = m[len(self.prefix):]
    await go(self, c, n, m)
  elif m[:4] == 'kim ':
    m = m[4:]
    await go(self, c, n, m)
  else:
    if len(m.split(' ')) > 1:
      if self.learntime + self.learndelay > time.time():
        await rec(self, m)
        self.learntime = time.time()

async def go(self, c, n, m):
    await rec(self, m)
    words = m.split(' ')
    if words[0] == 'admin':
      return
    await self.message(c, ' '.join(await genOut(self, await getNoun(self, words, c))))

async def init(self):
  
  self.qtime = {}

  self.learntime = 0
  self.learndelay = 2
  self.enmul = 25
  self.raw['nlp'] = filter

  self.cstate = {}
