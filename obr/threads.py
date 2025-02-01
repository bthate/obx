# This file is placed in the Public Domain.


"threads"


import queue
import threading
import time
import typing
import traceback


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
            try:
                args[0].ready()
            except (AttributeError, IndexError):
                pass

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


class Timer:

    def __init__(self, sleep, func, *args, thrname=None, **kwargs):
        self.args   = args
        self.func   = func
        self.kwargs = kwargs
        self.sleep  = sleep
        self.name   = thrname or kwargs.get("name", name(func))
        self.state  = {}
        self.timer  = None

    def run(self) -> None:
        self.state["latest"] = time.time()
        launch(self.func, *self.args)

    def start(self) -> None:
        timer = threading.Timer(self.sleep, self.run)
        timer.name   = self.name
        timer.sleep  = self.sleep
        timer.state  = self.state
        timer.func   = self.func
        timer.state["starttime"] = time.time()
        timer.state["latest"]    = time.time()
        timer.start()
        self.timer   = timer

    def stop(self) -> None:
        if self.timer:
            self.timer.cancel()


class Repeater(Timer):

    def run(self) -> None:
        launch(self.start)
        super().run()


class Errors:

    name = __file__.rsplit(".", maxsplit=2)[-2]
    errors = []

    @staticmethod
    def format(exc) -> str:
        exctype, excvalue, trb = type(exc), exc, exc.__traceback__
        trace = traceback.extract_tb(trb)
        result = ""
        for i in trace:
            fname = i[0]
            linenr = i[1]
            plugfile = fname[:-3].split("/")
            mod = []
            for i in plugfile[::-1]:
                mod.append(i)
                if i in ['obx', 'obr']:
                    break
            ownname = '.'.join(mod[::-1])
            if ownname.endswith("__"):
                continue
            if ownname.startswith("<"):
                continue
            result += f"{ownname}:{linenr} "
        del trace
        res = f"{exctype} {result[:-1]} {excvalue}"
        return res

    @staticmethod
    def full(exc) -> str:
        return traceback.format_exception(
            type(exc),
            exc,
            exc.__traceback__
        )


def errors() -> []:
    return Errors.errors


def later(exc) -> None:
    excp = exc.with_traceback(exc.__traceback__)
    fmt = Errors.format(excp)
    if fmt not in Errors.errors:
        Errors.errors.append(fmt)


def __dir__():
    return (
        'Errors',
        'Repeater',
        'Thread',
        'Timer',
        'errors',
        'later',
        'launch',
        'name'
    )
