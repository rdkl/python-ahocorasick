#!/usr/bin/env python
# *- coding: utf-8 -*-

try:
    import AhoCorasick64 as AhoCorasick
except:
    print "64-bit AhoCorasick lib not found."
    try:
        import AhoCorasick32 as AhoCorasick
    except:
        print "32-bit AhoCorasick lib not found."

################################################################################
class Matcher(object):
    """ 
    A wrapper for Aho-Corasick from libs.
    """
    def __init__(self, filename="./data/words.txt"):
        self.__matcher = AhoCorasick.Matcher()
        self.__matcher.Init(filename)
        self.__dict = {}
        self.__ReadWords(filename)
        
    # --------------------------------------------------------------------------
    def __ReadWords(self, filename):
        with open(filename, "r") as f:
            word_number = 0
            for line in f.readlines():
                # First line has length ~5, if file was created in other OS.
                if len(line) > 0:
                    self.__dict[word_number] = line[:-1]
                    word_number += 1
                    
    # --------------------------------------------------------------------------
    def FindWordsInText(self, text):
        return self.__matcher.FindWordsInText(" " + text + " ")
    
    # --------------------------------------------------------------------------
    def FindWordsInTextWithPositions(self, text):
        pos = self.__matcher.FindWordsInTextWithPositions(" " + text + " ")
        result = {}
        for word_index in pos:
            result[word_index] = []
            # print word_index, pos[word_index]
            for index in pos[word_index]:
                result[word_index].append(pos[word_index][index] - \
                                          len(self.__dict[word_index]) - 2)

        return result

    # --------------------------------------------------------------------------
    # Works much faster than FindWordsInTextWithPositions (about 60% faster).
    # def FindWordsInTextWithPositionsByEnd(self, text):
    #    return self.__matcher.FindWordsInTextWithPositions(" " + text + " ")
    #
    # --------------------------------------------------------------------------
    def GetDict(self):
        return self.__dict
    
    # --------------------------------------------------------------------------
################################################################################

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    f = open("./data/words.txt", "w")
    words = ["super", "by", "a", "returned"]
    for word in words:
        print >>f, word
    f.close()

    m = Matcher(filename="./data/words.txt")
    text = "Recall measures the quantity of relevant results returned by a " \
           "search, while precision is the measure of the quality of the " \
           "results returned. Recall is the ratio of relevant results returned " \
           "to all relevant results. Precision is the number of relevant " \
           "results returned to the total number of results returned."

    a = m.FindWordsInTextWithPositions(text)
    dict = m.GetDict()
    print dict
    for item in a:
        print dict[item], a[item], \
            "|" + text[a[item][0]:a[item][0] + len(dict[item])] + "|"
