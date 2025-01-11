# This file is placed in the Public Domain.


"pool of threads"


import time


import concurrent.futures as cf


from .command import command
from .errors  import later
from .fleet   import Fleet
from .reactor import Reactor


class Pool(Reactor):

    def callback(self, evt):
        func = self.cbs.get(evt.type, None)
        if func:
            try:
                submit(func, self, evt)
            except Exception as ex:
                evt._ex = ex
                later(ex)
                evt.ready()


def submit(func, *args, **kwargs):
    with cf.ThreadPoolExecutor(max_workers=5) as executor:
        try:
            future = executor.submit(func, *args, **kwargs)
            future.result()
        except Exception as ex:
            later(ex)


class PoolClient(Pool):

    def __init__(self):
        Pool.__init__(self)
        Fleet.add(self)
        self.register("command", command)

    def display(self, evt):
        for txt in evt.result:
            self.raw(txt)

    def raw(self, txt):
        raise NotImplementedError("raw")


def __dir__():
    return (
        'submit',
    )
