import unittest


class TestParser(unittest.TestCase):
    def test_compute_forward1(self):
        from Parser import Parser
        p = Parser("./list-files/compforwardTest.txt")
        p.compute_forward(p.lexicon[0], p.lexicon[1])
        test_result = ("X", "VInf", "Xd", "VPastPart", "outlive#")

        self.assertTrue(test_result[:4] in p.global_comparison_list)
        self.assertEqual((test_result[4],), p.global_comparison_list[test_result[:4]])

    def test_compute_forward2(self):
        from Parser import Parser
        p = Parser("./list-files/testCeiveExample.txt")
        p.compute_forward(p.lexicon[0], p.lexicon[1])
        test_result = ("Xive", "VInf", "Xption", "NSing", "rece#####")

        self.assertTrue(test_result[:4] in p.global_comparison_list)
        self.assertEqual((test_result[4],), p.global_comparison_list[test_result[:4]])

    def test_compute_forward_double_X(self):
        from Parser import Parser
        p = Parser("./list-files/testDoubleX.txt")
        p.compute_forward(p.lexicon[0], p.lexicon[1])

        test_result = ("Xdcee", "VInf", "Xecdd", "VInf", "abbc####")

        self.assertTrue(test_result[:4] in p.global_comparison_list)
        self.assertEqual((test_result[4],), p.global_comparison_list[test_result[:4]])

    def test_compute_backward1(self):
        from Parser import Parser
        p = Parser("./list-files/compbackwardTest.txt")
        p.compute_backward(p.lexicon[0], p.lexicon[1])
        test_result = ("X", "VInf", "outX", "VInf", "###do")

        self.assertTrue(test_result[:4] in p.global_comparison_list)
        self.assertEqual((test_result[4],), p.global_comparison_list[test_result[:4]])

    def test_compute_backward_double_X(self):
        from Parser import Parser
        p = Parser("./list-files/testDoubleX.txt")
        p.compute_backward(p.lexicon[2], p.lexicon[3])

        test_result = ("gffhiX", "VInf", "fgghjX", "VInf", "#####hjj")
        self.assertTrue(test_result[:4] in p.global_comparison_list)
        self.assertEqual((test_result[4],), p.global_comparison_list[test_result[:4]])

    def test_insert_into_global_comparison_list(self):
        from Parser import Parser
        p = Parser("./list-files/overUnderTest.txt")

        test_result = ("w1dif", "w1Cat", "w2dif", "w2Cat", "sim")
        p.insert_into_global_comparison_list(test_result, True)

        self.assertTrue(test_result[:4] in p.global_comparison_list)
        self.assertEqual((test_result[4],), p.global_comparison_list[test_result[:4]])
