import unittest
from research.term import EnglishStemmer


class TermTest(unittest.TestCase):

    def test_english_stemmer(self):
        processor = EnglishStemmer()
        pairs = [
            ("consigning", "consign"),
            ("conspired", "conspir"),
            ("cat", "cat"),
            ("cats", "cat")
        ]
        for term, stemmed in pairs:
            self.assertEqual(stemmed, processor.process(term))