import sys
import en
import re
import copy

from Sentences import Sentences, Sentence
'''
from nltk import word_tokenize
from who import whoQuestion
from what import whatQuestion
'''

def yesNoHelper(pos_tag):
    tagged = copy.deepcopy(pos_tag)
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
        return (ans, 4)
    elif not proper:
        return (ans, 3)
    elif ',' in ans or 'and' in ans:
        return (ans, 2)
    else:
        return (ans, 1)

def yesNoQuestion(sent):
    return yesNoHelper(sent.pos_tag)

def whenQuestion(sent):
    when = sent.when_tag
    if len(when) <= 2 or when[1][1] not in {'DATE', 'TIME'}:
        return ('', 10)
    idx = 1
    while (when[idx][1] in {'DATE', 'TIME'} or when[idx][0] == ','):
        idx += 1
    ans = 'When did '
    for i in range(idx, len(when)-1):
        ans += when[i][0] + ' '
    ans += '?'
    if sent.pos_tag[idx][1] in {'NNP', 'DT'}:
        return (ans, 1)
    else:
        return (ans, 3)


def whyQuestion(sent):
    tokens = copy.deepcopy(sent.tokenized_sent)
    cuz_idx = [i for i, w in enumerate(tokens) if w == 'because']
    if not cuz_idx:
        return ('', 10)
    yesNoPair = yesNoHelper(sent.pos_tag[:cuz_idx[0]])
    yesNoQues = yesNoPair[0] + ' ?'
    ans = 'Why ' + yesNoQues[0].lower() + yesNoQues[1:]
    return (ans, 1)






def main():
    article = sys.argv[1]
    nquestions = sys.argv[2]
    q = [('What is the article about?',1)]
    with open(article) as f:
        raw_sentences = f.read()
        sents = Sentences(raw_sentences)
        for k in xrange(sents.size):
            sent = Sentence(sents, k)
            #q += whoQuestion(sent)
            q += whatQuestion(sent)
            #q += whereQuestion(sent)
        q = sorted(q, key=lambda x: x[1])
    for i in xrange(int(nquestions)):
        print q[i%len(q)]
#        print q[i][0]

main()