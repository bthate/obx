# This file is placed in the Public Domain.


"interface"


import logging
import sys
import unittest


import obx.object


METHODS = [
    "Object",
    "construct",
    "edit",
    "fmt",
    "fqn",
    "items",
    "keys",
    "update",
    "values",
]



DICT = {}


DIFF = [
    "__dict__",
    "__module__",
    "__slots__",
]


OBJECT = obx.object


class TestInterface(unittest.TestCase): # pylint: disable=R0903

    "TestInterface"

    def test_methodinterface(self):
        "test methods interface."
        okd = True
        for meth in METHODS:
            func1 = getattr(OBJECT, meth)
            if not func1:
                continue
            func2 = DICT.get(meth)
            if not func2:
                continue
            if dir(func1) != dir(func2):
                print(func1, func2)
                okd = False
            sys.stdout.flush()
        self.assertTrue(okd)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("SomeTest.testSomething").setLevel(logging.DEBUG)
    unittest.main()
