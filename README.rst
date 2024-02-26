NAME

::

    OBX - program your own commands


SYNOPSIS

::

    >>> from obx import Object, dumps, loads
    >>> o = Object()
    >>> o.a = "b"
    >>> txt = dumps(o)
    >>> loads(txt)
    {"a": "b"}


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


CONTENT

::

    obx.brokers     object broker
    obx.excepts     deferred exception handling
    obx.handler     event handler
    obx.locates     find objects on disk
    obx.objects     a clean namespace
    obx.parsers     arguments parsing
    obx.persist     object store
    obx.repeats     repeaters
    obx.threads	    threads
    obx.workdir     directory to store objects


INSTALL

::

    $ pip install obx


AUTHOR

::

    Bart Thate <bthate@dds.nl>


COPYRIGHT

::

    OBX is Public Domain.
