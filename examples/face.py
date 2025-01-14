# This file is placed in the Public Domain.
# pylint: disable=W0105,W0611,E0402
# ruff: noqa: F401


"interface"


from . import irc, opm, rss


"teh dir"


def __dir__():
    return (
        'irc',
        'opm',
        'rss'
    )


__all__ = __dir__()
