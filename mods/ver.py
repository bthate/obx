# This file is placed in the Public Domain.


"version"


from obx.clients import Config


VERSION = "40"


"commands"


def ver(event):
    event.reply(f"{Config.name.upper()} {VERSION}")
