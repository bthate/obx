**NAME**


``OBX`` - objects


**SYNOPSIS**


|
| ``obx <cmd> [key=val] [key==val]``
| ``obx -cviw [init=mod1,mod2]``
| ``obx -d`` 
| ``obx -s``
|

**DESCRIPTION**


``OBX`` has all you need to program a unix cli program, such as disk
perisistence for configuration files, event handler to handle the
client/server connection, deferred exception handling to not crash
on an error, etc.

``OBX`` allows for easy json save//load to/from disk of objects. It
provides an "clean namespace" Object class that only has dunder
methods, so the namespace is not cluttered with method names. This
makes storing and reading to/from json possible.

``OBX`` is a demo bot, it can connect to IRC, fetch and display RSS
feeds, take todo notes, keep a shopping list and log text. You can
also copy/paste the service file and run it under systemd for 24/7
presence in a IRC channel.

``OBX`` is Public Domain.


**INSTALL**


installation is done with pipx

|
| ``$ pipx install obx``
| ``$ pipx ensurepath``
|
| <new terminal>
|
| ``$ obx srv > obx.service``
| ``$ sudo mv obx.service /etc/systemd/system/``
| ``$ sudo systemctl enable obx --now``
|
| joins ``#obx`` on localhost
|


**USAGE**


use ``obx`` to control the program, default it does nothing

|
| ``$ obx``
| ``$``
|

see list of commands

|
| ``$ obx cmd``
| ``cfg,cmd,dne,dpl,err,exp,imp,log,mod,mre,nme,``
| ``now,pwd,rem,req,res,rss,srv,syn,tdo,thr,upt``
|

start daemon

|
| ``$ obx -d``
| ``$``
|

start service

|
| ``$ obx -s``
| ``<runs until ctrl-c>``
|


**COMMANDS**


here is a list of available commands

|
| ``cfg`` - irc configuration
| ``cmd`` - commands
| ``dpl`` - sets display items
| ``err`` - show errors
| ``exp`` - export opml (stdout)
| ``imp`` - import opml
| ``log`` - log text
| ``mre`` - display cached output
| ``now`` - show genocide stats
| ``pwd`` - sasl nickserv name/pass
| ``rem`` - removes a rss feed
| ``res`` - restore deleted feeds
| ``req`` - reconsider
| ``rss`` - add a feed
| ``syn`` - sync rss feeds
| ``tdo`` - add todo item
| ``thr`` - show running threads
| ``upt`` - show uptime
|

**CONFIGURATION**


irc

|
| ``$ obx cfg server=<server>``
| ``$ obx cfg channel=<channel>``
| ``$ obx cfg nick=<nick>``
|

sasl

|
| ``$ obx pwd <nsvnick> <nspass>``
| ``$ obx cfg password=<frompwd>``
|

rss

|
| ``$ obx rss <url>``
| ``$ obx dpl <url> <item1,item2>``
| ``$ obx rem <url>``
| ``$ obx nme <url> <name>``
|

opml

|
| ``$ obx exp``
| ``$ obx imp <filename>``
|


**PROGRAMMING**

``obx`` runs it's modules in the package, so you have to clone from git

|
| ``$ git clone ssh://git@github.com/bthate/obx``
|

edit a file in obx/modules/<name>.py and add the following for ``hello world``

::

    def hello(event):
        event.reply("hello world !!")


save this and recreate the dispatch table

|
| ``$ obx tbl > obx/modules/tbl.py``
|

install that with ``pipx install . --force``, your program can execute the
``hello`` command now.

|
| ``$ obx hello``
| ``hello world !!``
|

commands run in their own thread and the program borks on exit, output gets
flushed on print so exceptions appear in the systemd logs, modules can contain
your own written python3 code, see the obx/modules directory for examples.


**FILES**

|
| ``~/.obx``
| ``~/.local/bin/obx``
| ``~/.local/pipx/venvs/obx/*``
|

**AUTHOR**

|
| ``Bart Thate`` <``bthate@dds.nl``>
|

**COPYRIGHT**

|
| ``OBX`` is Public Domain.
|
