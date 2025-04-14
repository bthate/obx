# This file is placed in the Public Domain.


"a clean namespace"


import json


class Object:

    def __contains__(self, key):
        return key in dir(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


def construct(obj, *args, **kwargs) -> None:
    if args:
        val = args[0]
        if isinstance(val, zip):
            update(obj, dict(val))
        elif isinstance(val, dict):
            update(obj, val)
        elif isinstance(val, Object):
            update(obj, vars(val))
    if kwargs:
        update(obj, kwargs)


def items(obj) -> []:
    if isinstance(obj,type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj) -> [str]:
    if isinstance(obj, type({})):
        return obj.keys()
    return list(obj.__dict__.keys())


def update(obj, data) -> None:
    if not isinstance(data, type({})):
        obj.__dict__.update(vars(data))
    else:
        obj.__dict__.update(data)


def values(obj) -> []:
    return obj.__dict__.values()


"decoder/encoder"


class Decoder(json.JSONDecoder):

    def decode(self, s, _w=None) -> Object:
        val = json.JSONDecoder.decode(self, s)
        if isinstance(val, dict):
            return hook(val)
        return val


class Encoder(json.JSONEncoder):

    def default(self, o) -> str:
        if isinstance(o, dict):
            return o.items()
        if issubclass(type(o), Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            try:
                return vars(o)
            except TypeError:
                return repr(o)


def dump(*args, **kw) -> None:
    kw["cls"] = Encoder
    json.dump(*args, **kw)


def dumps(*args, **kw) -> str:
    kw["cls"] = Encoder
    return json.dumps(*args, **kw)


def hook(objdict) -> Object:
    obj = Object()
    construct(obj, objdict)
    return obj


def load(*args, **kw) -> Object:
    kw["cls"] = Decoder
    kw["object_hook"] = hook
    return json.load(*args, **kw)


def loads(*args, **kw) -> Object:
    kw["cls"] = Decoder
    kw["object_hook"] = hook
    return json.loads(*args, **kw)


"interface"


def __dir__():
    return (
        'Object'
        'construct',
        'dump',
        'dumps',
        'hook',
        'items',
        'keys',
        'load',
        'loads',
        'values',
        'update'
    )
