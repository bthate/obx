# This file is placed in the Public Domain.
# pylint: disable=C0116,W0105,E0402


"uptime"


import time


from obx.find import elapsed


STARTTIME = time.time()


"commands"


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))
