import io

from research.index.common import Metadata
from research.index.common import raise_property_not_found


class ForwardIndex:
    def __init__(self, properties):
        self.metadata = ForwardIndexMetadata(properties)

    def reader(self):
        return ForwardIndexReader(self.metadata)

    def writer(self):
        return ForwardIndexWriter(self.metadata)

    def prune(self, term_pruner, output_index):

        with open(self.metadata.terms_path) as input_term_file:
            with open(output_index.metadata.terms_path, "w") as output_term_file:

                def write_term(t):
                    output_term_file.write(t)
                    return 1

                offsets = [write_term(term) if term_pruner.test(term[:-1]) else 0 for term in input_term_file]
                for i in range(1, len(offsets)):
                    offsets[i] += offsets[i - 1]

        reader = self.reader()
        writer = output_index.writer()

        byte_offset = 0
        document = reader.next_document()
        doc_offset = 0
        while document is not None:

            term_count = 0
            byte_count = 0
            term_id = document.next_term()
            while term_id is not None:
                if (term_id > 0 and offsets[term_id] == offsets[term_id - 1]) \
                        or (term_id == 0 and offsets[term_id] == 0):
                    byte_count += writer.write_term_id(term_id - offsets[term_id])
                    term_count += 1
                term_id = document.next_term()

            if term_count > 0:
                writer.write_document_info(document.title, document.doc_id - doc_offset, byte_offset, byte_count, term_count)
            else:
                doc_offset += 1

            byte_offset += byte_count
            document = reader.next_document()


class ForwardIndexMetadata(Metadata):
    f_doc_info = "doc_info"
    f_collection = "collection"
    f_terms = "terms"

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

        if ForwardIndexMetadata.f_terms not in self.paths:
            raise_property_not_found(ForwardIndexMetadata.f_terms)
        else:
            self.terms_path = self.paths[ForwardIndexMetadata.f_terms]


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


class ForwardIndexWriter:
    def __init__(self, metadata):
        self.doc_info_writer = io.open(metadata.doc_info_path, 'w')
        self.term_stream = io.open(metadata.collection_path, 'bw')
        self.encoder = metadata.coder_factory.encoder(self.term_stream)

    def write_term_id(self, n):
        return self.encoder.encode(n)

    def write_document_info(self, title, doc_id, offset, byte_count, term_count):
        self.doc_info_writer.write("{0} {1} {2} {3} {4}".format(title, doc_id, offset, byte_count, term_count))

    def close(self):
        self.doc_info_writer.close()
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
