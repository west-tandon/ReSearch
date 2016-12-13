import unittest
import io
import research.coding.varbyte as varbyte


class VarbyteTest(unittest.TestCase):

    def testDecode(self):

        decoder = varbyte.Decoder(io.BytesIO(b'\x81'))
        with self.subTest(decoder=decoder, expected=1):
            self.assertEqual(decoder.decode(), 1)

        decoder = varbyte.Decoder(io.BytesIO(b'\x01\x81'))
        with self.subTest(decoder=decoder, expected=129):
            self.assertEqual(decoder.decode(), 129)

        decoder = varbyte.Decoder(io.BytesIO(b'\x81\x01\x81'))
        with self.subTest(decoder=decoder, expected=129):
            self.assertEqual(decoder.decode(), 1)
            self.assertEqual(decoder.decode(), 129)
            with self.assertRaises(ValueError):
                decoder.decode()

    def testEncode(self):

        with self.subTest(encoded=1):
            b = io.BytesIO()
            encoder = varbyte.Encoder(b)
            encoder.encode(1)
            self.assertEqual(b.getvalue(), b'\x81')
            encoder.encode(129)
            self.assertEqual(b.getvalue(), b'\x81\x01\x81')