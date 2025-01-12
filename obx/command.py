# This file is placed in the Public Domain.
# pylint: disable=C,W0105,E0402


"commands"


import inspect
import types
import _thread


from .parse  import parse
from .thread import launch


lock = _thread.allocate_lock()


class Commands:

    cmds = {}

    @staticmethod
    def add(func):
        Commands.cmds[func.__name__] = func

    @staticmethod
    def scan(mod):
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmdz.__code__.co_varnames:
                Commands.add(cmdz)


"callbacks"


def command(bot, evt):
    #with lock:
    if True:
        parse(evt)
        func = Commands.cmds.get(evt.cmd, None)
        if func:
            func(evt)
        bot.display(evt)
        evt.ready()


"utilities"


def modloop(*pkgs, disable=""):
    for pkg in pkgs:
        for modname in dir(pkg):
            if modname in spl(disable):
                continue
            if modname.startswith("__"):
                continue
            yield getattr(pkg, modname)


def scan(*pkgs, init=False, disable=""):
    result = []
    for mod in modloop(*pkgs, disable=disable):
        if type(mod) is not types.ModuleType:
            continue
        Commands.scan(mod)
        thr = None
        if init and "init" in dir(mod):
            thr = launch(mod.init)
        result.append((mod, thr))
    return result


def spl(txt):
    try:
        result = txt.split(',')
    except (TypeError, ValueError):
        result = txt
    return [x for x in result if x]


"interface"


def __dir__():
    return (
        'Commands',
        'command',
        'scan'
    )
