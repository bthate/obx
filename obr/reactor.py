# This file is placed in the Public Domain.


"reactor"


import queue
import threading
import typing


from .errors  import later
from .events  import Event
from .threads import launch

lock = threading.RLock()


class Reactor:

    def __init__(self):
        self.cbs = {}
        self.queue = queue.Queue()
        self.ready   = threading.Event()
        self.stopped = threading.Event()

    def callback(self, evt) -> None:
        with lock:
            func = self.cbs.get(evt.type, None)
            if func:
                try:
                    evt._thr = launch(func, evt, name=evt.cmd or evt.txt)
                except Exception as ex:
                    later(ex)
                    evt.ready()

    def loop(self) -> None:
        evt = None
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                evt.orig = repr(self)
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                if evt:
                    evt.ready()
                _thread.interrupt_main()
        self.ready.set()

    def poll(self) -> Event:
        return self.queue.get()

    def put(self, evt) -> None:
        self.queue.put(evt)

    def raw(self, txt) -> None:
        raise NotImplementedError("raw")

    def register(self, typ, cbs) -> None:
        self.cbs[typ] = cbs

    def start(self) -> None:
        self.stopped.clear()
        self.ready.clear()
        launch(self.loop)

    def stop(self) -> None:
        self.stopped.set()

    def wait(self) -> None:
        self.ready.wait()


def __dir__():
    return (
        'Reactor',
    )
