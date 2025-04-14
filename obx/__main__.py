# This file is placed in the Public Domain.


"main program"


import os
import pathlib
import sys
import time
import _thread


from .client  import Client
from .handler import Event
from .json    import dumps
from .modules import Commands, Main, command, inits, md5sum
from .modules import mods, modules, parse, scan, settable
from .store   import Workdir, pidname
from .thread  import Errors, full


class CLI(Client):

    def __init__(self):
        Client.__init__(self)
        self.register("command", command)

    def raw(self, txt):
        output(txt.encode('utf-8', 'replace').decode("utf-8"))


class Console(CLI):

    def announce(self, txt):
        pass

    def callback(self, evt):
        CLI.callback(self, evt)
        evt.wait()

    def poll(self):
        evt = Event()
        evt.txt = input("> ")
        evt.type = "command"
        return evt


"output"


def doprint(txt):
    print(txt.rstrip())
    sys.stdout.flush()


def output(txt):
    doprint(txt)


def nil(txt):
    pass


def enable():
    global output
    output = doprint


def disable():
    global output
    output = nil


"signals"


def handler(signum, frame):
    _thread.interrupt_main()


"utilities"


def banner():
    tme = time.ctime(time.time()).replace("  ", " ")
    output(f"{Main.name.upper()} since {tme}")


def check(txt):
    args = sys.argv[1:]
    for arg in args:
        if not arg.startswith("-"):
            continue
        for char in txt:
            if char in arg:
                return True
    return False


def daemon(verbose=False):
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
    os.nice(10)


def errors():
    for exc in Errors.errors:
        for line in full(exc):
            output(line)


def forever():
    while True:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def nodebug():
    with open('/dev/null', 'a+', encoding="utf-8") as ses:
        os.dup2(ses.fileno(), sys.stderr.fileno())


def pidfile(filename):
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def privileges():
    import getpass
    import pwd
    pwnam2 = pwd.getpwnam(getpass.getuser())
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)


def setwd(name, path=""):
    Main.name = name
    path = path or os.path.expanduser(f"~/.{name}")
    Workdir.wdr = path


"commands"


def cmd(event):
    event.reply(",".join(sorted([x for x in Commands.names if x not in Main.ignore])))


def md5(event):
    table = mods("tbl")[0]
    event.reply(md5sum(table.__file__))


def srv(event):
    import getpass
    name = getpass.getuser()
    event.reply(TXT % (Main.name.upper(), name, name, name, Main.name))


def tbl(event):
    if not check("f"):
        Commands.names = {}
    for mod in mods(empty=True):
        scan(mod)
    event.reply("# This file is placed in the Public Domain.")
    event.reply("")
    event.reply("")
    event.reply('"lookup tables"')
    event.reply("")
    event.reply("")
    event.reply(f"NAMES = {dumps(Commands.names, indent=4, sort_keys=True)}")
    event.reply("")
    event.reply("")
    event.reply("MD5 = {")
    for mod in mods():
        event.reply(f'    "{mod.__name__.split(".")[-1]}": "{md5sum(mod.__file__)}",')
    event.reply("}")


"scripts"


def background():
    daemon("-v" in sys.argv)
    setwd(Main.name)
    privileges()
    disable()
    pidfile(pidname(Main.name))
    settable()
    Commands.add(cmd)
    inits(Main.init or "irc,rss")
    forever()


def console():
    import readline # noqa: F401
    setwd(Main.name)
    enable()
    settable()
    Commands.add(cmd)
    parse(Main, " ".join(sys.argv[1:]))
    Main.init = Main.sets.init or Main.init
    Main.verbose = Main.sets.verbose or Main.verbose
    if "v" in Main.opts:
        banner()
    for _mod, thr in inits(Main.init):
        if "w" in Main.opts:
            thr.join()
    csl = Console()
    csl.start()
    forever()


def control():
    if len(sys.argv) == 1:
        return
    setwd(Main.name)
    settable()
    enable()
    Commands.add(cmd)
    Commands.add(md5)
    Commands.add(srv)
    Commands.add(tbl)
    parse(Main, " ".join(sys.argv[1:]))
    csl = CLI()
    evt = Event()
    evt.orig = repr(csl)
    evt.type = "command"
    evt.txt = Main.otxt
    command(evt)
    evt.wait()


def service():
    setwd(Main.name)
    settable()
    nodebug()
    enable()
    banner()
    privileges()
    pidfile(pidname(Main.name))
    Commands.add(cmd)
    inits(Main.init or "irc,rss")
    forever()



"runtime"


def wrapped(func):
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        output("")
    errors()


def wrap(func):
    import termios
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        wrapped(func)
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def main():
    if check("a"):
        Main.ignore = "udp"
        Main.init   = ",".join(modules())
        for mod in mods():
            mod.DEBUG = False
    if check("v"):
        setattr(Main.opts, "v", True)
        enable()
    if check("c"):
        wrap(console)
    elif check("d"):
        background()
    elif check("s"):
        wrapped(service)
    else:
        wrapped(control)


"data"


TXT = """[Unit]
Description=%s
After=network-online.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""


"main"


if __name__ == "__main__":
    main()
