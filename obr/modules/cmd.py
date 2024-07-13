# This file is placed in the Public Domain.


"list of commands"


from obx.object import keys
from ..cmds     import Commands


def cmd(event):
    "list commands."
    event.reply(",".join(sorted(keys(Commands.modnames))))
