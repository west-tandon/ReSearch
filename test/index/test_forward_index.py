import shutil
import tempfile
import unittest
from os import path

from research.coding.varbyte import Encoder
from research.index.common import IndexFactory


class ForwardIndexReadTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.meta_path = path.join(self.test_dir, 'metadata')
        self.doc_info_path = path.join(self.test_dir, 'doc_info')
        self.collection_path = path.join(self.test_dir, 'collection')
        self.terms_path = path.join(self.test_dir, 'terms')

        f = open(self.meta_path, 'w')
        f.write('''
            {{
                "type" : "research.index.forward.ForwardIndex",
                "name" : "fi",
                "coding": "research.coding.varbyte",
                "paths": {{
                    "doc_info": "{0}",
                    "collection": "{1}",
                    "terms": "{2}"
                }}
            }}
        '''.format(self.doc_info_path, self.collection_path, self.terms_path))
        f.close()

        f = open(self.doc_info_path, 'w')
        f.writelines(["Document1 0 0 3 3\n",
                      "Document2 1 3 3 3\n"])
        f.close()

        f = open(self.terms_path, 'w')
        f.writelines(["0\n",
                      "1\n",
                      "2\n",
                      "3\n",
                      "4\n"])
        f.close()

        f = open(self.collection_path, 'bw')
        self.doc1_terms = [0, 1, 2]
        self.doc2_terms = [3, 4, 2]
        encoder = Encoder(f)
        for term_id in self.doc1_terms + self.doc2_terms:
            encoder.encode(term_id)
        f.close()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_forward_index(self):
        forward_index = IndexFactory.from_path(self.meta_path)
        reader = forward_index.reader()

        with self.subTest(document=1):
            document = reader.next_document()
            self.assertEqual(document.title, "Document1")
            self.assertEqual(document.doc_id, 0)
            self.assertEqual(document.count, 3)
            self.assertEqual(document.next_term_id(), 0)
            self.assertEqual(document.next_term_id(), 1)
            # Intentionally leaving out the next lines
            # self.assertEqual(document.next_term_id(), 2)
            # self.assertEqual(document.next_term_id(), None)

        with self.subTest(document=2):
            document = reader.next_document()
            self.assertEqual(document.title, "Document2")
            self.assertEqual(document.doc_id, 1)
            self.assertEqual(document.count, 3)
            self.assertEqual(document.next_term_id(), 3)
            self.assertEqual(document.next_term_id(), 4)
            self.assertEqual(document.next_term_id(), 2)
            self.assertEqual(document.next_term_id(), None)

        self.assertEqual(reader.next_document(), None)

    def test_forward_index_read_terms(self):
        forward_index = IndexFactory.from_path(self.meta_path)
        reader = forward_index.reader()

        with self.subTest(document=1):
            document = reader.next_document()
            self.assertEqual(document.next_term(), "0")
            self.assertEqual(document.next_term(), "1")
            self.assertEqual(document.next_term(), "2")
            self.assertEqual(document.next_term(), None)

        with self.subTest(document=2):
            document = reader.next_document()
            self.assertEqual(document.next_term(), "3")
            self.assertEqual(document.next_term(), "4")
            self.assertEqual(document.next_term(), "2")
            self.assertEqual(document.next_term(), None)

    def test_forward_index_skip_first(self):
        forward_index = IndexFactory.from_path(self.meta_path)
        reader = forward_index.reader()

        reader.skip(1)
        document = reader.next_document()
        self.assertEqual(document.title, "Document2")
        self.assertEqual(document.doc_id, 1)
        self.assertEqual(document.count, 3)

    def test_forward_index_skip_second(self):
        forward_index = IndexFactory.from_path(self.meta_path)
        reader = forward_index.reader()

        document = reader.next_document()
        reader.skip(1)
        document = reader.next_document()
        self.assertEqual(document, None)

    def test_forward_index_skip_all(self):
        forward_index = IndexFactory.from_path(self.meta_path)
        reader = forward_index.reader()

        reader.skip(2)
        document = reader.next_document()
        self.assertEqual(document, None)

    def test_pruning(self):

        meta_path = path.join(self.test_dir, 'f-metadata')
        doc_info_path = path.join(self.test_dir, 'f-doc_info')
        collection_path = path.join(self.test_dir, 'f-collection')
        terms_path = path.join(self.test_dir, 'f-terms')
        f = open(meta_path, 'w')
        f.write('''
                    {{
                        "type" : "research.index.forward.ForwardIndex",
                        "name" : "ofi",
                        "paths": {{
                            "doc_info": "{0}",
                            "collection": "{1}",
                            "terms": "{2}"
                        }}
                    }}
                '''.format(doc_info_path, collection_path, terms_path))
        f.close()

        forward_index = IndexFactory.from_path(self.meta_path)
        output_index = IndexFactory.from_path(meta_path)

        class TermPruner:
            def test(self, term):
                for ch in term:
                    if ord(ch) > ord("2"):
                        return False
                return True

        forward_index.prune(TermPruner(), output_index)
        reader = output_index.reader()

        document = reader.next_document()
        self.assertEqual(document.title, "Document2")
        self.assertEqual(document.doc_id, 0)
        self.assertEqual(document.count, 2)
        self.assertEqual(document.next_term_id(), 0)
        self.assertEqual(document.next_term_id(), 1)
        self.assertEqual(document.next_term_id(), None)

        self.assertEqual(reader.next_document(), None)
