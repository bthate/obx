# This file is placed in the Public Domain.


"NIXT"


from .disk   import read,write
from .json   import dumps, loads
from .object import Object as Object
from .object import construct, items, keys, update, values


__all__ = (
        'Object',
        'construct',
        'dumps',
        'items',
        'keys',
        'loads',
        'read',
        'update',
        'values',
        'write'
    )


def __dir__():
   return __all__
