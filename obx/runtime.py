# This file is placed in the Public Domain.
# pylint: disable=R,W0718,E1102


"runtime"


import queue
import threading
import time
import traceback
import types
import _thread


NAME      = __file__.rsplit("/", maxsplit=2)[-2]
STARTTIME = time.time()
VERBOSE   = None


class Broker:

    "Broker"

    objs = {}

    @staticmethod
    def add(obj):
        "add object."
        Broker.objs[repr(obj)] = obj

    @staticmethod
    def all(kind=None):
        "return all objects."
        if kind is not None:
            for key in [x for x in Broker.objs if kind in x]:
                yield Broker.get(key)
        return Broker.objs.values()

    @staticmethod
    def get(orig):
        "return object by matching repr."
        return Broker.objs.get(orig)


class Errors:

    "Errors"

    errors = []


def fmat(exc):
    "format an exception"
    return traceback.format_exception(
                               type(exc),
                               exc,
                               exc.__traceback__
                              )


def errors(outer):
    "display errors."
    for exc in Errors.errors:
        for line in exc:
            outer(line.strip())


def later(exc, evt=None):
    "add an exception"
    excp = exc.with_traceback(exc.__traceback__)
    fmt = fmat(excp)
    if fmt not in Errors.errors:
        Errors.errors.append(fmt)


class Logging:

    "Logging"

    filter = []


Logging.filter = ["PING", "PONG", "PRIVMSG"]


def debug(txt):
    "print to console."
    for skp in Logging.filter:
        if skp in txt:
            return
    if VERBOSE:
        VERBOSE(txt)


class Reactor:

    "Reactor"

    def __init__(self):
        self.cbs      = {}
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()

    def callback(self, evt):
        "call callback based on event type."
        func = self.cbs.get(evt.type, None)
        if func:
            launch(func, self, evt)

    def loop(self):
        "proces events until interrupted."
        while not self.stopped.is_set():
            evt = self.poll()
            self.callback(evt)

    def poll(self):
        "function to return event."
        return self.queue.get()

    def put(self, evt):
        "put event into the queue."
        self.queue.put_nowait(evt)

    def register(self, typ, cbs):
        "register callback for a type."
        self.cbs[typ] = cbs

    def start(self):
        "start the event loop."
        launch(self.loop)

    def stop(self):
        "stop the event loop."
        self.stopped.set()

    def wait(self):
        "wait till empty queue."
        while not self.stopped.is_set():
            if not self.queue.qsize():
                break


class Client(Reactor):

    "Client"

    def __init__(self):
        Reactor.__init__(self)
        Broker.add(self)

    def display(self, evt):
        "show results into a channel."
        for txt in evt.result:
            self.say(evt.channel, txt)

    def say(self, _channel, txt):
        "echo on verbose."
        self.raw(txt)

    def raw(self, txt):
        "print to screen."
        raise NotImplementedError


class Thread(threading.Thread):

    "Thread"

    def __init__(self, func, thrname, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self.name      = thrname
        self.queue     = queue.Queue()
        self.result    = None
        self.sleep     = None
        self.starttime = time.time()
        self.queue.put_nowait((func, args))

    def __contains__(self, key):
        return key in self.__dict__

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def size(self):
        "return qsize"
        return self.queue.qsize()

    def join(self, timeout=None):
        "join this thread."
        super().join(timeout)
        return self.result

    def run(self):
        "run this thread's payload."
        func, args = self.queue.get()
        self.result = func(*args)


class Timer:

    "Timer"

    def __init__(self, sleep, func, *args, thrname=None):
        self.args  = args
        self.func  = func
        self.sleep = sleep
        self.name  = thrname or named(func)
        self.state = {}
        self.timer = None

    def run(self):
        "run the payload in a thread."
        self.state["latest"] = time.time()
        launch(self.func, *self.args)

    def start(self):
        "start timer."
        timer = threading.Timer(self.sleep, self.run)
        timer.name   = self.name
        timer.daemon = True
        timer.sleep  = self.sleep
        timer.state  = self.state
        timer.func   = self.func
        timer.state["starttime"] = time.time()
        timer.state["latest"]    = time.time()
        timer.start()
        self.timer   = timer

    def stop(self):
        "stop timer."
        if self.timer:
            self.timer.cancel()


class Repeater(Timer):

    "Repeater"

    def run(self):
        launch(self.start)
        super().run()


def forever():
    "it doesn't stop, until ctrl-c"
    while True:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def init(*pkgs):
    "scan modules for commands and classes"
    mods = []
    for pkg in pkgs:
        for modname in modnames(pkg):
            modi = getattr(pkg, modname)
            if "init" not in dir(modi):
                continue
            thr = launch(modi.init)
            mods.append((modi, thr))
    return mods


def launch(func, *args, **kwargs):
    "launch a thread."
    name = kwargs.get("name", named(func))
    thread = Thread(func, name, *args, **kwargs)
    thread.start()
    return thread


def modnames(*args):
    "return module names."
    res = []
    for arg in args:
        res.extend([x for x in dir(arg) if not x.startswith("__")])
    return sorted(res)


def named(obj):
    "return a full qualified name of an object/function/module."
    if isinstance(obj, types.ModuleType):
        return obj.__name__
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


def wrap(func, outer):
    "reset console."
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        outer("")
    except Exception as ex:
        later(ex)


def __dir__():
    return (
        'Broker',
        'Client',
        'Errors',
        'Reactor',
        'Repeater',
        'Thread',
        'Timer',
        'debug',
        'forever',
        'errors',
        'init',
        'later',
        'launch',
        'modnames',
        'named',
        'wait'
    )
