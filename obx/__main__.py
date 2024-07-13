# This file is placed in the Public Domain.
# pylint: disable=C0413,W0212,W0401,W0614,W0718,E0401,E1121


"main"


import getpass
import os
import pwd
import sys
import readline
import termios
import time


from .face import *


from . import modules
from . import user


if os.path.exists("mods"):
    import mods as MODS
else:
    MODS = None


Cfg         = Config()
Cfg.dis     = ""
Cfg.mod     = "mod,cmd,err,thr"
Cfg.name    = __file__.split(os.sep)[-2]
Cfg.opts    = ""
Cfg.user    = getpass.getuser()
Cfg.wdr     = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wdr, f"{Cfg.name}.pid")


Persist.workdir = Cfg.wdr


class CSL(Console):

    "cSL"

    def announce(self, txt):
        "mask announce"


def daemon(verbose=False):
    "switch to background."
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")


def privileges(username):
    "drop privileges."
    pwnam = pwd.getpwnam(username)
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def wrap(func):
    "catch exceptions"
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    except Exception as ex:
        later(ex)
    errors()


def basic():
    "main"
    enable(print)
    parse(Cfg, " ".join(sys.argv[1:]))
    if "h" in Cfg.opts:
        return cmnd("hlp", print)
    Cfg.dis = Cfg.sets.dis
    Cfg.mod = ",".join(modnames(modules, user))
    scan(Cfg.mod, modules, user)
    return cmnd(Cfg.otxt, print)


def background():
    "main"
    daemon("-v" in sys.argv)
    skel()
    pidfile(Cfg.pidfile)
    privileges(Cfg.user)
    if "-v" in sys.argv:
        enable(print)
    Cfg.mod = ",".join(modnames(modules, user))
    scan(Cfg.mod, modules, user)
    init(Cfg.mod, modules, user)
    forever()


def console(func):
    "reset terminal."
    old3 = None
    try:
        old3 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    finally:
        if old3:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old3)
    errors()


def terminal():
    "main"
    readline.redisplay()
    enable(print)
    skel()
    parse(Cfg, " ".join(sys.argv[1:]))
    Cfg.dis = Cfg.sets.dis
    Cfg.mod += "," + ",".join(modnames(modules, user, MODS))
    if "v" in Cfg.opts:
        dte = " ".join(time.ctime(time.time()).replace("  ", " ").split()[1:])
        mods = ','.join(sorted({x.upper() for x in spl(Cfg.mod)}))
        print(f'{dte} {Cfg.name.upper()} {Cfg.opts.upper()} {mods}'.replace("  ", " "))
    scan(Cfg.mod, modules, user, MODS, Cfg.dis)
    csl = CSL(print, input)
    if "i" in Cfg.opts:
        init(Cfg.mod, modules, user, MODS, Cfg.dis)
    csl.start()
    cmnd(Cfg.otxt, print)
    forever()


def wrapped():
    "starting point."
    if len(sys.argv) < 2:
        return
    if "-d" in sys.argv[1]:
        background()
    elif "-h" in sys.argv[1]:
        cmnd("hlp", print)
    elif "-c" in sys.argv[1]:
        console(terminal)
    else:
        wrap(basic)


if __name__ == "__main__":
    wrapped()
