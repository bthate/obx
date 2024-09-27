# This file is placed in the Public Domain.


"running threads."


import threading
import time


from .. import Object, update


from ..command import Commands
from ..persist import laps
from ..runtime import STARTTIME


def thr(event):
    "list threads."
    result = []
    for thread in sorted(threading.enumerate(), key=lambda x: x.name):
        if str(thread).startswith('<_'):
            continue
        obj = Object()
        update(obj, vars(thread))
        if getattr(obj, 'current', None):
            thread.name = obj.current
        if getattr(obj, 'sleep', None):
            uptime = obj.sleep - int(time.time() - obj.state["latest"])
        elif getattr(obj, 'starttime', None):
            uptime = int(time.time() - obj.starttime)
        else:
            uptime = int(time.time() - STARTTIME)
        result.append((uptime, thread.name))
    res = []
    for uptime, txt in sorted(result, key=lambda x: x[1]):
        lap = laps(uptime)
        res.append(f'{txt}/{lap}')
    if res:
        event.reply(' '.join(res))
    else:
        event.reply('no threads')


Commands.add(thr)
