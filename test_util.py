from unittest import TestCase


class Test(TestCase):
    def test_get_beginning_sequence_overlap1(self):
        from util import get_beginning_sequence_overlap
        assert(get_beginning_sequence_overlap(("word1", ""), ("word2", "")) == 4)

    def test_get_beginning_sequence_overlap2(self):
        from util import get_beginning_sequence_overlap
        assert (get_beginning_sequence_overlap(("west1", ""), ("word1", "")) == 1)

    def test_get_beginning_sequence_overlap3(self):
        from util import get_beginning_sequence_overlap
        assert(get_beginning_sequence_overlap(("test1", ""), ("word2", "")) == 0)

    def test_get_beginning_sequence_overlap4(self):
        from util import get_beginning_sequence_overlap
        assert(get_beginning_sequence_overlap(("", ""), ("", "")) == 0)

    def test_get_ending_sequence_overlap1(self):
        from util import get_ending_sequence_overlap
        assert(get_ending_sequence_overlap(("1word", ""), ("2word", "")) == 4)

    def test_get_ending_sequence_overlap2(self):
        from util import get_ending_sequence_overlap
        assert(get_ending_sequence_overlap(("1word", ""), ("1tesd", "")) == 1)

    def test_get_ending_sequence_overlap3(self):
        from util import get_ending_sequence_overlap
        assert(get_ending_sequence_overlap(("1test", ""), ("2word", "")) == 0)

    def test_get_ending_sequence_overlap4(self):
        from util import get_ending_sequence_overlap
        assert(get_ending_sequence_overlap(("", ""), ("", "")) == 0)
