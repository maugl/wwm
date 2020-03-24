import conllu

input_file = "./ud-files/en_gum-ud-dev.conllu"
output_file = "./list-files/en_gum-ud-dev-list.txt"

in_file = open(input_file, "r", encoding="utf-8")
ud_sentences = conllu.parse_incr(in_file)

keep_tokens = list()
output = set()

verb_features = ["Number", "Person", "Tense", "VerbForm"]

for sent in ud_sentences:
    for token in sent.tokens:
        if token["upostag"] == "NOUN" or token["upostag"] == "VERB":
            keep_tokens.append(token)

for token in keep_tokens:
    category = ""
    if token["upostag"] == "NOUN":
        category = token["xpostag"]

    if token["upostag"] == "VERB":
        feats = token["feats"]
        category = "V"
        for v_feat in verb_features:
            category += feats[v_feat] if v_feat in feats.keys() else ""

    output.add((token["form"], category))
in_file.close()

with open(output_file, "w", encoding="utf-8") as out:
    for orth, tag in list(output):
        out.write("{}, {}\n".format(orth, tag))