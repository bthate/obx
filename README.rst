NAME

::

    NOTAI - program your own commands


NAME

    **NOTAI** - write your own commands


SYNOPSIS

    ::

        notai  <cmd> [key=val] [key==val]
        notaic [-i] [-v]
        notaid 


SYNOPSIS

::

    >>> from notai.object import Object, dumps, loads
    >>> o = Object()
    >>> o.a = "b"
    >>> txt = dumps(o)
    >>> loads(txt)
    {"a": "b"}


DESCRIPTION

::

    NOTAI has all the python3 code to program a unix cli program, such as
    disk perisistence for configuration files, event handler to
    handle the client/server connection, code to introspect modules
    for commands, deferred exception handling to not crash on an
    error, a parser to parse commandline options and values, etc.

    NOTAI uses object programming (OP) that allows for easy json save//load
    to/from disk of objects. It provides an "clean namespace" Object class
    that only has dunder methods, so the namespace is not cluttered with
    method names. This makes storing and reading to/from json possible.


**INSTALL**

    ::

        $ pipx install notai
        $ pipx ensurepath

        $ notai srv > notai.service
        # mv *.service /etc/systemd/system/
        # systemctl enable notai --now

        joins #notai on localhost


**USAGE**

    without any argument the bot does nothing

    ::

        $ notai
        $

    see list of commands

    ::

        $ notai cmd
        cmd,req,skl,srv


    start a console

    ::

        $ notaic
        >

    start daemon

    ::

        $ notaid
        $ 


CONFIGURATION

    irc

    ::

        $ notai cfg server=<server>
        $ notai cfg channel=<channel>
        $ notai cfg nick=<nick>

    sasl

    ::

        $ notai pwd <nsvnick> <nspass>
        $ notai cfg password=<frompwd>

    rss

    ::

        $ notai rss <url>
        $ notai dpl <url> <item1,item2>
        $ notai rem <url>
        $ notai nme <url> <name>


COMMANDS

    ::

        cfg - irc configuration
        cmd - commands
        mre - displays cached output
        pwd - sasl nickserv name/pass
        req - reconsider


**SOURCE**


    source is :ref:`here <source>`


**FILES**

    ::

        ~/.notai 
        ~/.local/bin/notai
        ~/.local/bin/notaic
        ~/.local/bin/notaid
        ~/.local/pipx/venvs/notai/*


AUTHOR

::

    Bart Thate <bthate@dds.nl>


COPYRIGHT

::

    NOTAI is Public Domain.
