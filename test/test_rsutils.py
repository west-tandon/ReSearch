import rsutils
import unittest
import shutil
import tempfile
import os


class RSUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)

    def test_flip(self):
        input = os.path.join(self.test_dir, "input")
        output = os.path.join(self.test_dir, "output")
        with open(input, 'bw') as f:
            f.write(b'\x00\x80\x08\x88')
        rsutils.flip_most_significant_bits(open(input, 'br'), open(output, 'bw'))
        with open(output, 'br') as f:
            self.assertEqual(f.read(1), b'\x80')
            self.assertEqual(f.read(1), b'\x00')
            self.assertEqual(f.read(1), b'\x88')
            self.assertEqual(f.read(1), b'\x08')
