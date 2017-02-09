import argparse
import sys

from research.index.common import IndexFactory

parser = argparse.ArgumentParser(description='Flip the most significant bit in every byte of the file.')
parser.add_argument('index', type=str, help='JSON file of the input index')
parser.add_argument('--start', '-s', numarg='?', default=0, type=int, help='the document index to start with')

args = parser.parse_args()

index = IndexFactory.from_path(args.index)
reader = index.reader()
reader.skip(0)

while True:
    document = reader.next_document()
    if document is None:
        break
    sys.stdout.write("# Document {0}: {1}".format(document.doc_id, document.title))
    term = document.next_term()
    if term is not None:
        sys.stdout.write(term)
        term = document.next_term()
        while term is not None:
            sys.stdout.write(" ")
            sys.stdout.write(term)
            term = document.next_term()
    cmd = input('')
    if cmd == 'q':
        break
    try:
        s = int(cmd)
        reader.skip(s)
    except ValueError:
        pass
