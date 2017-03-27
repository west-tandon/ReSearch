import argparse
import sys

from research.index.common import IndexFactory

parser = argparse.ArgumentParser(description='Flip the most significant bit in every byte of the file.')
parser.add_argument('index', type=str, help='JSON file of the input index')
g = parser.add_mutually_exclusive_group(required=True)
g.add_argument('--title', '-t', type=str, help='title to search for')
g.add_argument('--docid', '-d', type=int, help='document ID to search for')

args = parser.parse_args()

index = IndexFactory.from_path(args.index)
sys.stderr.write('Loading index...')
sys.stderr.flush()
reader = index.reader()
sys.stderr.write(' Done.\n')

document = None

if args.title is not None:
    document = reader.find_by_title(args.title)
else:
    document = reader.find_by_id(args.docid)

if document is None:
    print("Couldn't find document {}".format(args.title))
else:
    sys.stdout.write("\n# Document {0}: {1}\n".format(document.doc_id, document.title))
    term = document.next_term()
    if term is not None:
        sys.stdout.write(term)
        term = document.next_term()
        while term is not None:
            sys.stdout.write(" ")
            sys.stdout.write(term)
            term = document.next_term()
        sys.stdout.write('\n')
