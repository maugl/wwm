from collections import Counter
from sklearn.model_selection import KFold
from whole_word_morphologizer import Parser
import numpy as np

if __name__ == "__main__":
    p = Parser.Parser("C:/Users/Max/git/ReposWS1920/wwm/whole_word_morphologizer/list-files/MobyDickList.txt")

    lex = p.lexicon
    np_lex = np.array(lex)

    k_fold = KFold(2, True)

    params = {
        "comparison_threshold": 32,
        "editdistance_threshold": 8
    }

    parsers = list()
    correct_list = list()

    for check, test in k_fold.split(np_lex):
        p = Parser.Parser()
        p.lexicon = [(x, y) for x, y in np_lex[test]]
        p.wwm()
        p.params = params
        correct = list()
        count_total = len(lex)
        for word in p.generated_new_words:
            if word in lex:
                correct.append(word)

        parsers.append(p)
        correct_list.append(correct)

    for i in range(len(parsers)):
        print("number of new words: " + str(len(parsers[i].generated_new_words)))
        print("number of correct words: " + str(len(correct_list[i])))
        print("number of total words: " + str(len(lex)))
        print("accuracy: " + str(len(correct_list[i])/len(parsers[i].generated_new_words)))
        print("recall: " + str(len(correct_list[i])/len(lex)))
