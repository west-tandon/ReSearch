class BigUnicodePruner:

    def test(self, term):
        for ch in term:
            if ord(ch) > 2048:
                return False
        return True

# TODO:
# class PrunerBuilder:
#
#     def addTermPruner(self, termPruner):
#         pass
#
#     def addCharacterPrunner(self, characterPrunner):
#         pass

