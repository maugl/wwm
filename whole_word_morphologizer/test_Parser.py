from unittest import TestCase


class TestParser(TestCase):
    def test_compute_forward1(self):
        from whole_word_morphologizer.Parser import Parser
        p = Parser("./list-files/compforwardTest.txt")
        p.compute_forward(p.lexicon[0], p.lexicon[1])
        test_result = ("X", "VInf", "Xd", "VPastPart", "outlive#")

        assert(test_result[:4] in p.global_comparison_list)
        assert((test_result[4],) == p.global_comparison_list[test_result[:4]])

    def test_compute_forward2(self):
        from whole_word_morphologizer.Parser import Parser
        p = Parser("./list-files/testCeiveExample.txt")
        p.compute_forward(p.lexicon[0], p.lexicon[1])
        test_result = ("Xive", "VInf", "Xption", "NSing", "rece#####")

        assert(test_result[:4] in p.global_comparison_list)
        assert((test_result[4],) == p.global_comparison_list[test_result[:4]])

    def test_compute_forward_double_X(self):
        from whole_word_morphologizer.Parser import Parser
        p = Parser("./list-files/testDoubleX.txt")
        p.compute_forward(p.lexicon[0], p.lexicon[1])

        test_result = ("Xcdcee", "VInf", "Xcecdd", "VInf", "abb#####")
        assert(test_result[:4] in p.global_comparison_list)
        assert((test_result[4],) == p.global_comparison_list[test_result[:4]])

    def test_compute_backward1(self):
        from whole_word_morphologizer.Parser import Parser
        p = Parser("./list-files/compbackwardTest.txt")
        p.compute_backward(p.lexicon[0], p.lexicon[1])
        test_result = ("X", "VInf", "outX", "VInf", "###do")

        assert(test_result[:4] in p.global_comparison_list)
        assert((test_result[4],) == p.global_comparison_list[test_result[:4]])

    def test_compute_backward_double_X(self):
        from whole_word_morphologizer.Parser import Parser
        p = Parser("./list-files/testDoubleX.txt")
        p.compute_backward(p.lexicon[2], p.lexicon[3])

        test_result = ("gffhiX", "VInf", "fgghjX", "VInf", "#####hjj")
        assert(test_result[:4] in p.global_comparison_list)
        assert((test_result[4],) == p.global_comparison_list[test_result[:4]])

    def test_insert_into_global_comparison_list(self):
        from whole_word_morphologizer.Parser import Parser



