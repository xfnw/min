
import asyncio

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        return stdout.decode()
    if stderr:
        #print(f'[markov stderr]\n{stderr.decode()}')
        return



async def markov(self, c, n, m):
    m = ''.join([i for i in m if i.isalnum()])
    if len(m) > 0:
       await self.message(c, (await run("markov '{}'".format(m)))[:-1])
       return
    await self.message(c, 'the oven went boop')

async def init(self):
    self.cmd['m'] = markov
    self.cmd['markov'] = markov
    self.help['markov'] = ["markov <seed> - generate markov chains", "https://en.wikipedia.org/wiki/Markov_chain"]





