from abc import ABCMeta, abstractmethod
import bisect


class AbstractLexicon(metaclass=ABCMeta):
    @abstractmethod
    def term(self, idx):
        pass

    @abstractmethod
    def idx(self, term):
        pass

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.term(key)
        else:
            return self.idx(key)


class ArrayLexicon(AbstractLexicon):

    def __init__(self, file):
        with open(file, 'r') as f:
            self.terms = [(term[:-1], idx) for idx, term in enumerate(f.readlines())]
            self.terms.sort()
            self.map = [0 for x in range(len(self.terms))]
            for i, (term, idx) in enumerate(self.terms):
                self.map[idx] = i

    def term(self, idx):
        return self.terms[self.map[idx]][0]

    def idx(self, term):
        i = bisect.bisect_left(self.terms, (term, -1))
        if i != len(self.terms) and self.terms[i][0] == term:
            return self.terms[i][1]
        else:
            return None

    def count(self):
        return len(self.terms)