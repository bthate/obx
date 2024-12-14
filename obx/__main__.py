#!/usr/bin/env python3
# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0415,R0903,R0912,R0915,W0105,W0718,E0402


"main"


import os
import sys


sys.path.insert(0, os.getcwd())


from obx.mods import face
from obx.persist import Config
from obx.run     import Client, Commands, Event
from obx.run     import command, errors, parse, scan, wrap


Config.name = "obx"
Config.wdr  = os.path.expanduser(f"~/.{Config.name}")


Cfg = Config()


class CLI(Client):

    def raw(self, txt):
        print(txt)


def main():
    parse(Cfg, " ".join(sys.argv[1:]))
    scan(face)
    evt = Event()
    evt.type = "command"
    evt.txt = Cfg.otxt
    csl = CLI()
    command(csl, evt)
    evt.wait()


if __name__ == "__main__":
    main()
    for txt in errors():
        print(txt)
