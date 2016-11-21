import os
#import en
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
        #self.parser = self.get_parser()
        #self.parse_tree= self.parser.raw_parse(raw_sentence)
        self.pos_tags = pos_tag(self.tokenized_text)
        #self.ner_tags = self.get_ner_tags()
    def get_parser(self):
        os.environ['CLASSPATH'] = dir+'stanford-parser'
        os.environ['STANFORD_PARSER'] = dir+'stanford-parser/stanford-parser.jar'
        os.environ['STANFORD_MODELS'] = dir+'stanford-parser/stanford-parser-3.6.0-models.jar'
        parser = stanford.StanfordParser(model_path=dir+"stanford-parser/models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
        return parser
    def get_ner_tags(self):
        os.environ['CLASSPATH'] = dir+'stanford-ner'
        return StanfordNERTagger(dir+'stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz').tag(self.tokenized_text)


def whoQuestion(info):
    s=Sentence(info,0)
    tags=s.pos_tags
    result=[]
    words=word_tokenize(info)
    for pair in range(len(tags)):
        if tags[pair][1]=='NNP':
            question=''
            person=pair
            for p in range(len(words)-1):
                if p!=pair:
                    question+=words[p]+' '
                else:
                    if pair==0:
                        question+='Who '
                    else:
                        question+='who '
            question+='?'
            result+=[question]
    return result
with open('a10.txt') as f:
    for line in f.readlines()[:10]:
        sentences = re.split('(?<=[.!?]) +', line)
        for s in sentences:
            if s == '' or s.isspace():
                continue 
            s = ''.join(c for c in s if ord(c)<128)
            sent=Sentence(s,0)
            print(s)
            print(whoQuestion(s))


