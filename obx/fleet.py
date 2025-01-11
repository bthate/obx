# This file is placed in the Public Domain.
# pylint: disable=C,W0105


"list of bots"


class Fleet:

    bots = {}
    
    @staticmethod
    def add(bot):
        Fleet.bots[repr(bot)] = bot

    @staticmethod
    def get(name):
        return Fleet.bots.get(name, None)


"interface"


def __dir__():
    return (
        'Fleet',
    )
