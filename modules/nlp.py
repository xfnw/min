from bot import *

import dataset, random, time, re


def get(l, i):
    try:
        if i <= len(l) and i >= 0:
            return l[i]
        else:
            return ""
    except IndexError:
        return ""


async def rec(self, m):
    prew = shared.db["prew"]
    noch = shared.db["noun"]
    beg = shared.db["beg"]
    end = shared.db["end"]

    words = m.split()

    if words[0] == "admin" or len(words) < 2:
        return

    beg.insert(dict(word=words[0]))
    end.insert(dict(word=words[-1]))

    for w in range(len(words)):
        if w > 0:
            prew.insert_ignore(
                dict(
                    pre3=get(words, w - 3),
                    pre2=get(words, w - 2),
                    pre=get(words, w - 1),
                    pro=get(words, w),
                    pro2=get(words, w + 1),
                    pro3=get(words, w + 2),
                ),
                ["id"],
            )
        noch.insert(dict(word=w))


async def getNoun(self, words, c):
    if c in shared.cstate:
        oldnoun = shared.cstate[c]
    else:
        oldnoun = None

    nouns = shared.db["noun"]
    out = {}
    for i in words:
        out[i] = nouns.count(word=i)
    noun = min(out, key=out.get)

    conversation = shared.db["conver"]
    if oldnoun != None:
        print("adding", [oldnoun, noun])
        conversation.insert_ignore(dict(pre=oldnoun, pro=noun), ["id"])

    nextnoun = [i["pro"] for i in conversation.find(pre=noun)]
    print("nextnoun:", nextnoun)
    if len(nextnoun) > 0:
        noun = random.choice(nextnoun)
    shared.cstate[c] = noun
    return noun


async def genOut(self, noun):
    prew = shared.db["prew"]
    beg = shared.db["beg"]
    end = shared.db["end"]
    nouns = shared.db["noun"]
    iter = 0
    coun = 0
    out = [noun]
    while (
        beg.find_one(word=out[0]) is None
        or beg.count(word=out[0]) - 1 > iter * shared.enmul
    ) and iter < shared.maxiter:
        try:
            out = [
                random.choice(list(prew.find(pro=out[0], pro2=out[1], pro3=out[2])))[
                    "pre"
                ]
            ] + out
        except IndexError:
            try:
                out = [
                    random.choice(list(prew.find(pro=out[0], pro2=out[1])))["pre"]
                ] + out
            except IndexError:
                try:
                    out = [random.choice(list(prew.find(pro=out[0])))["pre"]] + out
                except IndexError:
                    iter += 69
        iter += 1
        coun += 1
    iter = 0
    while (
        end.find_one(word=out[-1]) is None
        or end.count(word=out[-1]) - 1 > iter * shared.enmul
    ) and iter < shared.maxiter:
        try:
            out.append(
                random.choice(list(prew.find(pre3=out[-3], pre2=out[-2], pre=out[-1])))[
                    "pro"
                ]
            )
        except IndexError:
            try:
                out.append(
                    random.choice(list(prew.find(pre2=out[-2], pre=out[-1])))["pro"]
                )
            except IndexError:
                try:
                    out.append(random.choice(list(prew.find(pre=out[-1])))["pro"])
                except IndexError:
                    iter += 69
        iter += 1
        coun += 1

    if coun <= 4:
        shared.enmul -= 0.1
    elif coun >= shared.maxiter:
        shared.enmul += 0.1

    return out


async def filter(self, c, n, m):
    if c in shared.qtime and shared.qtime[c] > time.time():
        return
    if m[: len(shared.prefix)] == shared.prefix:
        m = m[len(shared.prefix) :]
        await go(self, c, n, m)
    elif m[: len(self.nickname) + 1] == self.nickname + " ":
        m = m[len(self.nickname) + 1 :]
        await go(self, c, n, m)
    elif "#" not in c and n != self.nickname:
        await go(self, c, n, m)
    else:
        if len(m.split()) > 1:
            if shared.learntime + shared.learndelay < time.time():
                await rec(self, m)
                shared.learntime = time.time()


async def go(self, c, n, m):
    await rec(self, m)
    words = re.sub(r"([\.,\?!])", r" \1", m).split()
    if words[0] == "admin":
        return
    msg = re.sub(
        r" ([\.,\?!])",
        r"\1",
        " ".join(await genOut(self, await getNoun(self, words, c))),
    )
    if msg[-1] == "\x01" and msg[0] != "\x01":
        msg = msg[:-1]
    await self.message(c, msg)


async def init(self):

    shared.qtime = {}
    shared.learntime = 0

    # delay between grabbing random messages and passively
    # learning.
    shared.learndelay = 1
    # sentance ending weight, lower means longer sentances,
    # higher means shorter sentances. this will need to slowly
    # get larger as the database grows
    shared.enmul = 2
    shared.maxiter = 14

    shared.rawm["nlp"] = filter
    shared.cstate = {}
