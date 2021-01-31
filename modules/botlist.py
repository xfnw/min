from bot import *

@rawm('botlist')
async def botlist(self,channel,nick,msg):
    if msg == '!botlist':
        await message(self,'botlist',channel,'Hi, im kim. im a machine learning chatbot')



async def init(self):
    pass
