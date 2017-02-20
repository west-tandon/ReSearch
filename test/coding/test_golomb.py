import io
import unittest

import bitstring as bt

import research.coding.golomb as golomb


class GolombTest(unittest.TestCase):

    def test_decode(self):
        bits = bt.Bits(bin='1')
        with self.subTest(input=bits):
            decoder = golomb.Decoder(bits.tobytes())
            self.assertEqual(decoder.decode(), 0)

        bits = bt.Bits(bin='010')
        with self.subTest(input=bits):
            decoder = golomb.Decoder(bits.tobytes())
            self.assertEqual(decoder.decode(), 1)

        bits = bt.Bits(bin='011')
        with self.subTest(input=bits):
            decoder = golomb.Decoder(bits.tobytes())
            self.assertEqual(decoder.decode(), 2)

        bits = bt.Bits(bin='00100')
        with self.subTest(input=bits):
            decoder = golomb.Decoder(bits.tobytes())
            self.assertEqual(decoder.decode(), 3)

        bits = bt.Bits(bin='0001010')
        with self.subTest(input=bits):
            decoder = golomb.Decoder(bits.tobytes())
            self.assertEqual(decoder.decode(), 9)

        bits = bt.Bits(bin='1010011001000001010')
        with self.subTest(input=bits):
            decoder = golomb.Decoder(bits.tobytes())
            self.assertEqual(decoder.decode(), 0)
            self.assertEqual(decoder.decode(), 1)
            self.assertEqual(decoder.decode(), 2)
            self.assertEqual(decoder.decode(), 3)
            self.assertEqual(decoder.decode(), 9)

    def test_encode(self):
        numbers = [0, 1, 2, 3, 9]
        with self.subTest(input=numbers, w='close'):
            b = io.BytesIO()
            encoder = golomb.Encoder(b)
            for n in numbers:
                encoder.encode(n)
            encoder.close()
            self.assertEqual(b.getvalue(), io.BytesIO(bt.Bits(bin='1010011001000001010').tobytes()).getvalue())

        numbers = [0, 1, 2, 3, 9]
        with self.subTest(input=numbers, w='flush'):
            b = io.BytesIO()
            encoder = golomb.Encoder(b)
            for n in numbers:
                encoder.encode(n)
                encoder.flush()
            encoder.close()
            self.assertEqual(b.getvalue(), io.BytesIO(bt.Bits(bin='1010011001000001010').tobytes()).getvalue())
