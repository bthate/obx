# This file is placed in the Public Domain.
# pylint: disable=C,W0105,E0402


"commands"


from obx.object  import keys
from obx.runtime import Commands


def cmd(event):
    event.reply(",".join(sorted(keys(Commands.cmds))))
