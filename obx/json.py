# This file is placed in the Public Domain.


"decoder/encoder"


import json


from .object import Object, construct


class Decoder(json.JSONDecoder):

    """ Object decoder """

    def decode(self, s, _w=None) -> Object:
        val = json.JSONDecoder.decode(self, s)
        if isinstance(val, dict):
            return hook(val)
        return val


class Encoder(json.JSONEncoder):

    """ Object Encoder """

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


"utilities"


def dump(*args, **kw) -> None:
    "dump an object"
    kw["cls"] = Encoder
    json.dump(*args, **kw)


def dumps(*args, **kw) -> str:
    "dump object to string"
    kw["cls"] = Encoder
    return json.dumps(*args, **kw)


def hook(objdict) -> Object:
    "convert dict to object"
    obj = Object()
    construct(obj, objdict)
    return obj


def load(*args, **kw) -> Object:
    "load and object from path"
    kw["cls"] = Decoder
    kw["object_hook"] = hook
    return json.load(*args, **kw)


def loads(*args, **kw) -> Object:
    "load an object from string"
    kw["cls"] = Decoder
    kw["object_hook"] = hook
    return json.loads(*args, **kw)


"interface"


def __dir__():
    return (
        'dump',
        'dumps',
        'hook',
        'load',
        'loads'
    )
