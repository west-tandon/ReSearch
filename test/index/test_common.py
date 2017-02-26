import io
import shutil
import tempfile
import unittest
from os import path

from research.coding.varbyte import Encoder
from research.index.common import read_header, write_header, load_numbers


class HeaderTest(unittest.TestCase):

    def test(self):
        input_obj = {
            "key": "value",
            "list_key": ["e1", "e2"]
        }
        buffer = io.BytesIO()

        write_header(input_obj, buffer)
        buffer.seek(0)
        read_obj, l = read_header(buffer)
        self.assertEqual(input_obj, read_obj)


class LoadNumbersTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test(self):
        filename = path.join(self.test_dir, 'offsets')
        input_obj = {
            "coding": "research.coding.varbyte",
            "count": 3
        }
        with open(filename, 'bw') as f:
            write_header(input_obj, f)
            encoder = Encoder(f)
            encoder.encode(3)
            encoder.encode(2)
            encoder.encode(1)

        offsets = load_numbers(filename)
        self.assertListEqual(offsets, [3, 2, 1])


class IndexCommonTest(unittest.TestCase):
    pass
