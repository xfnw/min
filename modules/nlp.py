from bot import *

import dataset, random, time, re

async def rec(self, m):
  prew = shared.db['prew']
  noch = shared.db['noun']
  beg = shared.db['beg']
  end = shared.db['end']
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
    if c in shared.cstate:
        oldnoun = shared.cstate[c]
    else:
        oldnoun = None

    shared.db['remsg'].insert_ignore(dict(noun=oldnoun,msg=' '.join(words)),['id'])

    nouns = [i['word'] for i in shared.db['noun'].find()]
    out = {}
    for i in words:
        out[i] = nouns.count(i)
    noun = min(out, key=out.get)

    conversation = shared.db['conver']
    if oldnoun != None:
        print("adding", [oldnoun,noun])
        conversation.insert_ignore(dict(pre=oldnoun,pro=noun),['id'])

    nextnoun = [i['pro'] for i in conversation.find(pre=noun)]
    print("nextnoun:",nextnoun)
    if len(nextnoun) > 0:
        noun = random.choice(nextnoun)
    shared.cstate[c] = noun
    return noun
  
async def genOut(self, noun):
  oldresponses = [i['msg'] for i in shared.db['remsg'].find(noun=noun)]
  if len(oldresponses) > 0:
    return random.choice(oldresponses).split(' ')
  prew = shared.db['prew']
  beg = [ i['word'] for i in shared.db['beg'].find() ]
  end = [ i['word'] for i in shared.db['end'].find() ]
  nouns = [i['word'] for i in shared.db['noun'].find()]
  iter=0
  out = [noun]
  while (out[0] not in beg or nouns.count(out[0])-1 > iter * shared.enmul) and iter < 7:
    try:
      out = [ random.choice(list(prew.find(pro=out[0])))['pre'] ] + out
    except IndexError:
      iter += 69
    iter += 1
  iter = 0
  while (out[-1] not in end or nouns.count(out[-1])-1 > iter * shared.enmul) and iter < 7:
    
    try:
      out.append(random.choice(list(prew.find(pre=out[-1])))['pro'])
    except IndexError:
      iter += 69
    iter += 1
  return out


async def filter(self, c, n, m):
  if c in shared.qtime and shared.qtime[c] > time.time():
    return
  if m[:len(shared.prefix)] == shared.prefix:
    m = m[len(shared.prefix):]
    await go(self, c, n, m)
  elif m[:len(self.nickname)+1] == self.nickname+' ':
    m = m[len(self.nickname)+1:]
    await go(self, c, n, m)
  elif '#' not in c and n != self.nickname:
    await go(self, c, n, m)
  else:
    if len(m.split(' ')) > 1:
      if shared.learntime + shared.learndelay < time.time():
        await rec(self, m)
        shared.learntime = time.time()

async def go(self, c, n, m):
    await rec(self, m)
    words = re.sub(r'([\.,\?!])', r' \1', m).split()
    if words[0] == 'admin':
      return
    await self.message(c, ' '.join(await genOut(self, await getNoun(self, words, c))))

async def init(self):
  
  shared.qtime = {}
  shared.learntime = 0

  # delay between grabbing random messages and passively
  # learning.
  shared.learndelay = 1
  # sentance ending weight, lower means longer sentances,
  # higher means shorter sentances. this will need to slowly
  # get larger as the database grows
  shared.enmul = 6
  

  shared.rawm['nlp'] = filter
  shared.cstate = {}
