import os
import re
from nltk.parse import stanford
from nltk import word_tokenize, pos_tag
from nltk.tag.stanford import StanfordNERTagger

#dir = '/Users/Warfa/Desktop/nlp-project/'
dir = ''



# given a string of raw text, creates a object for all the sentences
class Sentences:
    def __init__(self, raw_sentences):
        # modify raw_sentences to contain contain ascii characters
        raw_asciis = raw_sentences.strip().decode("ascii","ignore").encode("ascii")
        # list of sentences and tokenized sentences, respectively
        self.sentences = re.split('(?<=[.!?])\n+|(?<=[.!?]) +', raw_asciis)
        self.tokenized_sents = [word_tokenize(sent) for sent in self.sentences]
        # number of sentences
        self.size = len(self.sentences)
        # list of sentences, parse trees, ner_tags, and pos_tags, respectively
        self.parses = get_parses(self.sentences)
        self.ner_tags = get_ner_tags(self.tokenized_sents)
        self.pos_tags = get_pos_tags(self.tokenized_sents)



# given a list of sentences, returns a list of parse trees
def get_parses(sentences):
    os.environ['CLASSPATH'] = dir+'stanford-parser'
    os.environ['STANFORD_PARSER'] = dir+'stanford-parser/stanford-parser.jar'
    os.environ['STANFORD_MODELS'] = dir+'stanford-parser/stanford-parser-3.6.0-models.jar'
    parser = stanford.StanfordParser(model_path=dir+"stanford-parser/models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    iter_trees = parser.raw_parse_sents(sentences) # this line might take quite a few seconds if the file size is large
    list_trees = []
    for iter_tree in iter_trees:
        for tree in iter_tree:
            list_trees.append(tree)
    return list_trees

# given a list of tokenized sentences, returns a list of ner_tags
def get_ner_tags(tokenized_sents):
    os.environ['CLASSPATH'] = dir+'stanford-ner'
    return StanfordNERTagger(dir+'stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz').tag_sents(tokenized_sents)

# given a list of tokenized sentences, returns a list of pos_tags
def get_pos_tags(tokenized_sents):
    return [pos_tag(sent) for sent in tokenized_sents]



# given a Sentences object and an index k, creates a separate object for the kth sentence
class Sentence:
    def __init__(self, sents, k):
        self.sentence = sents.sentences[k]
        self.tokenized_sent = sents.tokenized_sents[k]
        self.parse = sents.parses[k]
        self.ner_tag = sents.ner_tags[k]
        self.pos_tag = sents.pos_tags[k]


'''
# example usage
sents = Sentences("What is your name? My name is Bob. Nice to meet you!")
# for each of the 3 sentences, print relevant information
for k in xrange(sents.size):
    sent = Sentence(sents, k)
    print '==== Sentence Object', k, '===='
    print sent.sentence
    print sent.tokenized_sent
    print sent.parse
    print sent.ner_tag
    print sent.pos_tag
    print ''
'''
