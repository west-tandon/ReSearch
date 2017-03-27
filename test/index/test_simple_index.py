import shutil
import tempfile
import unittest
from os import path

from research.coding.varbyte import Encoder
from research.index.common import IndexFactory, write_header
from research.index.simple import *


def get_index(test_dir) -> Index:

    with open(path.join(test_dir, 'simple.terms'), 'w') as f:
        f.write("a\n")
        f.write("b\n")
        f.write("c\n")

    with open(path.join(test_dir, 'simple.docs'), 'bw') as f:
        write_header({"coding": "research.coding.varbyte"}, f)
        encoder = Encoder(f)
        # a
        encoder.encode(1)
        encoder.encode(4)  # 5
        encoder.encode(4)  # 9
        # b
        encoder.encode(1)
        encoder.encode(1)  # 2
        # c
        encoder.encode(5)
        encoder.encode(1)  # 6
        encoder.encode(2)  # 8

    with open(path.join(test_dir, 'simple.frequencies'), 'bw') as f:
        write_header({"count": 3, "coding": "research.coding.varbyte"}, f)
        encoder = Encoder(f)
        encoder.encode(3)
        encoder.encode(2)
        encoder.encode(3)

    with open(path.join(test_dir, 'simple.docs#offsets'), 'bw') as f:
        write_header({"count": 3, "coding": "research.coding.varbyte"}, f)
        encoder = Encoder(f)
        encoder.encode(0)
        encoder.encode(3)
        encoder.encode(5)

    with open(path.join(test_dir, 'simple.counts'), 'bw') as f:
        write_header({"coding": "research.coding.varbyte"}, f)
        encoder = Encoder(f)
        # a
        encoder.encode(1)
        encoder.encode(1)
        encoder.encode(3)
        # b
        encoder.encode(2)
        encoder.encode(2)
        # c
        encoder.encode(2)
        encoder.encode(5)
        encoder.encode(20)

    with open(path.join(test_dir, 'simple.counts#offsets'), 'bw') as f:
        write_header({"count": 3, "coding": "research.coding.varbyte"}, f)
        encoder = Encoder(f)
        encoder.encode(0)
        encoder.encode(3)
        encoder.encode(5)

    return IndexFactory.from_json({
        'type': 'research.index.simple.Index',
        'name': 'simple',
        'dir': test_dir
    })


# class SimpleIndexTest(unittest.TestCase):
#     pass
#
#
class IndexReaderTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.index = get_index(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def basic_test(self):
        reader = self.index.reader()

        ilr = reader.documents(term='z')
        self.assertEqual(ilr, None)

        ilr = reader.documents(term='a')
        self.assertEqual(ilr.term, 'a')
        self.assertEqual(ilr.frequency, 3)
        self.assertEqual(ilr.next_doc(), 1)
        self.assertEqual(ilr.count, 1)
        self.assertEqual(ilr.next_doc(), 5)
        self.assertEqual(ilr.count, 1)
        self.assertEqual(ilr.next_doc(), 9)
        self.assertEqual(ilr.count, 3)
        self.assertEqual(ilr.next_doc(), None)

        ilr = reader.documents(term='b')
        self.assertEqual(ilr.term, 'b')
        self.assertEqual(ilr.frequency, 2)
        self.assertEqual(ilr.next_doc(), 1)
        self.assertEqual(ilr.count, 2)

        ilr = reader.next()
        self.assertEqual(ilr.term, None)
        self.assertEqual(ilr.frequency, 3)
        self.assertEqual(ilr.next_doc(), 5)
        self.assertEqual(ilr.count, 2)
        self.assertEqual(ilr.next_doc(), 6)
        self.assertEqual(ilr.count, 5)
        self.assertEqual(ilr.next_doc(), 8)
        self.assertEqual(ilr.count, 20)
        self.assertEqual(ilr.next_doc(), None)

        reader.close()

        with self.assertRaises(AssertionError):
            reader.next()
        with self.assertRaises(AssertionError):
            reader.documents(term_id=0)

    def test_next_ge(self):
        reader = self.index.reader()

        ilr = reader.documents(term='a')
        self.assertEqual(ilr.next_doc(), 1)
        self.assertEqual(ilr.next_ge(4), 5)
        self.assertEqual(ilr.next_ge(5), 5)
        self.assertEqual(ilr.next_ge(8), 9)
        self.assertEqual(ilr.next_ge(10), None)

        ilr = reader.documents(term='b')
        self.assertEqual(ilr.next_ge(4), None)
        self.assertEqual(ilr.next_doc(), None)

        reader.close()
