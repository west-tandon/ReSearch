import unittest

from research.coding.common import *


class CommonTest(unittest.TestCase):

    def test_read_unary(self):
        bs = bt.BitStream(bin='00001')
        with self.subTest(stream=bs):
            self.assertEqual(read_unary(bs), 4)
            self.assertEqual(bs.pos, bs.length)

        bs = bt.BitStream(bin='000010')
        with self.subTest(stream=bs):
            self.assertEqual(read_unary(bs), 4)
            self.assertEqual(bs.pos, bs.length - 1)

        bs = bt.BitStream(bin='100000')
        with self.subTest(stream=bs):
            self.assertEqual(read_unary(bs), 0)
            self.assertEqual(bs.pos, 1)