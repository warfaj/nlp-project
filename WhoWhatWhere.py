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
def whoQuestion(info):
    words=info.tokenized_sent[:len(info.tokenized_sent)-1]
    whoIndices=[]
    questions=[]
    for pos in ['NNP','PRP']:
        for tag in range(len(info.pos_tag)):
            if info.pos_tag[tag][1]==pos and info.ner_tag[tag][1]=='PERSON':
                whoIndices+=[tag]
    for whoIndex in whoIndices:
        question=''
        score=10
        for word in range(len(words)):
            if word==whoIndex:
                if word==0:
                    score-=4
                    question+='Who '
                    if len(words)>1 and (info.pos_tag[1][1]=='VBZ' or info.pos_tag[1][1]=='VBD'):
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
    words=info.tokenized_sent[:len(info.tokenized_sent)-1]
    whatIndices=[]
    for pos in ['NN','NNS']:
        for tag in range(len(info.pos_tag)):
            if info.pos_tag[tag][1]==pos:
                whatIndices+=[tag]
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
    words=info.tokenized_sent[:len(info.tokenized_sent)-1]
    whereIndices=[]
    for tag in range(len(posTags)):
        if info.pos_tag[tag][1]=='LOCATION':
            whereIndices+=[tag]
    questions=[]
    for whereIndex in whereIndices:
        question=''
        score=10
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

