# This file is in the Public Domain.
# pylint: disable=C0116,C0415,E0402


"service"


import os


from .modules import face
from .persist import NAME, pidfile, pidname
from .runtime import errors, forever, scan, wrap


def privileges():
    import getpass
    import pwd
    pwnam2 = pwd.getpwnam(getpass.getuser())
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)


def service():
    privileges()
    pidfile(pidname(NAME))
    scan(face, init=True)
    forever()


def wrapped():
    wrap(service)
    for line in errors():
        print(line)


if __name__ == "__main__":
    wrapped()
