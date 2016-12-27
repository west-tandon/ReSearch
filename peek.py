import argparse
import sys

import research.coding.double as double

parser = argparse.ArgumentParser(description='Decode list of byte-encoded values and display them in consecutive lines.')
# parser.add_argument('coding', required=True, type=argparse.FileType('br'))
parser.add_argument('input', nargs='?', type=argparse.FileType('br'), default=sys.stdin)
parser.add_argument('--output', '-o', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
parser.add_argument('--big-endian', '-b', nargs='?', type=bool, default=False)
args = parser.parse_args()

decoder = double.Decoder(args.input,big_endian=args.big_endian)
x = decoder.decode()
while x is not None:
    print(str(x))
    x = decoder.decode()
# /home/elshize/IdeaProjects/mg4j-nyu/src/test/resources/clusters/gov2C.minscore

