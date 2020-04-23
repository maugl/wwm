from sklearn.model_selection import KFold
import Parser
from itertools import product
import numpy as np


class WwmAnalysis:
    def __init__(self):
        self.parsers = list()
        self.correct_list = list()
        self.number_of_words_in_fold = list()
        self.accuracies = list()
        self.compare = set()

    def run_analysis(self, params=None, folds=6):
        with open("../list-files/bnc_word_list.txt", "r") as f:
            self.compare = set(f.readlines())

        p = Parser.Parser("../list-files/MobyDickList.txt")

        lex = p.lexicon
        np_lex = np.array(lex)

        k_fold = KFold(folds, True)

        bnc_tagset = ["AJ0", "AJC", "AJS", "NN1", "NN2", "VVB", "VVD", "VVG", "VVI", "VVN", "VVZ"]
        upenn_tagset = ["JJ", "JJR", "JJS", "NN", "NNS", "VB", "VBD", "VBG", "VBP", "VBN", "VBZ"]
        upenn_to_bnc = {k: v for k, v in zip(upenn_tagset, bnc_tagset)}

        self.parsers = list()
        self.correct_list = list()
        self.number_of_words_in_fold = list()
        self.accuracies = list()

        for check, test in k_fold.split(np_lex):
            p = Parser.Parser()
            p.lexicon = [(x, y) for x, y in np_lex[test]]

            self.number_of_words_in_fold.append(len(p.lexicon))
            p.params.update(params)

            p.wwm()

            correct = list()
            count_total = len(lex)

            for word in p.generated_new_words:
                if "{},{}\n".format(word[0], upenn_to_bnc[word[1]]) in self.compare:
                    correct.append(word)

            self.parsers.append(p)
            self.correct_list.append(correct)

    def print_stats(self):
        for i in range(len(self.parsers)):
            print("number of words in fold: " + str(self.number_of_words_in_fold[i]))
            print("number of strategies discovered: " + str(len(self.parsers[i].strategies)))
            print("number of new words: " + str(len(self.parsers[i].generated_new_words)))
            print("number of correct words: " + str(len(self.correct_list[i])))
            print("number of total comparison words: " + str(len(self.compare)))
            if len(self.parsers[i].generated_new_words) != 0:
                acc = len(self.correct_list[i]) / len(self.parsers[i].generated_new_words)
            else:
                acc = 0
            print("accuracy: " + str(acc))

    def get_accuracies(self):
        self.accuracies = list()
        for i in range(len(self.parsers)):
            if len(self.parsers[i].generated_new_words) != 0:
                acc = len(self.correct_list[i]) / len(self.parsers[i].generated_new_words)
            else:
                acc = 0
            self.accuracies.append(acc)
        return self.accuracies

    def get_avg_accuracy(self):
        accs = self.get_accuracies()
        return sum(accs)/len(accs)

    def get_avg_strategy_count(self):
        strat_counts = list()
        for p in self.parsers:
            strat_counts.append(len(p.strategies))
        return sum(strat_counts) / len(strat_counts)

    def find_parameters(self):
        begin_sequence_overlap = list(range(2, 3))
        end_sequence_overlap = list(range(3,4))
        comparison_threshold = list(range(15, 18, 1))
        editdistance_threshold = list(range(4, 5))

        params_possible_values = [begin_sequence_overlap, end_sequence_overlap,
                                  comparison_threshold, editdistance_threshold]

        param_names = ["begin_sequence_overlap", "end_sequence_overlap", "comparison_threshold", "editdistance_threshold"]

        param_list = [list(zip(param_names, p)) for p in list(product(*params_possible_values))]

        data = list()
        print(len(param_list))

        for params in [{k: v for k,v in param_vals} for param_vals in param_list]:
            print("====================================================")
            print(params)
            an = WwmAnalysis()
            an.run_analysis(params)

            print("accuracies list: " + str(an.get_accuracies()))
            print("avg accuracy: " + str(an.get_avg_accuracy()))
            print("avg strategy count: " + str(an.get_avg_strategy_count()))

            data.append((params, an.get_accuracies(), an.get_avg_accuracy(), an.get_avg_strategy_count()))

        with open("analysis_data_3.txt", "w", encoding="utf-8") as f:
            for d in data:
                f.write("{}\t{}\t{}\t{}\n".format(d[2], d[3], d[1], d[0]))


if __name__ == "__main__":
    params = {
        "begin_sequence_overlap": 2,
        "end_sequence_overlap": 3,
        "comparison_threshold": 48,
        "editdistance_threshold": 4
    }

    analysis = WwmAnalysis()
    analysis.run_analysis(params=params, folds=2)

    analysis.print_stats()

    print(str(analysis.get_avg_accuracy()))

    # analysis.find_parameters()

