NAME

::

    OBX - write your own commands


SYNOPSIS

::

    obx  <cmd> [key=val] [key==val]
    obxc [-i] [-v]
    obxd 


DESCRIPTION

::

    OBX has all the python3 code to program a unix cli program, such as
    disk perisistence for configuration files, event handler to
    handle the client/server connection, code to introspect modules
    for commands, deferred exception handling to not crash on an
    error, a parser to parse commandline options and values, etc.

    OBX uses object programming (OP) that allows for easy json save//load
    to/from disk of objects. It provides an "clean namespace" Object class
    that only has dunder methods, so the namespace is not cluttered with
    method names. This makes storing and reading to/from json possible.

    OBX has a demo bot, it can connect to IRC, fetch and display RSS
    feeds, take todo notes, keep a shopping list and log text. You can
    also copy/paste the service file and run it under systemd for 24/7
    presence in a IRC channel.

    OBX is Public Domain.


INSTALL

::

    $ pipx install obx
    $ pipx ensurepath

    <new terminal>

    $ obx srv > obx.service
    # mv *.service /etc/systemd/system/
    # systemctl enable obx --now

    joins #obx on localhost


USAGE

::

    without any argument the bot does nothing::

    $ obx
    $

    see list of commands

    $ obx cmd
    cmd,skl,srv


    start a console

    $ obxc
    >

    start daemon

    $ obxd
    $ 


CONFIGURATION

::

    irc

    $ obx cfg server=<server>
    $ obx cfg channel=<channel>
    $ obx cfg nick=<nick>

    sasl

    $ obx pwd <nsvnick> <nspass>
    $ obx cfg password=<frompwd>

    rss

    $ obx rss <url>
    $ obx dpl <url> <item1,item2>
    $ obx rem <url>
    $ obx nme <url> <name>


COMMANDS

::

    cfg - irc configuration
    cmd - commands
    mre - displays cached output
    pwd - sasl nickserv name/pass


FILES

::

    ~/.obx
    ~/.local/bin/obx
    ~/.local/bin/obxc
    ~/.local/bin/obxd
    ~/.local/pipx/venvs/obx/*


AUTHOR

::

    Bart Thate <bthate@dds.nl>


COPYRIGHT

::

    OBX is Public Domain.
