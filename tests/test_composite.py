# This file is placed in the Public Domain.
# pylint: disable=C


"composite"


import unittest


from obx import Object, dumps, loads


class Tmp(Object):

    pass

class Temp(Object):

    def __init__(self):
        Object.__init__(self)
        self.a = Tmp()


class TestComposite(unittest.TestCase):

    def testcomposite(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.abc = "test"
        self.assertEqual(obj.obj.abc, "test")