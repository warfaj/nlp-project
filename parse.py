import re
import nltk
from nltk.corpus import wordnet as wn

# makes word lower-case, removes punctuation
# allows the word to be stored in a dictionary better
def strip(word):
    w = word.lower()
    w = re.sub('[.!? ,:"\']', '', w)
    return w

def splitsentence(sentence):
    words = re.findall(r"[\w']+", sentence)
    for i in xrange(len(words)):
        words[i] = strip(words[i])
    return words

class Parse:

    # initialization functions, takes in a string of text
    def __init__(self, raw_text):
        # lines = text.splitlines() # list of text line split by newline delimeter
        dictionary = {} # maps words to indices
        sentences = re.split('(?<=[.!?\n])\n+|(?<=[.!?\n]) +', raw_text) # list that maps indices to sentences
        self.dictionary = dictionary
        self.sentences = sentences
        for i in xrange(len(sentences)):
            words = splitsentence(sentences[i])
            for word in words:
                if word.isdigit():
                    token = word
                else:
                    token = wn.morphy(word.strip().decode("ascii","ignore").encode("ascii"))
                if token in dictionary:
                    dictionary[token].add(i)
                else:
                    dictionary[token] = {i}

    # given a word, returns all indices of sentences that contain the word
    def findword_sym(self, word):
        if word.isdigit():
            w = word
        else:
            w = wn.morphy(strip(word))

        syns = wn.synsets(word)
        sents = set([])
        syn_lemmas = []
        for synset in syns:
            syn_lemmas+=synset.lemmas()
        words = set([s.name() for s in syn_lemmas])
        for syn in words:
            if syn in self.dictionary:
                sents.update(self.dictionary[syn])
        return set(sents)

    def findword(self, word):
        if word.isdigit():
            w = word
        else:
            w = wn.morphy(strip(word))

        if w in self.dictionary:
            return self.dictionary[w]

        return set()

    # given a list of words, returns all indices of sentences containing all the words
    def findwords(self, words):
        if len(words) == 0:
            return set()
        indices = self.findword(words[0])
        for word in words[1:]:
            idxs = self.findword(word)
            indices = set.intersection(indices,idxs)
        return indices

    # given a string of words, returns all indices of sentences containing all the words
    def findsentence(self, sentence):
        words = splitsentence(sentence)
        return self.findwords(words)

    # given an index, returns the sentence
    def findidx(self, i):
        if 0 <= i and i < len(self.sentences):
            return self.sentences[i]
        else:
            return ''
