from sklearn.model_selection import KFold
from whole_word_morphologizer import Parser
import numpy as np

if __name__ == "__main__":

    with open("./list-files/bnc_word_list.txt", "r") as f:
        compare = set(f.readlines())

    p = Parser.Parser("./list-files/MobyDickList.txt")

    lex = p.lexicon
    np_lex = np.array(lex)

    k_fold = KFold(6, True)

    bnc_tagset = ["AJ0", "AJC", "AJS", "NN1", "NN2", "VVB", "VVD", "VVG", "VVI", "VVN", "VVZ"]
    upenn_tagset = ["JJ", "JJR", "JJS", "NN", "NNS", "VB", "VBD", "VBG", "VBP", "VBN", "VBZ"]
    upenn_to_bnc = {k: v for k, v in zip(upenn_tagset, bnc_tagset)}

    params = {
        "begin_sequence_overlap": 3,
        "end_sequence_overlap": 3,
        "comparison_threshold": 16,
        "editdistance_threshold": 5
    }

    parsers = list()
    correct_list = list()
    number_of_words_in_fold = list()

    for check, test in k_fold.split(np_lex):
        p = Parser.Parser()
        p.lexicon = [(x, y) for x, y in np_lex[test]]

        number_of_words_in_fold.append(len(p.lexicon))
        p.params.update(params)

        p.wwm()

        correct = list()
        count_total = len(lex)

        for word in p.generated_new_words:
            if "{},{}\n".format(word[0], upenn_to_bnc[word[1]]) in compare:
                correct.append(word)

        parsers.append(p)
        correct_list.append(correct)

    for i in range(len(parsers)):
        print("number of words in fold: " + str(number_of_words_in_fold[i]))
        print("number of strategies discovered: " + str(len(parsers[i].strategies)))
        print("number of new words: " + str(len(parsers[i].generated_new_words)))
        print("number of correct words: " + str(len(correct_list[i])))
        print("number of total comparison words: " + str(len(compare)))
        print("accuracy: " + str(len(correct_list[i])/len(parsers[i].generated_new_words)))
        print("recall: " + str(len(correct_list[i])/len(compare)))
