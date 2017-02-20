import math

import bitstring as bt

from research.coding.common import ONE, ZERO, read_unary


class Decoder:

    def __init__(self, stream):
        self.stream = bt.BitStream(bytes=stream)

    def decode(self):
        N = read_unary(self.stream)
        bits = self.stream.read(N)
        bits.insert(ONE, 0)
        bits.pos = 0
        return bits.read('uint:{0}'.format(N + 1))


class Encoder:

    def __init__(self, stream):
        self.stream = stream
        self.bit_stream = bt.BitStream()

    def encode(self, n):
        assert n > 0, 'Gamma encoder encodes only numbers > 0'
        N = math.floor(math.log2(n))
        for i in range(N):
            self.bit_stream.append(ZERO)
        self.bit_stream.append(bt.Bits(uint=n, length=N + 1))

    def flush(self):
        len = math.floor((self.bit_stream.length - self.bit_stream.pos) / 8)
        self.stream.write(self.bit_stream[:len * 8].tobytes())
        self.bit_stream = self.bit_stream[len * 8:]

    def close(self):
        self.stream.write(self.bit_stream.tobytes())
