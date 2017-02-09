import unittest
import shutil
import tempfile
import os
from research.lexicon import ArrayLexicon


class LexiconTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.terms_path = os.path.join(self.test_dir, "terms")
        with open(self.terms_path, 'w') as term_file:
            term_file.write("a\nz\nc\nb\n")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_array_lexicon(self):
        lex = ArrayLexicon(self.terms_path)

        expected = [
            (0, "a"),
            (1, "z"),
            (2, "c"),
            (3, "b")
        ]
        for idx, term in expected:
            self.assertEqual(term, lex[idx])
            self.assertEqual(idx, lex[term])