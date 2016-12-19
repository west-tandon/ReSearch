import io

from research.index import Metadata
from research.index import raise_property_not_found


class ForwardIndex:
    def __init__(self, properties):
        self.metadata = ForwardIndexMetadata(properties)

    def reader(self):
        return ForwardIndexReader(self.metadata)

    # def export(self, metadata):


class ForwardIndexMetadata(Metadata):
    f_doc_info = "doc_info"
    f_collection = "collection"

    def __init__(self, properties):
        super(ForwardIndexMetadata, self).__init__(properties)

        assert properties[Metadata.f_type] == "{0}.{1}".format(ForwardIndex.__module__, ForwardIndex.__name__)

        if ForwardIndexMetadata.f_doc_info not in self.paths:
            raise_property_not_found(ForwardIndexMetadata.f_doc_info)
        else:
            self.doc_info_path = self.paths[ForwardIndexMetadata.f_doc_info]

        if ForwardIndexMetadata.f_collection not in self.paths:
            raise_property_not_found(ForwardIndexMetadata.f_collection)
        else:
            self.collection_path = self.paths[ForwardIndexMetadata.f_collection]


class ForwardIndexReader:
    def __init__(self, metadata):
        self.doc_info_reader = io.open(metadata.doc_info_path, 'r')
        self.term_stream = io.open(metadata.collection_path, 'br')
        self.decoder = metadata.coder_factory.decoder(self.term_stream)

    def next_document(self):
        meta_line = self.doc_info_reader.readline()
        if meta_line == "":
            return None
        else:
            (title, doc_id, offset, size, count) = Document.parse_meta(meta_line)
            return Document(title, doc_id, count, self.decoder)

    def close(self):
        self.doc_info_reader.close()
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
