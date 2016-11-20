import os
import en
import re

from nltk.parse import stanford
from nltk import word_tokenize, pos_tag
from nltk.tag.stanford import StanfordNERTagger
from nltk.tree import Tree

#dir = '/Users/warfajibril/PycharmProjects/NLPProject/'
#dir = '~/Desktop/nlp project/nlp-project-master/'
dir = ''

class Sentence(object):

    def __init__(self, raw_sentence, id):
        self.id = id
        self.raw_text=raw_sentence
        self.tokenized_text=word_tokenize(raw_sentence)
        self.parser = self.get_parser()
        self.parse_tree= self.parser.raw_parse(raw_sentence)
        self.pos_tags = pos_tag(self.tokenized_text)
        self.ner_tags = self.get_ner_tags()



    def get_parser(self):
        os.environ['CLASSPATH'] = dir+'stanford-parser'
        os.environ['STANFORD_PARSER'] = dir+'stanford-parser/stanford-parser.jar'
        os.environ['STANFORD_MODELS'] = dir+'stanford-parser/stanford-parser-3.6.0-models.jar'
        parser = stanford.StanfordParser(model_path=dir+"stanford-parser/models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
        return parser

    def get_ner_tags(self):
        os.environ['CLASSPATH'] = dir+'stanford-ner'
        return StanfordNERTagger(dir+'stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz').tag(self.tokenized_text)

def modify(inputStr):

    sent = Sentence(inputStr,0)
    pos_tags = sent.pos_tags
    tagged = None
    for x in sent.parse_tree:
        for t in x.subtrees():
            if t.label() == 'NP':
                tagged = Tree.toString(t)
    needChange = False
    starts = {'is', 'was', 'are', 'were', 'has', 'have', 'had', 'will', 'would', 'can', 'could', 'shall', 'should'}
    aux_verbs = [i for i, w in enumerate(tagged) if w[0] in starts]
    if aux_verbs:
        tagged.insert(0, tagged.pop(aux_verbs[0]))
    else:
        tagged.insert(0, ('did', 'VBD'))
        needChange = True
    #tagged.insert(0, ('When', 'WRB'))

    if tagged[1][1] != 'NNP':
        return None

    ans = tagged[0][0].title() + ' '
    if needChange:
        for i in xrange(len(tagged)-2):
            ans += present(tagged[i+1][0]) + ' '
    else:
        for i in xrange(len(tagged)-2):
            ans += tagged[i+1][0] + ' '
    ans += '?'

    return ans

def present(word):
    try:
        return en.verb.present(word)
    except:
        return word


with open('q.txt') as f:
    for line in f.readlines():
        sentences = re.split('(?<=[.!?]) +', line)
        for s in sentences:
            if s == '' or s.isspace():
                continue 
            s = ''.join(c for c in s if ord(c)<128)
            print modify(s)
            print s
