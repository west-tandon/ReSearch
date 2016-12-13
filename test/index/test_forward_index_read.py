import unittest
import shutil
import tempfile
from research.coding.varbyte import Encoder
from research.index.forward import ForwardIndex
import research.index.forward as forward
from os import path


class ForwardIndexReadTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.meta_path = path.join(self.test_dir, 'metadata')
        self.doc_info_path = path.join(self.test_dir, 'doc_info')
        self.collection_path = path.join(self.test_dir, 'collection')

        f = open(self.meta_path, 'w')
        f.write('''
            {{
                "paths": {{
                    "doc_info": "{0}",
                    "collection": "{1}"
                }}
            }}
        '''.format(self.doc_info_path, self.collection_path))
        f.close()

        f = open(self.doc_info_path, 'w')
        f.writelines(["Document1 0 0 3 3\n",
                      "Document2 1 3 3 3\n"])
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
        forward_index = ForwardIndex.load(self.meta_path)
        reader = forward_index.reader()

        with self.subTest(document=1):
            document = reader.next_document()
            self.assertEqual(document.title, "Document1")
            self.assertEqual(document.doc_id, 0)
            self.assertEqual(document.count, 3)
            self.assertEqual(document.next_term(), 0)
            self.assertEqual(document.next_term(), 1)
            self.assertEqual(document.next_term(), 2)
            self.assertEqual(document.next_term(), None)

        with self.subTest(document=2):
            document = reader.next_document()
            self.assertEqual(document.title, "Document2")
            self.assertEqual(document.doc_id, 1)
            self.assertEqual(document.count, 3)
            self.assertEqual(document.next_term(), 3)
            self.assertEqual(document.next_term(), 4)
            self.assertEqual(document.next_term(), 2)
            self.assertEqual(document.next_term(), None)

        self.assertEqual(reader.next_document(), None)