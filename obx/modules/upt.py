# This file is placed in the Public Domain.
# pylint: disable=C0116,E0402


"uptime"


import time


from obx.utility import elapsed


STARTTIME = time.time()


def upt(event):
    event.reply(elapsed(time.time()-STARTTIME))
