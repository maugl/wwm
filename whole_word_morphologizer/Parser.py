from collections import Counter
from whole_word_morphologizer.util import get_ending_sequence_overlap, get_beginning_sequence_overlap
import re

class Parser:
    def __init__(self, word_list_file):
        self.lexicon = list()
        self.comparison_count = dict()
        self.global_comparison_list = dict()
        self.strategies = set()

        self.params = {
            "begin_sequence_overlap": 2,
            "end_sequence_overlap": 2,
            "comparison_threshold": 3,
            "same_segment": "X",
            "one_char": "#",
            "zero_one_char": "*"
        }

        self.read_lexicon(word_list_file)

    def wwm(self):
        self.comparison_count = dict()
        self.global_comparison_list = dict()
        for w1 in self.lexicon:
            for w2 in self.lexicon:
                if get_beginning_sequence_overlap(w1, w2):
                    self.compute_forward(w1, w2)
                # why not check both?
                elif get_ending_sequence_overlap(w1, w2):
                    self.compute_backward(w1, w2)
        # add newly found strategies to the set of strategies
        self.strategies = self.strategies.union(set([k + v for k, v in self.global_comparison_list.items() if
                                                     self.comparison_count[k] >= self.params["comparison_threshold"]]))
        self.generate()

    def compute_forward(self, word1, word2):
        # (0,       1,      2       3,      4
        # [w1dif,   w1cat,  w2dif,  w2cat,  sim]
        comparison = ["", word1[1],"", word2[1], ""]
        orth1 = word1[0]
        orth2 = word2[0]

        i = 0
        while i < len(orth2):
            if i < len(orth1) and orth1[i] == orth2[i]:
                comparison[4] += orth1[i]
                if comparison[0][-1:] != self.params["same_segment"]:
                    comparison[0] += self.params["same_segment"]
                    comparison[2] += self.params["same_segment"]
            else:
                comparison[0] += orth1[i] if i < len(orth1) else ""
                comparison[2] += orth2[i]
                comparison[4] += self.params["one_char"] if i < len(orth1) else self.params["zero_one_char"]

            i += 1
        if len(orth1) > len(orth2):
            comparison[0] += orth1[len(orth2):]
            comparison[4] += (len(orth1) - len(orth2)) * self.params["zero_one_char"]

        self.insert_into_global_comparison_list(tuple(comparison))

    def compute_backward(self, word1, word2):
        # might be included into a helper function include(word1, word2, ["forward", "backward"])
        # that way only one implementation only changing i to -i in some way
        # just need to reverse all comparison values in the end

        comparison = ["", word1[1], "", word2[1], ""]
        orth1 = word1[0]
        orth2 = word2[0]

        i = 1
        while i <= len(orth2):
            if i <= len(orth1) and orth1[-i] == orth2[-i]:
                comparison[4] = orth1[-i] + comparison[4]
                if comparison[0][0:1] != self.params["same_segment"]:
                    comparison[0] = self.params["same_segment"] + comparison[0]
                    comparison[2] = self.params["same_segment"] + comparison[2]
            else:
                comparison[0] = orth1[-i] + comparison[0] if i <= len(orth1) else comparison[0]
                comparison[2] = orth2[-i] + comparison[2]
                comparison[4] = self.params["one_char"] + comparison[4] \
                    if i <= len(orth1) else self.params["zero_one_char"] + comparison[4]
            i += 1
        if len(orth1) > len(orth2):
            comparison[0] = orth1[:len(orth1) - len(orth2)] + comparison[0]
            comparison[4] = (len(orth1) - len(orth2)) * self.params["zero_one_char"] + comparison[4]

        self.insert_into_global_comparison_list(tuple(comparison))

    def insert_into_global_comparison_list(self, comparison):
        if comparison[:4] in self.global_comparison_list.keys():
            self.merge(comparison)
            self.comparison_count[comparison[:4]] += 1
        else:
            self.global_comparison_list[comparison[:4]] = (comparison[4],)
            self.comparison_count[comparison[:4]] = 1

    def merge(self, comparison):
        list_sim = self.global_comparison_list[comparison[:4]][0]
        merge_sim = comparison[4]
        new_sim = ""

        if list_sim[0] == self.params["one_char"] or list_sim[0] == self.params["zero_one_char"]:
            # forwards merge
            backwards = False
        else:
            # bacwards merge
            list_sim = list_sim[::-1]
            merge_sim = merge_sim[::-1]
            backwards = True

        for i, char in enumerate(list_sim):
            if i >= len(merge_sim[i]):
                if char == merge_sim[i]:
                    new_sim = char
                elif (char == self.params["one_char"] and merge_sim[i] == self.params["zero_one_char"]) or \
                        (char == self.params["zero_one_char"] and self.params["one_char"]):
                    new_sim += self.params["zero_one_char"]
                else:
                    new_sim += self.params["one_char"]
            else:
                new_sim += self.params["zero_one_char"]
        if len(merge_sim) > len(list_sim):
            new_sim += (len(merge_sim) - len(list_sim)) * self.params["zero_one_char"]

        self.global_comparison_list[comparison[:4]] = (new_sim[::-1] if backwards else new_sim,)

    def read_lexicon(self, word_list_file):
        with open(word_list_file, "r") as f:
            for line in f.readlines():
                contents = line.strip("\n").split(",")
                self.lexicon.append((contents[0].strip().lower(), contents[1].strip()))

    def check_beginning_sequence_overlap(self, word1, word2):
        char_ind = 0
        while char_ind < self.params["begin_sequence_overlap"]:
            if word1[0][char_ind] != word2[0][char_ind]:
                return False
            char_ind += 1
        return True

    def check_ending_sequence_overlap(self, word1, word2):
        char_ind = 1

        while char_ind <= self.params["end_sequence_overlap"]:
            if word1[0][len(word1)-char_ind] != word2[0][len(word2)-char_ind]:
                return False
            char_ind += 1
        return True

    def generate(self):
        for strat in self.strategies:
            w1dif = strat[0]
            if w1dif.startswith(self.params["same_segment"]):
                w1dif = w1dif.replace(self.params["same_segment"], "")
                search_re = strat[4][len(w1dif):] + w1dif
            elif w1dif.endswith(self.params["same_segment"]):
                w1dif = w1dif.replace(self.params["same_segment"], "")
                search_re = w1dif + strat[4][len(w1dif):]
            else:
                continue
            # search_re = search_re.replace(self.params["zero_one_char"], "\w?").replace(self.params["one_char"], "\w")
            print(search_re)

if __name__ == "__main__":
    p = Parser("./list-files/en_gum-ud-dev-list.txt")
    print(p.lexicon[:25])