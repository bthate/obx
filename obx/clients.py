# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,W0105,W0212,W0613,W0718,E0402


"clients"


import queue
import threading


from obr.default import Default
from obr.reactor import Fleet, Reactor
from obr.threads import launch


class Config(Default):

    init = ""
    name = "obx"
    opts = Default()


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        Fleet.add(self)

    def raw(self, txt) -> None:
        raise NotImplementedError("raw")

    def say(self, channel, txt) -> None:
        self.raw(txt)


class Output:
    def __init__(self):
        self.oqueue   = queue.Queue()
        self.running = threading.Event()

    def loop(self) -> None:
        self.running.set()
        while self.running.is_set():
            evt = self.oqueue.get()
            if evt is None:
                self.oqueue.task_done()
                break
            Fleet.display(evt)
            self.oqueue.task_done()

    def oput(self,evt) -> None:
        if not self.running.is_set():
            Fleet.display(evt)
        self.oqueue.put(evt)

    def start(self) -> None:
        if not self.running.is_set():
            self.running.set()
            launch(self.loop)

    def stop(self) -> None:
        self.running.clear()
        self.oqueue.put(None)

    def wait(self) -> None:
        self.oqueue.join()
        self.running.wait()


class Buffered(Client, Output):

    def __init__(self):
        Client.__init__(self)
        Output.__init__(self)

    def raw(self, txt) -> None:
        raise NotImplementedError("raw")

    def start(self) -> None:
        Output.start(self)
        Client.start(self)

    def stop(self) -> None:
        Output.stop(self)
        Client.stop(self)

    def wait(self) -> None:
        Output.wait(self)
        Client.wait(self)


def debug(txt) -> None:
    if "v" in Config.opts:
        output(txt)


def output(txt) -> None:
    # output here
    print(txt)


def __dir__():
    return (
        'Default',
        'Client',
        'Fleet',
        'debug'
    )
