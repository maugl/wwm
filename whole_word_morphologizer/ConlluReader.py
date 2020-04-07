import conllu


class ConlluReader:
    def __init__(self, input_file, output_file=None):
        self.input_file = input_file
        self.output_file = output_file

        self.lexicon = None

        self.read_input()

    def read_input(self):
        self.lexicon = read_conllu_file(self.input_file)

    def write_output(self):
        write_list(self.lexicon, self.output_file)


def read_conllu_file(input_file):
    in_file = open(input_file, "r", encoding="utf-8")
    ud_sentences = conllu.parse_incr(in_file)
    output = set()
    verb_features = ["Number", "Person", "Tense", "VerbForm"]

    for sent in ud_sentences:
        for token in sent.tokens:
            category = ""
            if token["upostag"] == "NOUN":
                category = token["xpostag"]
            elif token["upostag"] == "VERB":
                feats = token["feats"]
                category = "V"
                for v_feat in verb_features:
                    category += feats[v_feat] if v_feat in feats.keys() else ""
                '''elif token["upostag"] == "ADJ":
                    category = token["xpostag"]
                '''
            else:
                continue
            output.add((token["form"].lower(), category))
    in_file.close()
    return list(sorted(output))


def write_list(output, output_file):
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("{}, {}".format(output[0][0], output[0][1]))
        i = 1
        while i < len(output):
            out.write("\n{}, {}".format(output[i][0], output[i][1]))
            i += 1


if __name__ == "__main__":
    in_file = "C:\\Users\\Max\\git\\ReposWS1920\\wwm\\whole_word_morphologizer\\ud-files\\en_gum-ud-dev.conllu"
    out_file = "C:\\Users\\Max\\git\\ReposWS1920\\wwm\\whole_word_morphologizer\\list-files" \
               "\\en_gum-ud-dev-list_test.txt"
    r = ConlluReader(in_file, out_file)
    print(len(r.lexicon))
    r.write_output()