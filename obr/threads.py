# This file is placed in the Public Domain.


"threads"


import queue
import threading
import time
import typing


from .errors import later
from .events import Event


lock = threading.RLock()


class Thread(threading.Thread):

    def __init__(self, func, thrname, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self.name = thrname
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def run(self) -> None:
        func, args = self.queue.get()
        try:
            self.result = func(*args)
        except Exception as ex:
            later(ex)
            if not args:
                return
            evt = args[0]
            if isinstance(evt, Event):
                evt.ready()

    def join(self, timeout=None) -> typing.Any:
        super().join(timeout)
        return self.result


def launch(func, *args, **kwargs) -> Thread:
    nme = kwargs.get("name", name(func))
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread


def name(obj) -> str:
    typ = type(obj)
    if '__builtins__' in dir(typ):
        return obj.__name__
    if '__self__' in dir(obj):
        return f'{obj.__self__.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj) and '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj):
        return f"{obj.__class__.__module__}.{obj.__class__.__name__}"
    if '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    return None


def __dir__():
    return (
        'Thread',
        'launch',
        'name'
    )
