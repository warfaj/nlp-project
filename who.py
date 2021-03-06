import os
#import en
import re

from nltk.parse import stanford
from nltk import word_tokenize, pos_tag
from nltk.tag.stanford import StanfordNERTagger
from nltk.tree import Tree

#dir = '/Users/warfajibril/PycharmProjects/NLPProject/'
#dir = '~/Desktop/nlp project/nlp-project-master/'
dir = '/Users/Tejas/Desktop/nlp-project-master/'
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
        #import nltk
        #nltk.internals.config_java("C:/Program Files/Java/jre1.8.0_111/bin/java.exe")
        os.environ['CLASSPATH'] = dir+'stanford-ner'
        return StanfordNERTagger(dir+'stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz').tag(self.tokenized_text)


def whoQuestion(info):
    try:
        s=Sentence(info,0)
        tags=[item[1] for item in s.pos_tags]
       # print(tags)
        words=word_tokenize(info)[:len(tags)-1]
        whoIndex=-1
        try:
            whoIndex=tags.index('NNP')
        except:
            try:
                whoIndex=tags.index('PRP')
            except:
                return ('',100)
        for word in range(whoIndex+1,len(words)):
            if tags[word-1]=='NNP' and tags[word]=='NNP':
                words.remove(words[word])
                tags.remove(tags[word])
            else:
                break
        question=''
        score=10
        if whoIndex!=-1:
            for word in range(len(words)):
                if word==whoIndex:
                    if word==0:
                        score-=4
                        question+='Who '
                        if len(tags)>1 and (tags[1]=='VBZ' or tags[1]=='VBD'):
                            score-=5
                    else:
                        question+='who '
                else:
                    question+=words[word]+' '
        return (question+'?',score)
    except:
        return ('',100)
'''
with open('a10.txt') as f:
    for line in f.readlines()[:10]:
        sentences = re.split('(?<=[.!?]) +', line)
        for s in sentences:
            if s == '' or s.isspace():
                continue 
            s = ''.join(c for c in s if ord(c)<128)
            sent=Sentence(s,0)
            #print(s)
            print(whoQuestion(s))
'''
s='She is my friend.'
S=Sentence(s,0)
#print(S.pos_tags)
print(whoQuestion(s))




