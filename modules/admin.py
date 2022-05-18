import importlib, time, asyncio, random, sys
from bot import *

quitmessages = [
    "time to die",
    "you can hide, but you can not run!",
    "you're next",
    "bye",
    "the balun has been popped.",
]


async def commit(self, chan, source, msg):
    await self.send(build("QUIT", [f"{source} told me to commit {msg}!"]))
    sys.exit()


async def quit(self, chan, source, msg):
    await self.send(build("QUIT", [random.choice(quitmessages)]))
    sys.exit()


async def reloadmods(self, chan, source, msg):
    await self.message(chan, "reloading modules...")
    shared.oldcmd = shared.commands
    shared.commands = {}
    shared.rawm = {}
    shared.listeners = []
    shared.help = {}
    try:
        for i in shared.modules:
            importlib.reload(shared.modules[i])
            await shared.modules[i].init(self)
            # await self.message(chan, 'load {} sucess!'.format(i))
        await self.message(
            chan, "done! {} modules reloaded!".format(len(shared.modules))
        )
    except:
        await self.message(
            chan, "reload failed... {}...".format(repr(sys.exc_info()[1]))
        )
        shared.commands = shared.oldcmd


async def rawcmd(self, chan, source, msg):
    await self.send_raw(msg)


async def joins(self, chan, source, msg):
    await self.message(chan, "joining slowly as to not flood...")
    for i in self.chandb.all():
        await self.send(build("JOIN", [i["name"]]))
        await asyncio.sleep(1)
        print("joined {}".format(i["name"]))
    await self.message(
        chan,
        "Sucess! i may be laggy for a bit while i sort through all these channels...",
    )


async def aexec(self, code, chan=None, source=None, msg=None):
    # Make an async function with the code and `exec` it
    exec(
        f"async def __ex(self, chan, source, msg): "
        + "".join(f"\n {l}" for l in code.split("\\n"))
    )

    # Get `__ex` from local variables, call it and return the result
    return await locals()["__ex"](self, chan, source, msg)


async def ev(self, chan, source, msg):
    msg = msg.split(" ")
    try:
        await self.message(
            chan, "ok, output: {}".format(str(await aexec(self, " ".join(msg)))[:400])
        )
    except:
        await self.message(chan, "ut oh! {}".format(repr(sys.exc_info()[1])))


async def send(self, c, n, m):
    msg = m.split(" ")
    await self.message(msg.pop(0), " ".join(msg))
    await self.message(c, "sent")


async def shut(self, c, n, m):
    shared.qtime[c] = time.time() + (60 * 10)
    await self.message(c, "Ok, il be back in 10 minutes")


async def deleteword(self, c, n, m):
    starttime = time.time()
    deleteme = m.split()
    shared.db["conver"].delete(pre=deleteme)
    shared.db["prew"].delete(pre=deleteme)
    shared.db["conver"].delete(pro=deleteme)
    shared.db["prew"].delete(pro=deleteme)
    shared.db["noun"].delete(word=deleteme)
    shared.db["beg"].delete(word=deleteme)
    shared.db["end"].delete(word=deleteme)
    await self.message(
        c, f"word(s) deleted in {round(time.time()-starttime,2)} seconds"
    )


async def schans(self, c, n, m):
    self.chandb.delete()
    for i in self.channels:
        self.chandb.insert(dict(name=i))
    await self.message(c, "Ok")


async def addalias(self, c, n, m):
    al = m.split(" ")[0]
    m = m[len(al) + 1 :]  # dont use the list since i want trailing spaces
    Alias(al, m)

    await self.message(c, 'added "{}" alias for "{}"'.format(al, m))


async def addcommand(self, c, n, m):
    al = m.split(" ")[0]
    m = m[len(al) + 1 :]  # dont use the list since i want trailing spaces
    Command(al, m)

    await self.message(c, 'added "{}" alias for "{}"'.format(al, m))


