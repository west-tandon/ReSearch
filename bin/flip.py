import research.utils
import argparse
import sys

parser = argparse.ArgumentParser(description='Flip the most significant bit in every byte of the file.')
parser.add_argument('input', nargs='?', type=argparse.FileType('br'), default=sys.stdin)
parser.add_argument('--output', '-o', nargs='?', type=argparse.FileType('bw'), default=sys.stdout)
args = parser.parse_args()

research.utils.flip_most_significant_bits(args.input, args.output)
