**NAME**

``OBX`` - write your own commands


**SYNOPSIS**

::

    obx  <cmd> [key=val] [key==val]
    obxc [-i] [-v]
    obxd 
    obxs


**DESCRIPTION**


``OBX`` has all the python3 code to program a unix cli program, such as
disk perisistence for configuration files, event handler to
handle the client/server connection, code to introspect modules
for commands, deferred exception handling to not crash on an
error, a parser to parse commandline options and values, etc.

``OBX`` uses object programming (OP) that allows for easy json save//load
to/from disk of objects. It provides an "clean namespace" Object class
that only has dunder methods, so the namespace is not cluttered with
method names. This makes storing and reading to/from json possible.

``OBX`` has a demo bot, it can connect to IRC, fetch and display RSS
feeds, take todo notes, keep a shopping list and log text. You can
also copy/paste the service file and run it under systemd for 24/7
presence in a IRC channel.

``OBX`` is Public Domain.


**INSTALL**

::

    $ pipx install obx
    $ pipx ensurepath


**CONFIGURATION**


irc

::

    $ obx cfg server=<server>
    $ obx cfg channel=<channel>
    $ obx cfg nick=<nick>

sasl

::

    $ obx pwd <nsvnick> <nspass>
    $ obx cfg password=<frompwd>

rss

::

    $ obx rss <url>
    $ obx dpl <url> <item1,item2>
    $ obx rem <url>
    $ obx nme <url> <name>

opml

::

    $ obx exp
    $ obx imp <filename>


**SYSTEMD**

    $ obx srv > obx.service
    $ sudo mv obx.service /etc/systemd/system/
    $ sudo systemctl enable obx --now

    joins #obx on localhost


**USAGE**


without any argument the bot does nothing

::

    $ obx
    $

see list of commands

::

    $ obx cmd
    cfg,cmd,dne,dpl,err,exp,imp,log,mod,mre,nme,
    pwd,rem,req,res,rss,srv,syn,tdo,thr,upt


start a console

::

    $ obxc
    >


use -v to enable verbose

::

    $ obxc -v
    OBX since Tue Sep 17 04:10:08 2024
    > 


use -i to init modules

::

    $ obxc -i
    >



start daemon

::

    $ obxd
    $


start service

::

   $ obxs
   <runs until ctrl-c>


**COMMANDS**

::

    here is a list of available commands

    cfg - irc configuration
    cmd - commands
    dpl - sets display items
    err - show errors
    exp - export opml (stdout)
    imp - import opml
    log - log text
    mre - display cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    res - restore deleted feeds
    rss - add a feed
    srv - create service file
    syn - sync rss feeds
    tdo - add todo item
    thr - show running threads


**SOURCE**

::

    source is at https://github.com/bthate/obx



**FILES**

::

    ~/.obx
    ~/.local/bin/obx
    ~/.local/bin/obxc
    ~/.local/bin/obxd
    ~/.local/bin/obxs
    ~/.local/pipx/venvs/obx/*


**AUTHOR**

::

    Bart Thate <bthate@dds.nl>


**COPYRIGHT**

::

    OBX is Public Domain.
