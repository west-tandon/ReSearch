import unittest
import io
import research.coding.double as double


class DoubleTest(unittest.TestCase):

    def test_decode(self):

        with self.subTest(expected=1.5,type='little-endian'):
            decoder = double.Decoder(io.BytesIO(b'\x00\x00\x00\x00\x00\x00\xF8\x3F'))
            self.assertEqual(decoder.decode(), 1.5)
            self.assertEqual(decoder.decode(), None)

        with self.subTest(expected=1.5,type='big-endian'):
            decoder = double.Decoder(io.BytesIO(b'\x3F\xF8\x00\x00\x00\x00\x00\x00'), big_endian=True)
            self.assertEqual(decoder.decode(), 1.5)
            self.assertEqual(decoder.decode(), None)

    def test_encode(self):

        with self.subTest(encoded=1.5):
            b = io.BytesIO()
            encoder = double.Encoder(b)
            encoder.encode(1.5)
            self.assertEqual(b.getvalue(), b'\x00\x00\x00\x00\x00\x00\xF8\x3F')
