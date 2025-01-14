# This file is placed in the Public Domain.
# pylint: disable=C,R0903,W0105,W0718


"threading"


import queue
import threading
import time
import traceback
import _thread


class Worker(threading.Thread):

    def __init__(self, func, name, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self.name = name
        self.queue = queue.Queue()
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def run(self):
        while not self.stopped.is_set():
            try:
                func, args = self.queue.get()
                func(*args)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()
            except Exception as ex:
                later(ex)


def launch(func, *args, **kwargs):
    nme = kwargs.get("name", name(func))
    thread = threading.Thread(None, func, nme, args, kwargs)
    thread.start()
    return thread


def name(obj):
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


"errors"


class Errors:

    errors = []

    @staticmethod
    def format(exc):
        return traceback.format_exception(
            type(exc),
            exc,
            exc.__traceback__
        )


def errors():
    for err in Errors.errors:
        for line in err:
            yield line


def later(exc):
    excp = exc.with_traceback(exc.__traceback__)
    fmt = Errors.format(excp)
    if fmt not in Errors.errors:
        Errors.errors.append(fmt)


"interface"


def __dir__():
    return (
        'Errors',
        'Thread',
        'errors',
        'later',
        'launch',
        'name'
    )
