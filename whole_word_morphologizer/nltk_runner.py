import nltk
from whole_word_morphologizer.ConlluReader import write_list
import re

with open("/MobyDick.txt", "r", encoding="utf-8") as f:
    text = f.read()

md_tokenized = nltk.word_tokenize(text=text, language="english")
md_tagged = nltk.pos_tag(md_tokenized)
tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "JJ", "JJR", "JJS", "NNS", "NN"]
md_tagged_filtered = {(orth.lower(), cat) for orth, cat in md_tagged if cat in tags}

md_tagged_filtered_reduced = [(orth, cat) for orth, cat in md_tagged_filtered if re.fullmatch("[A-Za-z]*", orth) is not None]

write_list(list(sorted(md_tagged_filtered_reduced)),
           "/list-files/MobyDickListTest.txt")