async def addot(self, c, n, m):
    al = m.split(" ")[0]
    m = m[len(al) + 1 :]  # dont use the list since i want trailing spaces
    if al in shared.rawm:
        await self.message(c, "no dont overwrite a command dummy")
        return
    Ot(al, m)

    await self.message(c, 'added "{}" trigger for "{}"'.format(al, m))


async def addspook(self, c, n, m):
    al = m.split(" ")[0]
    m = m[len(al) + 1 :]  # dont use the list since i want trailing spaces
    if al in shared.rawm:
        await self.message(c, "no dont overwrite a command dummy")
        return
    Spook(al, m)

    await self.message(c, 'added "{}" trigger for "{}"'.format(al, m))


async def addtrigger(self, c, n, m):
    al = m.split(" ")[0]
    m = m[len(al) + 1 :]  # dont use the list since i want trailing spaces
    if al in shared.rawm:
        await self.message(c, "no dont overwrite a command dummy")
        return
    Trigger(al, m)

    await self.message(c, 'added "{}" trigger for "{}"'.format(al, m))


class Ot:

    ots = {}

    def __init__(self, al, ms):
        self.ms = str(ms)
        self.al = str(al)
        self.__class__.ots[self.al] = ms
        shared.rawm[self.al] = self.ot

    async def ot(alself, self, c, n, m):
        if alself.al in m and n != self.nickname:
            asyncio.create_task(
                self.on_privmsg(
                    build("PRIVMSG", [c, alself.ms.format(m)], n + "!spoof@spoof")
                )
            )
            shared.rawm.pop(alself.al)


class Spook:

    spooks = {}

    def __init__(self, al, ms):
        self.ms = str(ms)
        self.al = str(al)
        self.__class__.spooks[self.al] = ms
        shared.rawm[self.al] = self.spook

    async def spook(alself, self, c, n, m):
        if alself.al in m and n != self.nickname:
            self.send(build("PRIVMSG", [c, alself.ms.format(m)]))
            shared.rawm.pop(alself.al)


class Trigger:

    triggers = {}

    def __init__(self, al, ms):
        self.ms = str(ms)
        self.al = str(al)
        self.__class__.triggers[al] = ms
        shared.rawm[al] = self.trigger

    async def trigger(alself, self, c, n, m):
        if alself.al in m:
            asyncio.create_task(
                self.on_privmsg(
                    build("PRIVMSG", [c, alself.ms.format(m)], n + "!spoof@spoof")
                )
            )


class Command:

    commands = {}

    def __init__(self, cmd, ms):
        self.ms = str(ms)
        self.__class__.commands[cmd] = ms
        shared.commands[cmd] = self.command

    async def command(alself, self, chan, source, msg):
        try:
            out = await aexec(self, alself.ms, chan, source, msg)
        except:
            await self.message(chan, "ut oh! {}".format(repr(sys.exc_info()[1])))
        else:
            if out is not None and len(out) > 0:
                await self.message(chan, str(out))


class Alias:

    aliases = {}

    def __init__(self, cmd, ms):
        self.ms = str(ms)
        self.__class__.aliases[cmd] = ms
        shared.commands[cmd] = self.alias

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
    "deleteword": deleteword,
    "schans": schans,
    "addalias": addalias,
    "addcommand": addcommand,
    "addtrigger": addtrigger,
    "addot": addot,
    "addspook": addspook,
}


@command("admin")
@is_admin
async def adminHandle(self, chan, source, msg):
    msg = msg.split(" ")
    if len(msg) < 1 or not msg[0] in commands:
        await self.message(chan, "Invalid command")
        return
    print("[ADMIN MODULE] {} told me to {}!!!".format(source, msg[0]))
    asyncio.create_task(commands[msg.pop(0)](self, chan, source, " ".join(msg)))


async def init(self):
    self.chandb = shared.db["chan"]

    self.admins = ["xfnw"]
    return

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
