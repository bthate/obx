# This file is placed in the Public Domain.


"pool of threads"


import time


import concurrent.futures as cf


from .command import command
from .errors  import later
from .fleet   import Fleet
from .reactor import Reactor


class Worker(Reactor):

    def loop(self):
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                if evt is None:
                    break
                evt.orig = repr(self)
                command(self, evt)
            except (KeyboardInterrupt, EOFError):
                if "ready" in dir(evt):
                    evt.ready()
                _thread.interrupt_main()


class Pool:

    workers = [Worker()] * 6

    @staticmethod
    def put(evt):
        for worker in Pool.workers:
            if worker.qsize() == 0:
                worker.put(evt)
                return
        worker = Worker()
        worker.put(evt)


class PoolClient(Worker):

    def __init__(self):
        Worker.__init__(self)
        Fleet.add(self)

    def display(self, evt):
        for txt in evt.result:
            self.raw(txt)

    def raw(self, txt):
        raise NotImplementedError("raw")


def __dir__():
    return (
        'submit',
    )
