import argparse
import sys

from research.index.common import IndexFactory

parser = argparse.ArgumentParser(description='Flip the most significant bit in every byte of the file.')
parser.add_argument('index', type=str, help='JSON file of the input index')
parser.add_argument('--start', '-s', nargs='?', default=0, type=int, help='the document index to start with')

args = parser.parse_args()

index = IndexFactory.from_path(args.index)
sys.stderr.write('Loading index...\n')
reader = index.reader()
reader.skip(args.start)

while True:
    document = reader.next_document()
    if document is None:
        break
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
    cmd = input('')
    if cmd == 'q':
        sys.stderr.write('Quitting...\n')
        break
    try:
        s = int(cmd)
        reader.skip(s)
    except ValueError:
        pass
