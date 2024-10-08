# This file is placed in the Public Domain.
# pylint: disable=R,W0105


"persistence"


import datetime
import json
import os
import pathlib
import time
import _thread


from .        import dump, load, update
from .default import Default
from .method  import search


lock     = _thread.allocate_lock()
disklock = _thread.allocate_lock()
p        = os.path.join


class ReadError(Exception):
    "error reading json file."


"workdir"


class Workdir:

    "Workdir"

    fqns = []
    name = Default.__module__.split(".", maxsplit=2)[-1]
    wdr = os.path.expanduser(f"~/.{name}")


def long(name):
    "match from single name to long name."
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def pidname():
    "return pidfile path."
    return os.path.join(Workdir.wdr, f"{Workdir.name}.pid")


def skel():
    "create directory,"
    stor = p(Workdir.wdr, "store", "")
    path = pathlib.Path(stor)
    path.mkdir(parents=True, exist_ok=True)
    return path


def store(pth=""):
    "return objects directory."
    stor = p(Workdir.wdr, "store", "")
    if not os.path.exists(stor):
        skel()
    return p(Workdir.wdr, "store", pth)


def types():
    "return types stored."
    return os.listdir(store())


def whitelist(clz):
    "whitelist classes."
    Workdir.fqns.append(fqn(clz))


"utilitites"


def cdir(pth):
    "create directory."
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def ident(obj):
    "return an id for an object."
    return p(fqn(obj), *str(datetime.datetime.now()).split())


def find(mtc, selector=None, index=None, deleted=False, matching=False):
    "find object matching the selector dict."
    clz = long(mtc)
    nrs = -1
    for fnm in sorted(fns(clz), key=fntime):
        obj = Default()
        fetch(obj, fnm)
        if not deleted and '__deleted__' in obj and obj.__deleted__:
            continue
        if selector and not search(obj, selector, matching):
            continue
        nrs += 1
        if index is not None and nrs != int(index):
            continue
        yield (fnm, obj)


def fns(mtc=""):
    "show list of files."
    dname = ''
    pth = store(mtc)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            for dname in sorted(dirs):
                if dname.count('-') == 2:
                    ddd = p(rootdir, dname)
                    for fll in os.scandir(ddd):
                        yield strip(p(ddd, fll))


def fntime(daystr):
    "convert file name to it's saved time."
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return timed


def fqn(obj):
    "return full qualified name of an object."
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def laps(seconds, short=True):
    "show elapsed time."
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    yea = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    yeas = int(nsec/yea)
    nsec -= yeas*yea
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    nsec -= int(minute*minutes)
    sec = int(nsec)
    if yeas:
        txt += f"{yeas}y"
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += f"{nrdays}d"
    if short and txt:
        return txt.strip()
    if hours:
        txt += f"{hours}h"
    if minutes:
        txt += f"{minutes}m"
    if sec:
        txt += f"{sec}s"
    txt = txt.strip()
    return txt


def strip(pth, nmr=3):
    "reduce to path with directory."
    return os.sep.join(pth.split(os.sep)[-nmr:])


"methods"


def fetch(obj, pth):
    "read object from disk."
    with disklock:
        pth2 = store(pth)
        read(obj, pth2)
        return os.sep.join(pth.split(os.sep)[-3:])


def last(obj, selector=None):
    "return last object saved."
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    res = None
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        res = inp[0]
    return res


def read(obj, pth):
    "read an object from file path."
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            try:
                update(obj, load(ofile))
            except json.decoder.JSONDecodeError as ex:
                raise ReadError(pth) from ex


def sync(obj, pth=None):
    "sync object to disk."
    if pth is None:
        pth = ident(obj)
    with disklock:
        pth2 = store(pth)
        write(obj, pth2)
        return pth


def write(obj, pth):
    "write an object to disk."
    with lock:
        cdir(pth)
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile, indent=4)


"interface"


def __dir__():
    return (
        'ReadError',
        'Workdir',
        'find',
        'fns',
        'fetch',
        'last',
        'laps',
        'long',
        'pidname',
        'read',
        'skel',
        'store',
        'sync',
        'types',
        'whitelist',
        'write'
    )
