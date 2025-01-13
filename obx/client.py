# This file is placed in the Public Domain.
# pylint: disable=C,R0903,W0105,W0612,E0402


"client"


import queue
import threading


from .command import command
from .fleet   import Fleet
from .object  import Obj
from .reactor import Reactor
from .thread  import launch


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        Fleet.add(self)
        self.register("command", command)

    def display(self, evt):
        for txt, tme in sorted(evt.result, key=lambda x: x[1]):
            self.raw(txt)

    def raw(self, txt):
        raise NotImplementedError("raw")


"config"


class Config(Obj):

    name = Obj.__module__.split(".")[0]


"output"


class Output:

    cache = {}

    def __init__(self):
        self.oqueue = queue.Queue()
        self.dostop = threading.Event()

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


"buffered"


class Buffered(Output, Client):

    def __init__(self):
        Output.__init__(self)
        Client.__init__(self)

    def display(self, evt):
        for txt, tme in sorted(evt.result, key=lambda x: x[1]):
            self.oput(evt.channel, txt)

    def dosay(self, channel, txt):
        self.raw(txt)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def stop(self):
        Output.stop(self)
        Client.stop(self)

    def start(self):
        Output.start(self)
        Client.start(self)

    def wait(self):
        Output.wait(self)
        Client.wait(self)


"interface"


def __dir__():
    return (
        'Buffered',
        'Client',
        'Config',
        'Output'
    )
