import sys
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

def generateYesNo(inputStr):
    sent = Sentence(inputStr,0)
    tagged = sent.pos_tags
    needChange = False
    starts = {'is', 'was', 'are', 'were', 'has', 'have', 'had', 'will', 'would', 'can', 'could', 'shall', 'should'}
    aux_verbs = [i for i, w in enumerate(tagged) if w[0] in starts]
    if aux_verbs:
        tagged.insert(0, tagged.pop(aux_verbs[0]))
    else:
        tagged.insert(0, ('did', 'VBD'))
        needChange = True

    proper = False
    if tagged[1][1] in {'NNP', 'DT'} :
        proper = True

    ans = tagged[0][0].title() + ' '
    punc = False
    
    for i in xrange(len(tagged)-1):
        word = tagged[i+1][0]
        if i+1 == 1 and tagged[1][1] != 'NNP':
            word = word.lower()
        if i+1 == len(tagged)-1:
            if tagged[i+1][0] in {'.', '!'}:
                word = '?'
                punc = True

        # we may need to change word to present tense
        word2 = None
        if needChange:
            try:
                word2 = en.verb.present(word)
            except:
                word2 = word
        else:
                word2 = word

        if i+1 == len(tagged)-1:
            ans += word2
        else:
            ans += word2 + ' '

    if not punc:
        return (4, ans)
    elif not proper:
        return (3, ans)
    elif ',' in ans or 'and' in ans:
        return (2, ans)
    else:
        return (1, ans)


def main():
    article = sys.argv[1]
    nquestions = sys.argv[2]
    qs = []
    with open(article) as f:
        for line in f.readlines():
            sentences = re.split('(?<=[.!?]) +', line)
            for s in sentences:
                if s == '' or s.isspace():
                    continue
                s = ''.join(c for c in s if ord(c)<128)
                qs.append(generateYesNo(s))
    sorted_qs = sorted(qs, key=lambda x: x[0])
    for i in xrange(int(nquestions)):
        print sorted_qs[i % len(sorted_qs)][1]

main()