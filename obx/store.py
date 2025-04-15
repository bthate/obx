# This file is placed in the Public Domain.


"object store"


def cdir(pth) -> None:
    "create directory."
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def fqn(obj) -> str:
    "full qualifies name."
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = f"{obj.__module__}.{obj.__name__}"
    return kin


def getpath(obj):
    "return idented path."
    return j(store(ident(obj)))


def ident(obj) -> str:
    "mix full qualified name and a time stamp into a path."
    return j(fqn(obj),*str(datetime.datetime.now()).split())


def last(obj, selector=None) -> Object:
    "last object saved." 
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


def read(obj, pth) -> str:
    "read object from path."
    with lock:
        with open(pth, "r", encoding="utf-8") as fpt:
            try:
                update(obj, load(fpt))
            except json.decoder.JSONDecodeError as ex:
                raise Error(pth) from ex
    return pth


def search(obj, selector, matching=None) -> bool:
    "search an object if it matches key,value dict."
    res = False
    if not selector:
        return res
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if not val:
            continue
        if matching and value == val:
            res = True
        elif str(value).lower() in str(val).lower() or value == "match":
            res = True
        else:
            res = False
            break
    return res


def write(obj, pth=None) -> str:
    "write object to store, empty pth uses an idented path."
    with lock:
        if pth is None:
            pth = store(ident(obj))
        cdir(pth)
        with open(pth, "w", encoding="utf-8") as fpt:
            dump(obj, fpt, indent=4)
        return pth


def __dir__():
    return (
        'cdir',
        'fqn',
        'getpath',
        'ident',
        'last',
        'long',
        'read',
        'search',
        'write'
    )
