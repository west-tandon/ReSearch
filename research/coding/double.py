"""
IEEE 754 double precision format
"""
import struct


class Decoder:

    def __init__(self, stream, big_endian=False):
        self.stream = stream
        self.big_endian = big_endian

    def decode(self):
        x = self.stream.read(8)
        if x == b"":
            return None
        else:
            if self.big_endian:
                return struct.unpack('>d', x)[0]
            else:
                return struct.unpack('<d', x)[0]


class Encoder:

    def __init__(self, stream):
        self.stream = stream

    def encode(self, x):
        self.stream.write(struct.pack('d', x))


class Factory:
    @staticmethod
    def encoder(stream):
        return Encoder(stream)

    @staticmethod
    def decoder(stream):
        return Decoder(stream)