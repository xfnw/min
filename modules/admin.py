import importlib, time, asyncio, random
from bot import *

quitmessages = [
    "time to die",
    "you can hide, but you can not run!",
    "you're next",
    "bye",
    "the balun has been popped.",
]


async def commit(self, chan, source, msg):
    await self.quit("{} told me to commit {}".format(source, msg))


async def quit(self, chan, source, msg):
    await self.send(build("QUIT", [random.choice(quitmessages)]))


async def reloadmods(self, chan, source, msg):
    await self.message(chan, "[\x036admin\x0f] reloading modules...")
    shared.oldcmd = shared.commands
    shared.commands = {}
    shared.rawm = {}
    shared.listeners = []
    shared.help = {}
    try:
        for i in shared.modules:
            importlib.reload(shared.modules[i])
            await shared.modules[i].init(self)
            # await self.message(chan, '[\x036admin\x0f] load {} sucess!'.format(i))
        await self.message(
            chan,
            "[\x036admin\x0f] done! {} modules reloaded!".format(len(shared.modules)),
        )
    except:
        await self.message(
            chan, "[\x036admin\x0f] reload failed... attempting to recover..."
        )
        shared.commands = shared.oldcmd


async def rawcmd(self, chan, source, msg):
    await self.send_raw(msg)


async def joins(self, chan, source, msg):
    await self.message(chan, "[\x036admin\x0f] joining slowly as to not flood...")
    for i in self.chandb.all():
        await self.send(build("JOIN", [i["name"]]))
        await asyncio.sleep(1)
        print("joined {}".format(i["name"]))
    await self.message(
        chan,
        "[\x036admin\x0f] Sucess! i may be laggy for a bit while i sort through all these channels...",
    )


async def aexec(self, code):
    # Make an async function with the code and `exec` it
    exec(f"async def __ex(self): " + "".join(f"\n {l}" for l in code.split("\n")))

    # Get `__ex` from local variables, call it and return the result
    return await locals()["__ex"](self)


async def ev(self, chan, source, msg):
    msg = msg.split(" ")
    try:
        await self.message(
            chan,
            "[\x036admin\x0f] ok, output: {}".format(
                str(await aexec(self, " ".join(msg)))[:400]
            ),
        )
    except:
        await self.message(chan, "[\x036admin\x0f] exception in eval!")


async def send(self, c, n, m):
    msg = m.split(" ")
    await self.message(msg.pop(0), " ".join(msg))
    await self.message(c, "[\x036admin\x0f] sent")


async def shut(self, c, n, m):
    shared.qtime[c] = time.time() + (60 * 10)
    await self.message(c, "[\x036admin\x0f] Ok, il be back in 10 minutes")


async def schans(self, c, n, m):
    self.chandb.delete()
    for i in self.channels:
        self.chandb.insert(dict(name=i))
    await self.message(c, "[\x036admin\x0f] Ok")


async def addalias(self, c, n, m):
    al = m.split(" ")[0]
    m = m[len(al) + 1 :]  # dont use the list since i want trailing spaces
    if al in self.cmd:
        await self.message(c, "[\x036admin\x0f] no dont overwrite a command dummy")
        return
    self.cmd[al] = Alias(m).alias

    await self.message(c, '[\x036admin\x0f] added "{}" alias for "{}"'.format(al, m))


async def addot(self, c, n, m):
    al = m.split(" ")[0]
    m = m[len(al) + 1 :]  # dont use the list since i want trailing spaces
    if al in shared.rawm:
        await self.message(c, "[\x036admin\x0f] no dont overwrite a command dummy")
        return
    shared.rawm[al] = Ot(m, al).ot

    await self.message(c, '[\x036admin\x0f] added "{}" trigger for "{}"'.format(al, m))


async def addspook(self, c, n, m):
    al = m.split(" ")[0]
    m = m[len(al) + 1 :]  # dont use the list since i want trailing spaces
    if al in shared.rawm:
        await self.message(c, "[\x036admin\x0f] no dont overwrite a command dummy")
        return
    shared.rawm[al] = Spook(m, al).spook

    await self.message(c, '[\x036admin\x0f] added "{}" trigger for "{}"'.format(al, m))


