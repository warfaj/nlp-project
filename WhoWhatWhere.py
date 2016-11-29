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
from Sentences import Sentences, Sentence
def simplify(info,pos):
    s=Sentence(info,0)
    posTags=[item[1] for item in s.pos_tag()]
    nerTags=[item[1] for item in s.ner_tag()]
    words=s.tokenized_sent[:len(nerTags)-1]
    if pos not in posTags:
        return (None,None,None)
    i=posTags.index(pos)
    extraWords=[]
    modifiedPosTags=tags[:i+1]
    modifiedNerTags=tags[:i+1]
    for word in range(i+1,len(words)):
        if posTags[word-1]==pos and posTags[word]==pos:
            extraWords+=[words[word]]
        else:
            modifiedPostags+=[posTags[word]]
            modifiedNerTags+=[nerTags[word]]
    for word in extraWords:
        words.remove(word)
    return (words,modifiedPostags,modifiedNerTags)
def whoQuestion(info):
    info=info.sentence
    words,posTags,nerTags=simplify(info,'NNP')
    if (words,posTags,nerTags)==(None,None,None):return ('',100)
    whoIndices=[]
    questions=[]
    for pos in ['NNP','PRP']:
        for tag in range(len(posTags)):
            if posTags[tag]==pos and nerTags[tag]=='PERSON':
                whoIndices+=[tag]
    for whoIndex in whoIndices:
        question=''
        score=10
        for word in range(len(words)):
            if word==whoIndex:
                if word==0:
                    score-=4
                    question+='Who '
                    if len(posTags)>1 and (posTags[1]=='VBZ' or posTags[1]=='VBD'):
                        score-=5
                else:
                    if word==len(words)-1:
                        question+='who?'
                    else:
                        question+='who '
            else:
                if word==len(words)-1:
                        question+=words[word]+'?'
                else:
                    question+=words[word]+' '
        questions+=[(question,score)]
    return questions
def whatQuestion(info):
    s=info
    posTags=[item[1] for item in s.pos_tag()]
    nerTags=[item[1] for item in s.ner_tag()]
    words=s.tokenized_sent[:len(nerTags)-1]
    whatIndices=[]
    for pos in ['NN','NNS']:
        if pos in posTags:
            whatIndices+=[posTags.index(pos)]
    questions=[]
    for whatIndex in whatIndices:
        question=''
        score=10
        if whatIndex!=-1:
            for word in range(len(words)):
                if word==whatIndex:
                    if word==0:
                        question+='What '
                    elif word==len(words)-1:
                        question+='what?'
                    else:
                        question+='what '
                else:
                    if word==len(words)-1:
                        question+=words[word]+'?'
                    else:
                        question+=words[word]+' '
        questions+=[(question,score)]
    return questions
def whereQuestion(info):
    s=info
    posTags=[item[1] for item in s.pos_tag()]
    nerTags=[item[1] for item in s.ner_tag()]
    words=s.tokenized_sent[:len(nerTags)-1]
    whereIndices=[]
    for tag in range(len(posTags)):
        if posTags[tag]=='LOCATION':
            whereIndices+=[tag]
    questions=[]
    for whereIndex in whereIndices:
        question=''
        score=10
        if whereIndex!=-1:
            for word in range(len(words)):
                if word==whereIndex:
                    if word==0:
                        question+='Where '
                    elif word==len(words)-1:
                        question+='where?'
                    else:
                        question+='where '
                else:
                    if word==len(words)-1:
                        question+=words[word]+'?'
                    else:
                        question+=words[word]+' '
        questions+=[(question,score)]
    return questions
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
s='Thomas Alva Edison met John F Kennedy. Max was born in Mexico. Bob ate an apple.'
S=Sentences(s)
sent1=Sentence(S,0)
sent2=Sentence(S,1)
sent3=Sentence(S,2)
print(whoQuestion(sent1),whereQuestion(sent2),whatQuestion(sent3))

