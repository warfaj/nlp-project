import os
from nltk.parse import stanford
from nltk import word_tokenize, pos_tag
from nltk.tag.stanford import StanfordNERTagger

dir = '/Users/Warfa/Desktop/nlp-project/'


class Sentence:

    def __init__(self, raw_sentence, id):
        self.id = id
        self.raw_text=raw_sentence.strip().decode("ascii","ignore").encode("ascii")
        self.tokenized_text=word_tokenize(self.raw_text)
        self.parser = self.get_parser()


    def get_parse(self):
        return self.parser.raw_parse(self.raw_text)

    def get_parser(self):
        os.environ['CLASSPATH'] = dir+'stanford-parser'
        os.environ['STANFORD_PARSER'] = dir+'stanford-parser/stanford-parser.jar'
        os.environ['STANFORD_MODELS'] = dir+'stanford-parser/stanford-parser-3.6.0-models.jar'
        parser = stanford.StanfordParser(model_path=dir+"stanford-parser/models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
        return parser

    def get_ner_tags(self):
        os.environ['CLASSPATH'] = dir+'stanford-ner'
        return StanfordNERTagger(dir+'stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz').tag(self.tokenized_text)

    def get_pos_tags(self):
        return pos_tag(self.tokenized_text)
'''

with open('q.txt') as f:
    i = 0
    for line in f.readlines():
        question = line.split('\t')[0]
        info = Sentence(question, i)
        i+= 1
        print info.ner_tags
        print info.pos_tags
        for x in info.parse_tree:
            print x
'''


info = Sentence("What is your name?", 0)