async def addtrigger(self, c, n, m):
    al = m.split(" ")[0]
    m = m[len(al) + 1 :]  # dont use the list since i want trailing spaces
    if al in shared.rawm:
        await self.message(c, "[\x036admin\x0f] no dont overwrite a command dummy")
        return
    shared.rawm[al] = Trigger(m, al).trigger

    await self.message(c, '[\x036admin\x0f] added "{}" trigger for "{}"'.format(al, m))


class Ot:
    def __init__(self, ms, al):
        self.ms = str(ms)
        self.al = str(al)

    async def ot(alself, self, c, n, m):
        if alself.al in m and n != self.nickname:
            asyncio.create_task(
                self.on_privmsg(
                    build("PRIVMSG", [c, alself.ms.format(m)], n + "!spoof@spoof")
                )
            )
            shared.rawm.pop(alself.al)


class Spook:
    def __init__(self, ms, al):
        self.ms = str(ms)
        self.al = str(al)

    async def spook(alself, self, c, n, m):
        if alself.al in m and n != self.nickname:
            asyncio.create_task(self.message(c, alself.ms.format(m)))
            shared.rawm.pop(alself.al)


class Trigger:
    def __init__(self, ms, al):
        self.ms = str(ms)
        self.al = str(al)

    async def trigger(alself, self, c, n, m):
        if alself.al in m:
            asyncio.create_task(
                self.on_privmsg(
                    build("PRIVMSG", [c, alself.ms.format(m)], n + "!spoof@spoof")
                )
            )


class Alias:
    def __init__(self, ms):
        self.ms = str(ms)

    async def alias(alself, self, c, n, m):
        asyncio.create_task(
            self.on_privmsg(
                build("PRIVMSG", [c, alself.ms.format(m)], n + "!spoof@spoof")
            )
        )


commands = {
    "quit": quit,
    "reload": reloadmods,
    "commit": commit,
    "raw": rawcmd,
    "eval": ev,
    "send": send,
    "joins": joins,
    "shut": shut,
    "schans": schans,
    "addalias": addalias,
    "addtrigger": addtrigger,
    "addot": addot,
    "addspook": addspook,
}


@command("admin")
@is_admin
async def adminHandle(self, chan, source, msg):
    msg = msg.split(" ")
    if len(msg) < 1 or not msg[0] in commands:
        await self.message(chan, "[\x036admin\x0f] Invalid command")
        return
    print("[ADMIN MODULE] {} told me to {}!!!".format(source, msg[0]))
    asyncio.create_task(commands[msg.pop(0)](self, chan, source, " ".join(msg)))


async def init(self):
    self.chandb = shared.db["chan"]

    self.admins = ["xfnw"]
    return
    self.cmd["admin"] = adminHandle

    self.help["admin"] = [
        "admin - various bot owner commands (more for subcommands)",
        "sub-commands of admin, for more info do help admin <command>: quit reload commit part join joins eval send",
    ]
    self.help["admin quit"] = ["admin quit <message> - make the bot disconnect", "no"]
    self.help["admin reload"] = [
        "admin reload - reload the modules and configs",
        "nothing to see here",
    ]
    self.help["admin commit"] = [
        "admin commit <action> - oh no (more)",
        "suggested with <3 by khux",
    ]
    self.help["admin part"] = ["admin part <channel> - leave a channel", ":o"]
    self.help["admin join"] = [
        "admin join <channel> - make the bot join a channel",
        "...",
    ]
    self.help["admin joins"] = [
        "admin joins - join more channels",
        "dont reconnect to a bunch of chans when the bots crashing etc",
    ]
    self.help["admin eval"] = [
        "admin eval <command> - absolute power corrupts absolutely",
        "lmao",
    ]
    self.help["admin send"] = [
        "admin send <channel> <message> - send a message",
        "lmao",
    ]
    self.help["admin schans"] = ["admin schans - save the commands to join", ";p;"]
