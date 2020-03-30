from collections import Counter
from whole_word_morphologizer.util import get_ending_sequence_overlap, get_beginning_sequence_overlap
import re
import editdistance


class Parser:
    def __init__(self, word_list_file):
        self.lexicon = list()
        self.comparison_count = dict()
        self.global_comparison_list = dict()
        self.strategies = set()

        self.generated_known_words = set()
        self.generated_new_words = set()
        self.generation_used_strategies = dict()

        self.params = {
            "begin_sequence_overlap": 2,
            "end_sequence_overlap": 2,
            "comparison_threshold": 3,
            "same_segment": "X",
            "one_char": "#",
            "zero_one_char": "*",
            "editdistance_threshold": 5
        }

        self.read_lexicon(word_list_file)

    def wwm(self):
        self.comparison_count = dict()
        self.global_comparison_list = dict()
        # TODO no need to fully loop over lexicon if generate works bidirectional
        for w1 in self.lexicon:
            for w2 in self.lexicon:
                # differing from original code, but same words may not be compared
                if w1 == w2:
                    continue
                # In practice, only those pairs of words
                # which are by some heuristic sufficiently similar in
                # the first place are compared.
                if get_beginning_sequence_overlap(w1, w2) >= self.params["begin_sequence_overlap"]:
                    if editdistance.distance(w1[0], w2[0]) < self.params["editdistance_threshold"]:
                        self.compute_forward(w1, w2)
                # why not check both? back and forward?
                elif get_ending_sequence_overlap(w1, w2) >= self.params["end_sequence_overlap"]:
                    if editdistance.distance(w1[0], w2[0]) < self.params["editdistance_threshold"]:
                        self.compute_backward(w1, w2)
                # print(self.global_comparison_list)
        # add newly found strategies to the set of strategies
        self.strategies = self.strategies.union(set([k + v for k, v in self.global_comparison_list.items() if
                                                     self.comparison_count[k] >= self.params["comparison_threshold"]]))
        known_words, new_words, used_strategies = self.generate()

        self.generated_known_words = known_words
        self.generated_new_words = new_words
        self.generation_used_strategies = used_strategies

    def compute_forward(self, word1, word2):
        self.insert_into_global_comparison_list(self.generate_comparison(word1, word2, True), True)

    def compute_backward(self, word1, word2):
        self.insert_into_global_comparison_list(self.generate_comparison(word1, word2, False), False)

    def generate_comparison(self, word1, word2, forward):
        orth1 = word1[0]
        orth2 = word2[0]

        if not forward:
            orth1 = orth1[::-1]
            orth2 = orth2[::-1]
            overlap = get_ending_sequence_overlap(word1, word2)
        else:
            overlap = get_beginning_sequence_overlap(word1, word2)

        dif_w1 = self.params["same_segment"] + orth1[overlap:]
        dif_w2 = self.params["same_segment"] + orth2[overlap:]
        sim = orth1[:overlap] + (max(len(orth1), len(orth2)) - overlap) * self.params["one_char"]

        if not forward:
            dif_w1 = dif_w1[::-1]
            dif_w2 = dif_w2[::-1]
            sim = sim[::-1]

        return dif_w1, word1[1], dif_w2, word2[1], sim

    def insert_into_global_comparison_list(self, comparison, forward):
        if comparison[:4] in self.global_comparison_list.keys():
            self.merge(comparison, forward)
            self.comparison_count[comparison[:4]] += 1
        else:
            self.global_comparison_list[comparison[:4]] = (comparison[4],)
            self.comparison_count[comparison[:4]] = 1

    def merge(self, comparison, forward):
        '''
        Split the similarities into two parts. And then compare the difference part back to front, in order to determine
        same substrings between words.

        Example forward:
            ('Xive', 'VInf', 'Xption', 'NSing', 'conce#####')
            ('Xive', 'VInf', 'Xption', 'NSing', 'rece#####')
            remove same part and reverse: ecer - ecnoc

            check for similarities between the strings outward from the cut

            new different part: *##ce
            old same part: #####
            new similarity string: '*##ce#####'

        Example backward:


        :param comparison: 
        :param forward: 
        :return: 
        '''
        list_comparison = comparison[:4] + self.global_comparison_list[comparison[:4]]
        sim_same_len = max(len(comparison[0])-len(self.params["same_segment"]),
                           len(comparison[2])-len(self.params["same_segment"]))
        new_sim = ""

        #print(list_comparison)
        #print(comparison)

        if forward:
            # forward merge
            # reverse order of checking
            list_sim = list_comparison[4][:-sim_same_len][::-1]
            merge_sim = comparison[4][:-sim_same_len][::-1]
            same_part = list_comparison[4][-sim_same_len:]
        else:
            # bacwards merge
            list_sim = list_comparison[4][sim_same_len:]
            merge_sim = comparison[4][sim_same_len:]
            same_part = list_comparison[4][:sim_same_len]

        #print(list_sim)
        #print(merge_sim)

        for i, char in enumerate(list_sim):
            if i < len(merge_sim):
                if char == merge_sim[i]:
                    new_sim += char
                elif (char == self.params["one_char"] and merge_sim[i] == self.params["zero_one_char"]) or \
                        (char == self.params["zero_one_char"] and self.params["one_char"]):
                    new_sim += self.params["zero_one_char"]
                else:
                    new_sim += self.params["one_char"]
            else:
                new_sim += self.params["zero_one_char"]
        if len(merge_sim) > len(list_sim):
            new_sim += (len(merge_sim) - len(list_sim)) * self.params["zero_one_char"]

        #print("new: " +  new_sim[::-1] if forward else new_sim)
        #print((new_sim[::-1] + same_part if forward else same_part + new_sim,))
        self.global_comparison_list[comparison[:4]] = (new_sim[::-1] + same_part if forward else same_part + new_sim,)

    def read_lexicon(self, word_list_file):
        with open(word_list_file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                contents = line.strip("\n").split(",")
                word = (contents[0].strip().lower(), contents[1].strip())
                if word not in self.lexicon:
                    self.lexicon.append(word)
        self.lexicon = list(self.lexicon)

    def generate(self):
        newly_generated_words = set()
        known_generated_words = set()
        strats_used = dict()
        # TODO loop lexicon first???
        for strat in self.strategies:
            w1dif = strat[0]
            w2dif = strat[2]
            len_dif_segment = max(len(w1dif), len(strat[2])) - len(self.params["same_segment"])
            if w1dif.startswith(self.params["same_segment"]) and w2dif.startswith(self.params["same_segment"]):
                #input check from front
                w1dif = w1dif.replace(self.params["same_segment"], "")
                search_re = strat[4][:len_dif_segment] + w1dif

                # output check
                w2dif = w2dif.replace(self.params["same_segment"], "")
                output_re = strat[4][:len_dif_segment] + w2dif

            elif w1dif.endswith(self.params["same_segment"]) and w2dif.endswith(self.params["same_segment"]):
                #input check from back
                w1dif = w1dif.replace(self.params["same_segment"], "")
                search_re = w1dif + strat[4][len_dif_segment:]

                #output check
                w2dif = w2dif.replace(self.params["same_segment"], "")
                output_re = w2dif + strat[4][len_dif_segment:]
            else:
                # in case no "same_segment" is found. should not happen
                continue

            search_re = search_re.replace(self.params["zero_one_char"], "\\w?").replace(self.params["one_char"], "\\w")
            s_regex = re.compile(search_re)

            output_re = output_re.replace(self.params["zero_one_char"], "\\w?").replace(self.params["one_char"], "\\w")
            o_regex = re.compile(output_re)

            for word in self.lexicon:
                if s_regex.fullmatch(word[0]) and word[1] == strat[1]:
                    new_word = strat[2].replace(self.params["same_segment"], word[0].replace(w1dif, "")), strat[3]
                    if o_regex.fullmatch(new_word[0]):
                        if new_word in self.lexicon:
                            known_generated_words.add(new_word)
                        else:
                            newly_generated_words.add(new_word)
                        if new_word not in strats_used:
                            strats_used[new_word] = [strat + (search_re, output_re)]
                        else:
                            strats_used[new_word].append(strat + (search_re, output_re))

        return known_generated_words, newly_generated_words, strats_used


if __name__ == "__main__":
    p = Parser("./list-files/en_gum-ud-dev-list.txt")
    print(p.lexicon[:25])