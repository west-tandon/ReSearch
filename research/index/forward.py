import json
import io
from research.coding.varbyte import Decoder


class ForwardIndex:
    def __init__(self, metadata):
        self.metadata = metadata

    @staticmethod
    def load(metadata_path):
        with open(metadata_path) as file:
            return ForwardIndex(json.loads(file.read()))

    def reader(self):
        paths = self.metadata["paths"]
        return ForwardIndexReader(paths["doc_info"], paths['collection'])


class ForwardIndexReader:
    def __init__(self, meta, collection):
        self.meta_reader = io.open(meta, 'r')
        self.term_stream = io.open(collection, 'br')
        self.decoder = Decoder(self.term_stream)

    def next_document(self):
        meta_line = self.meta_reader.readline()
        if meta_line == "":
            return None
        else:
            (title, doc_id, offset, size, count) = Document.parse_meta(meta_line)
            return Document(title, doc_id, count, self.decoder)

    def close(self):
        self.meta_reader.close()
        self.term_stream.close()


class Document:
    def __init__(self, title, doc_id, count, decoder):
        self.title = title
        self.doc_id = doc_id
        self.count = count
        self.remaining = count
        self.decoder = decoder

    def next_term(self):
        if self.remaining == 0:
            return None
        else:
            self.remaining -= 1
            return self.decoder.decode()

    @staticmethod
    def parse_meta(meta_line):
        fields = meta_line.split()
        if len(fields) != 5:
            raise ValueError("expected 5 fields in document meta file, but %d found" % len(fields))
        return fields[0], int(fields[1]), int(fields[2]), int(fields[3]), int(fields[4])
