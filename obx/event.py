# This file is placed in the Public Domain.
# pylint: disable=C,W0105,E0402


"event"


import threading
import time


from .object import Obj


class Event(Obj):

    def __init__(self):
        Obj.__init__(self)
        self._ex    = None
        self._ready = threading.Event()
        self._thr   = None
        self.ctime  = time.time()
        self.result = []
        self.type   = "event"
        self.txt    = ""

    def ok(self):
        self.reply("ok")

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append((txt, time.time()))

    def wait(self):
        self._ready.wait()
        if self._thr:
            self._thr.join()


"interface"


def __dir__():
    return (
        'Event',
    )
