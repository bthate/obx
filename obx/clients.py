# This file is placed in the Public Domain.
# pylint: disable=C,R0903,W0105,W0612,E0402


"client"


import queue
import threading


from .command import command
from .objects import Default
from .reactor import Reactor
from .threads import launch


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        Fleet.add(self)
        self.register("command", command)

    def display(self, evt):
        for txt in evt.result:
            self.raw(txt)

    def raw(self, txt):
        raise NotImplementedError("raw")


"config"


class Config(Default):

    name = Default.__module__.split(".")[0]


"fleet"


class Fleet:

    bots = {}

    @staticmethod
    def add(bot):
        Fleet.bots[repr(bot)] = bot

    @staticmethod
    def announce(txt):
        for bot in Fleet.bots:
            bot.announce(txt)

    @staticmethod
    def get(name):
        return Fleet.bots.get(name, None)


"output"


class Output:

    cache = {}

    def __init__(self):
        self.oqueue = queue.Queue()
        self.dostop = threading.Event()

    def display(self, evt):
        for txt in evt.result:
            self.oput(evt.channel, txt)

    def dosay(self, channel, txt):
        raise NotImplementedError("dosay")

    def oput(self, channel, txt):
        self.oqueue.put((channel, txt))

    def output(self):
        while not self.dostop.is_set():
            (channel, txt) = self.oqueue.get()
            if channel is None and txt is None:
                self.oqueue.task_done()
                break
            self.dosay(channel, txt)
            self.oqueue.task_done()

    def start(self):
        launch(self.output)

    def stop(self):
        self.oqueue.join()
        self.dostop.set()
        self.oqueue.put((None, None))

    def wait(self):
        self.dostop.wait()


"interface"


def __dir__():
    return (
        'Client',
        'Config',
        'Fleet',
        'Output'
    )
