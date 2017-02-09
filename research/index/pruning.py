from nltk.corpus import stopwords


class BigUnicodePruner:

    def test(self, term):
        for ch in term:
            if ord(ch) > 2048:
                return False
        return True


class EnglishStopWordsPruner:
    def __init__(self):
        self.stopwords = set(stopwords.words('english'))

    def test(self, term):
        return term not in self.stopwords

