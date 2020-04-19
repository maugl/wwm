from collections import Counter
from sklearn.model_selection import KFold
from whole_word_morphologizer import Parser
import numpy as np

if __name__ == "__main__":
    p_compare = Parser.Parser("./list-files/mobydick_gum_ewt_total.txt")
    lex_compare = set(p_compare.lexicon)

    p = Parser.Parser("./list-files/MobyDickList.txt")

    lex = p.lexicon
    np_lex = np.array(lex)

    k_fold = KFold(6, True)

    params = {
        "begin_sequence_overlap": 4,
        "end_sequence_overlap": 4,
        "comparison_threshold": 32,
        "editdistance_threshold": 3
    }

    parsers = list()
    correct_list = list()
    number_of_words_in_fold = list()

    for check, test in k_fold.split(np_lex):
        p = Parser.Parser()
        p.lexicon = [(x, y) for x, y in np_lex[test]]

        number_of_words_in_fold.append(len(p.lexicon))

        p.wwm()
        p.params = params
        correct = list()
        count_total = len(lex)

        for word in p.generated_new_words:
            if word in lex_compare:
                correct.append(word)

        parsers.append(p)
        correct_list.append(correct)

    for i in range(len(parsers)):
        print("number of words in fold: " + str(number_of_words_in_fold[i]))
        print("number of new words: " + str(len(parsers[i].generated_new_words)))
        print("number of strategies discovered: " + str(len(parsers[i].strategies)))
        print("number of correct words: " + str(len(correct_list[i])))
        print("number of total comparison words: " + str(len(lex_compare)))
        print("accuracy: " + str(len(correct_list[i])/len(parsers[i].generated_new_words)))
        print("recall: " + str(len(correct_list[i])/len(lex_compare)))
