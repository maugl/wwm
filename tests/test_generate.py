import unittest


class TestGenerate(unittest.TestCase):
    def test_generate1(self):
        from Parser import Parser
        p = Parser("../list-files/testGenerate1.txt")
        p.params["comparison_threshold"] = 1

        p.wwm()
        self.assertTrue(("overlast", "VPresFin")in p.generated_new_words)

    def test_generate2(self):
        from Parser import Parser
        p = Parser("../list-files/testCeiveExample.txt")
        p.params["comparison_threshold"] = 1

        word_to_check = ("deception", "NSing")
        p.lexicon.remove(word_to_check)

        p.wwm()

        self.assertTrue(word_to_check in p.generated_new_words)

    def test_generate3(self):
        from Parser import Parser
        p = Parser("../list-files/compbackwardTest.txt")
        p.params["comparison_threshold"] = 1


        # only overrun, outrun and run works here because take is too long and do is too short
        word_to_check = ("run", "VInf")
        p.lexicon.remove(word_to_check)

        p.wwm()

        self.assertTrue(word_to_check in p.generated_new_words)