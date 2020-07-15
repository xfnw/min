import time

async def invite(self, channel, by):
    if self.db['invite'].find_one(enabled='true'):
        if self.db['invite'].find_one(blacklist=channel):
            print('{} invited me to {}, a blacklisted channel'.format(by,channel))
            return
        print('{} invited me to {}!'.format(by, channel))
        self.t = time.time()+1
        await self.join(channel)
    else:
        print('ive been invited but invites are disabled')


async def init(self):
    pass

