# This file is placed in the Public Domain.
# pylint: disable=R


"default values"


from . import Object


class Default(Object):

    "Default"

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


class Config(Default):

    "Config"


def __dir__():
    return (
        'Config',
        'Default'
    )
