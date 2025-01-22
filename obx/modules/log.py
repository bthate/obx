# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903


"log text"


import time


from obx.objects import Object
from obx.persist import elapsed, find, fntime, ident, store, write


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


def log(event):
    if not event.rest:
        nmr = 0
        for fnm, obj in find('log'):
            lap = elapsed(time.time() - fntime(fnm))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply('no log')
        return
    obj = Log()
    obj.txt = event.rest
    write(obj)
    event.ok()
