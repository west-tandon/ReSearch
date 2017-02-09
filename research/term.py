from nltk.stem.snowball import SnowballStemmer


class EnglishStemmer:
    def __init__(self):
        self.stemmer = SnowballStemmer("english")

    def process(self, term):
        return self.stemmer.stem(term)
