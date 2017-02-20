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