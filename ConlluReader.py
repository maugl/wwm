import conllu


class ConlluReader:
    def __init__(self, input_file, output_file=None):
        self.input_file = input_file
        self.output_file = output_file

        self.lexicon = list()

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
                if feats is None:
                    print(token["form"], token["feats"])
                    continue
                category = "V"
                for v_feat in verb_features:
                    category += feats[v_feat] if v_feat in feats.keys() else ""
            elif token["upostag"] == "ADJ":
                category = token["xpostag"]
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
    in_files = [
        "/home/max/git/WS1819/a12-maugl/ud-treebanks-v2.3/UD_English-GUM/en_gum-ud-dev.conllu",
        "/home/max/git/WS1819/a12-maugl/ud-treebanks-v2.3/UD_English-GUM/en_gum-ud-test.conllu"]

    out_files = [
        "/home/max/git/WS1920/wwm/whole_word_morphologizer/list-files/en_gum-ud-dev.txt",
        "/home/max/git/WS1920/wwm/whole_word_morphologizer/list-files/en_gum-ud-test.txt"
    ]

    compiled_reader = ConlluReader("/home/max/git/WS1819/a12-maugl/ud-treebanks-v2.3/UD_English-GUM/en_gum-ud-train.conllu",
                                   "/list-files/en_gum-ud-train.txt")

    for i, o in zip(in_files[1:], out_files[1:]):
        r = ConlluReader(i, o)
        print(len(r.lexicon))
        compiled_reader.lexicon.extend(r.lexicon)

    compiled_reader.output_file = "/list-files/en_gum-ud-total.txt"
    compiled_reader.write_output()