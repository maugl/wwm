import unittest


class TestWmm(unittest.TestCase):

    def test_generated_words(self):
        from whole_word_morphologizer.Parser import Parser
        from whole_word_morphologizer.Parser import Parser
        p = Parser("./list-files/en_gum-ud-dev-list.txt")

        p.wwm()

        errors = list()

        for word in p.lexicon:
            try:
                self.assertTrue(word in p.generated_known_words, msg= str(word) + " not generated")
            except AssertionError as e:
                errors.append((word, e))

        print(errors)
        self.assertTrue(len(errors) == 0)
