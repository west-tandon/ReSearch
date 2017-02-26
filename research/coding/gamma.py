import math

import bitstring as bt
from research.coding.common import BitEncoder, BitDecoder

from research.coding.common import ONE, ZERO, read_unary


class Decoder(BitDecoder):
    def decode(self):
        N = read_unary(self.stream)
        bits = self.stream.read(N)
        bits.insert(ONE, 0)
        bits.pos = 0
        return bits.read('uint:{0}'.format(N + 1))


class Encoder(BitEncoder):
    def encode(self, n):
        assert n > 0, 'Gamma encoder encodes only numbers > 0'
        N = math.floor(math.log2(n))
        for i in range(N):
            self.bit_stream.append(ZERO)
        self.bit_stream.append(bt.Bits(uint=n, length=N + 1))
