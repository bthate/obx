# This file is placed in the Public Domain.
# pylint: disable=R,W0621,W0622


"OBX"


import json


class Object:

    "Object"

    def __contains__(self, key):
        return key in dir(self)

    def __getstate__(self):
        "no pickle."

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __oid__(self):
        return 1

    def __str__(self):
        return str(self.__dict__)


def construct(obj, *args, **kwargs):
    "construct an object from provided arguments."
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


def items(obj):
    "return the items of an object."
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    "return keys of an object."
    if isinstance(obj, type({})):
        return obj.keys()
    return list(obj.__dict__.keys())


def match(obj, txt):
    "check if object has matching keys."
    for key in keys(obj):
        if txt in key:
            yield key


def search(obj, selector, match=None):
    "check if object matches provided values."
    res = False
    if not selector:
        return res
    for key, value in items(selector):
        val = getattr(obj, key, None)
        if not val:
            continue
        if match and value == val:
            res = True
        elif str(value).lower() in str(val).lower():
            res = True
        else:
            res = False
            break
    return res


def update(obj, data, empty=True):
    "update an object."
    for key, value in items(data):
        if empty and not value:
            continue
        setattr(obj, key, value)


def values(obj):
    "return values of an object."
    return obj.__dict__.values()


class ObjectDecoder(json.JSONDecoder):

    "ObjectDecoder"

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, _w=None):
        "decoding string to object."
        val = json.JSONDecoder.decode(self, s)
        if not val:
            val = {}
        return hook(val)

    def raw_decode(self, s, idx=0):
        "decode partial string to object."
        return json.JSONDecoder.raw_decode(self, s, idx)


def hook(objdict, typ=None):
    "construct object from dict."
    if typ:
        obj = typ()
    else:
        obj = Object()
    construct(obj, objdict)
    return obj


def load(fpt, *args, **kw):
    "load object from file."
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.load(fpt, *args, **kw)


def loads(string, *args, **kw):
    "load object from string."
    kw["cls"] = ObjectDecoder
    kw["object_hook"] = hook
    return json.loads(string, *args, **kw)


class ObjectEncoder(json.JSONEncoder):

    "ObjectEncoder"

    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, o):
        "return stringable value."
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
            return o
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            try:
                return o.__dict__
            except AttributeError:
                return repr(o)

    def encode(self, o) -> str:
        "encode object to string."
        return json.JSONEncoder.encode(self, o)

    def iterencode(self, o, _one_shot=False):
        "loop over object to encode to string."
        return json.JSONEncoder.iterencode(self, o, _one_shot)


def dump(*args, **kw):
    "dump object to file."
    kw["cls"] = ObjectEncoder
    return json.dump(*args, **kw)


def dumps(*args, **kw):
    "dump object to string."
    kw["cls"] = ObjectEncoder
    return json.dumps(*args, **kw)


def __dir__():
    return (
        'Object',
        'construct',
        'dumps',
        'edit',
        'format',
        'loads',
        'items',
        'keysmatch',
        'keys',
        'match',
        'search',
        'update',
        'values',
    )
