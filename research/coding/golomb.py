import math
import bitstring as bt
from research.coding.common import BitEncoder, BitDecoder


class Decoder(BitDecoder):

    def decode(self):
        return self.stream.read('ue')


class Encoder(BitEncoder):

    def encode(self, n):
        self.bit_stream.append(bt.pack('ue', n))
