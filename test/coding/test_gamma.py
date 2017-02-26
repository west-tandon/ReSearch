import io
import unittest

import bitstring as bt

import research.coding.gamma as gamma


class GammaTest(unittest.TestCase):

    def test_decode(self):

        bits = bt.Bits(bin='1')
        with self.subTest(input=bits):
            decoder = gamma.Decoder(bits.tobytes())
            self.assertEqual(decoder.decode(), 1)

        bits = bt.Bits(bin='010')
        with self.subTest(input=bits):
            decoder = gamma.Decoder(bits.tobytes())
            self.assertEqual(decoder.decode(), 2)

        bits = bt.Bits(bin='011')
        with self.subTest(input=bits):
            decoder = gamma.Decoder(bits.tobytes())
            self.assertEqual(decoder.decode(), 3)

        bits = bt.Bits(bin='000010001')
        with self.subTest(input=bits):
            decoder = gamma.Decoder(bits.tobytes())
            self.assertEqual(decoder.decode(), 17)

        bits = bt.Bits(bin='1010011000010001')
        with self.subTest(input=bits):
            decoder = gamma.Decoder(bits.tobytes())
            self.assertEqual(decoder.decode(), 1)
            self.assertEqual(decoder.decode(), 2)
            self.assertEqual(decoder.decode(), 3)
            self.assertEqual(decoder.decode(), 17)

    def test_encode(self):

        n = 0
        with self.subTest(input=n):
            b = io.BytesIO()
            with self.assertRaises(AssertionError):
                gamma.Encoder(b).encode(n)

        numbers = [1, 2, 3, 17]
        with self.subTest(input=numbers, w='close'):
            b = io.BytesIO()
            encoder = gamma.Encoder(b)
            for n in numbers:
                encoder.encode(n)
            encoder.close()
            self.assertEqual(b.getvalue(), io.BytesIO(bt.Bits(bin='1010011000010001').tobytes()).getvalue())

        numbers = [1, 2, 3, 17]
        with self.subTest(input=numbers, w='flush'):
            b = io.BytesIO()
            encoder = gamma.Encoder(b)
            for n in numbers:
                encoder.encode(n)
                encoder.flush()
            encoder.close()
            self.assertEqual(b.getvalue(), io.BytesIO(bt.Bits(bin='1010011000010001').tobytes()).getvalue())