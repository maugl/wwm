def get_beginning_sequence_overlap(word1, word2):
    i = 0
    while i < len(word1[0]) and i < len(word2[0]) and word1[0][i] == word2[0][i]:
        i += 1
    return i


def get_ending_sequence_overlap(word1, word2):
    i = 0
    while i < len(word1[0]) and i < len(word2[0]) and \
            word1[0][len(word1[0]) - i - 1] == word2[0][len(word2[0]) - i - 1]:
        i += 1
    return i

