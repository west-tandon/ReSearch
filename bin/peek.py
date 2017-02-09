import argparse
import sys

import research.coding.double
import research.coding.varbyte

parser = argparse.ArgumentParser(description='Decode list of byte-encoded values and display them in consecutive lines.')
parser.add_argument('format', type=str)
parser.add_argument('input', nargs='*', type=argparse.FileType('br'), default=sys.stdin)
parser.add_argument('--output', '-o', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
parser.add_argument('--delimiter', '-d', type=str, default='\t')
args = parser.parse_args()


class StringDecoder:
    def __init__(self, stream):
        self.stream = stream

    def decode(self):
        line = self.stream.readline()
        if line == b"":
            return None
        else:
            return line[:-1].decode("UTF-8")


def get_decoder(file, coding):
    if coding.lower() == 'd':
        return research.coding.double.Decoder(file, big_endian=coding.isupper())
    if coding.lower() == 's':
        return StringDecoder(file)
    if coding.lower() == 'v':
        return research.coding.varbyte.Decoder(file)
    else:
        raise ValueError('invalid coding format: {0}'.format(coding))

try:
    decoders = [
        get_decoder(file, coding)
        for (file, coding) in zip(args.input, list(args.format))
    ]
    x = [decoder.decode() for decoder in decoders]
    while x[0] is not None:
        for v in x:
            args.output.write(str(v))
            args.output.write(args.delimiter)
        args.output.write('\n')
        x = [decoder.decode() for decoder in decoders]
except BrokenPipeError:
    exit()
except KeyboardInterrupt:
    exit()

args.output.close()
