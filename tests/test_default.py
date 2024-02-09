# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116


"defaults"


import unittest


from obx import Default


class TestDefault(unittest.TestCase):

    def test_construct(self):
        obj = Default()
        self.assertEqual(type(obj), Default)

    def test_access(self):
        obj = Default()
        self.assertEqual(obj.test, '')
