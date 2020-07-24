import time

async def invite(self, channel, by):

    if self.db['invite'].find_one(blacklist=channel):
        print('{} invited me to {}, a blacklisted channel'.format(by,channel))
        return

    if self.db['invite'].find_one(enabled='true'):

        print('{} invited me to {}!'.format(by, channel))
        self.t = time.time()+1
        await self.join(channel)
    else:
        if self.chandb.find_one(name=channel):
            self.t = time.time()+1
            await self.join(channel)
            print('whee invited to {} by {}'.format(channel,by))
            return
            
        print('ive been invited but invites are disabled')


async def init(self):
    pass

