class Decoder:

    def __init__(self, stream):
        self.stream = stream

    def decode(self):
        byte = self.stream.read(1)
        n = 0
        while byte != b"":
            n <<= 7
            val = byte[0] & 0b01111111
            n |= val
            if byte[0] != val:
                return n
            else:
                byte = self.stream.read(1)
        raise ValueError("stream ended before the last byte could be retrieved")


class Encoder:

    def __init__(self, stream):
        self.stream = stream

    def encode(self, n):
        if n < 0:
            raise ValueError("encoded number bust be non-negative, but {0} given".format(n))
        buffer = bytearray(8)
        p = 8
        while n > 0b01111111:
            p -= 1
            buffer[p] = n & 0b01111111
            n >>= 7
        p -= 1
        buffer[p] = n
        buffer[7] ^= 0b10000000
        self.stream.write(buffer[p:])
        return 8 - p
