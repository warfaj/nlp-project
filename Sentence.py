import os
from nltk.parse import stanford
from nltk import word_tokenize, pos_tag
from nltk.tag.stanford import StanfordNERTagger

class Sentence(object):

    def __init__(self, raw_sentence, id):
        self.id = id
        self.raw_text=raw_sentence
        self.tokenized_text=word_tokenize(raw_sentence)
        self.parser = self.get_parser()
        self.tagger = self.get_tagger()
        self.parse_tree= self.parser.raw_parse(raw_sentence)
        self.pos_tags = pos_tag(self.tokenized_text)
        self.ner_tags = self.get_ner_tags()



    def get_parser(self):
        os.environ['STANFORD_PARSER'] = 'stanford_parser/stanford-parser-full-2015-12-09/stanford-parser.jar'
        os.environ['STANFORD_MODELS'] = 'stanford_parser/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'
        parser = stanford.StanfordParser(model_path="stanford_parser/stanford-parser-full-2015-12-09/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
        return parser

    def get_ner_tags(self):
        return StanfordNERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz').tag(self.tokenized_text)