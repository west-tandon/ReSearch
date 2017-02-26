import io

from research.index.common import IndexMetadata, load_numbers, read_header, resolve_decoder
from research.lexicon import ArrayLexicon


class Index:
    def __init__(self, properties):
        self.metadata = IndexMetadata(properties)

    def reader(self) -> 'IndexReader':
        return IndexReader(self.metadata)


class IndexReader:
    def __init__(self, metadata: IndexMetadata):
        self.metadata = metadata
        self.current_term = 0
        self.frequencies = load_numbers(self.metadata.frequencies_path())
        self.lexicon = ArrayLexicon(self.metadata.terms_path())
        self.num_terms = self.lexicon.count()

        self.docs_offsets = load_numbers(self.metadata.docs_offsets_path())
        self.docs_stream = open(self.metadata.docs_path(), 'br')
        self.docs_header, self.docs_init_offset = read_header(self.docs_stream)

        self.counts_offsets = load_numbers(self.metadata.counts_offsets_path())
        self.counts_stream = open(self.metadata.counts_path(), 'br')
        self.counts_header, self.counts_init_offset = read_header(self.counts_stream)
        self.open = True

    def next(self):
        assert self.open, "the reader has been closed"
        if self.current_term >= self.num_terms:
            return None
        else:
            self.current_term += 1
            self.docs_stream.seek(
                self.docs_init_offset + self.docs_offsets[self.current_term] - self.docs_stream.tell(),
                io.SEEK_CUR)
            self.counts_stream.seek(
                self.counts_init_offset + self.counts_offsets[self.current_term] - self.counts_stream.tell(),
                io.SEEK_CUR)
            return InvertedListReader(self, self.frequencies[self.current_term])

    def documents(self, term=None, term_id=None):
        assert (term is not None and term_id is None) or (term is None and term_id is not None),\
            "you must define either term or term_id"
        assert term is None or term != '', "term cannot be an empty string"
        assert self.open, "the reader has been closed"

        # Resolve term ID
        if term is not None:
            term_id = self.lexicon.idx(term)
            if term_id is None:
                return None

        self.docs_stream.seek(self.docs_init_offset + self.docs_offsets[term_id])
        self.counts_stream.seek(self.counts_init_offset + self.counts_offsets[term_id])
        self.current_term = term_id
        return InvertedListReader(self, self.frequencies[term_id], term)

    def close(self):
        self.docs_stream.close()
        self.counts_stream.close()
        self.open = False


class InvertedListReader:
    def __init__(self, index_reader, frequency, term=None):
        self.index_reader = index_reader
        self.docs_decoder = resolve_decoder(index_reader.docs_header, index_reader.docs_stream)
        self.counts_decoder = resolve_decoder(index_reader.counts_header, index_reader.counts_stream)
        self.frequency = frequency
        self.at_idx = 0
        self.last_id = 0

        self.term = term
        """ The term of the currently processed list (if available, otherwise None) """

        self.count = None
        """ the number of occurrences of the term in the most recently retrieved document """

    def next_doc(self):
        if self.at_idx >= self.frequency:
            self.count = None
            return None
        else:
            self.last_id += self.docs_decoder.decode()
            self.count = self.counts_decoder.decode()
            self.at_idx += 1
            return self.last_id

    def next_ge(self, id):
        """
        Move to the next greater or equal ID.
        Never goes back, to look up a smaller value, open a new InvertedListReader.
        :param id: the lookup ID
        :return: the first ID greater or equal to 'id' or None
        """
        if self.at_idx == 0:
            self.last_id = -1
        while self.last_id is not None and self.last_id < id:
            self.last_id = self.next_doc()
        return self.last_id


class IndexBuilder:
    def build(self, properties, inpt):
        pass
