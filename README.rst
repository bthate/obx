NAME

::

    OBX - program your own commands


INSTALL

::

    $ pipx install obx
    $ pipx ensurepath


SYNOPSIS

::

    >>> from obx.object import Object, dumps, loads
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

    obx.broker     object broker
    obx.client     clients
    obx.disk       object store
    obx.find       find objects on disk
    obx.handler    event handler
    obx.log        logging
    obx.object     a clean namespace
    obx.run        runtime
    obx.threads	   threads



AUTHOR

::

    Bart Thate <bthate@dds.nl>


COPYRIGHT

::

    OBX is Public Domain.
