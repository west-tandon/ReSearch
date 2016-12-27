import argparse

import research.utils as utils
from research.index.common import IndexFactory

parser = argparse.ArgumentParser(description='Flip the most significant bit in every byte of the file.')
parser.add_argument('index', type=str, help='Properties file of the input index')
parser.add_argument('--pruner', '-p', required=True, type=str, help='A pruner to be used')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--output', '-o', type=str, help='Properties file of the output index')
group.add_argument('--json', '-j', type=str, help='JSON string defining output index')

args = parser.parse_args()

input_index = IndexFactory.from_path(args.index)
output_index = IndexFactory.from_path(args.output)

input_index.prune(utils.get_object_of(args.pruner), output_index)
