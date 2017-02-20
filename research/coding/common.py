import math
import bitstring as bt

ZERO = bt.Bits(bin='0')
ONE = bt.Bits(bin='1')


def read_unary(bit_stream):
    bit = bit_stream.read(1)
    n = 0
    while bit == ZERO:
        n += 1
        bit = bit_stream.read(1)
    return n


class BitDecoder:
    def __init__(self, stream):
        self.stream = bt.BitStream(bytes=stream)


class BitEncoder:
    def __init__(self, stream):
        self.stream = stream
        self.bit_stream = bt.BitStream()

    def flush(self):
        num_bytes_to_flush = math.floor((self.bit_stream.length - self.bit_stream.pos) / 8)
        num_bits_to_flush = num_bytes_to_flush * 8
        self.stream.write(self.bit_stream[:num_bits_to_flush].tobytes())
        self.bit_stream = self.bit_stream[num_bits_to_flush:]

    def close(self):
        self.stream.write(self.bit_stream.tobytes())
