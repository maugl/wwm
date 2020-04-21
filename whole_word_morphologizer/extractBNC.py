from xml.etree import ElementTree as et

if __name__ == "__main__":
    corpus = ""
    with open("../bnc_extraction/VNA_raw.xml") as f_in:
        for line in f_in.readlines():
            corpus += line

    xml_tree = et.fromstring(corpus)

    new_lines = set()

    with open("./bnc_word_list.txt", "w", encoding="utf-8") as f:
        for hit in xml_tree.findall(".//w"):
            new_line = "{},{}\n".format(hit.text.lower().strip(), hit.attrib["c5"])
            if new_line not in new_lines:
                f.write(new_line)
                new_lines.add(new_line)