import sys
import en
import re
import copy

from Sentences import Sentences, Sentence

def yesNoHelper(pos_tag, pronoun):
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
        if i+1 == 1:
            if tagged[1][1] == 'PRP':
                word = pronoun
            elif tagged[1][1] != 'NNP':
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
    elif ',' in ans or 'and' in ans:
        return (ans, 3)
    elif not proper:
        return (ans, 2)
    else:
        return (ans, 1)

def yesNoQuestion(sent):
    return [yesNoHelper(sent.pos_tag, sent.pronoun)]

def whenQuestion(sent):
    when = copy.deepcopy(sent.when_tag)
    if len(when) <= 2 or when[1][1] not in {'DATE', 'TIME'}:
        return []
    idx = 1
    while (when[idx][1] in {'DATE', 'TIME'} or when[idx][0] == ','):
        idx += 1
    ans = 'When did '
    score = 4
    if sent.pos_tag[idx][1] in {'NNP', 'DT'}:
        score = 2
    if sent.pos_tag[idx][1] == 'PRP':
        ans += sent.pronoun + ' '
        score = 3
    else:
        ans += when[idx][0] + ' '
    needChange = True
    for i in range(idx+1, len(when)-1):
        if needChange:
            try:
                ans += en.verb.present(when[i][0]) + ' '
                needChange = False
            except:
                ans += when[i][0] + ' '
        else:
            ans += when[i][0] + ' '
    ans += '?'
    return [(ans, score)]

def whyQuestion(sent):
    tokens = copy.deepcopy(sent.tokenized_sent)
    cuz_idx = [i for i, w in enumerate(tokens) if w == 'because']
    if not cuz_idx:
        return []
    yesNoPair = yesNoHelper(sent.pos_tag[:cuz_idx[0]], sent.pronoun)
    yesNoQues = yesNoPair[0] + ' ?'
    ans = 'Why ' + yesNoQues[0].lower() + yesNoQues[1:]
    return [(ans, 1)]






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
        score=6
        for word in range(len(words)):
            if word==whoIndex:
                if word==0:
                    score-=2
                    question+='Who '
                    if len(words)>1 and (info.pos_tag[1][1]=='VBZ' or info.pos_tag[1][1]=='VBD'):
                        score-=3
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
    questions=[]
    people=[]
    actions=[]
    for word in range(1,len(words)):
        if info.pos_tag[word-1][1]=='NNP':
            if info.pos_tag[word][1]=='VBD':
                people+=[info.pos_tag[word-1][0]]
                actions+=[info.pos_tag[word][0]]
    for question in range(len(people)):
        try: questions+=[('What did '+people[question]+' '+en.verb.present(actions[question])+'?',4)]
        except: questions+=[('What did '+people[question]+' '+actions[question]+'?',6)]
    return questions 

def whereQuestion(info):
    words=info.tokenized_sent[:len(info.tokenized_sent)-1]
    whereIndices=[]
    for tag in range(len(words)):
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





def main():
    article = sys.argv[1]
    nquestions = sys.argv[2]
    q = [('What is the article about?',3)]
    with open(article) as f:
        raw_sentences = f.read()
        sents = Sentences(raw_sentences)
        for k in xrange(sents.size):
            sent = Sentence(sents, k)
            try: q += yesNoQuestion(sent)
            except: pass
            try: q += whenQuestion(sent)
            except: pass
            try: q += whyQuestion(sent)
            except: pass
            try: q += whoQuestion(sent)
            except: pass
            try: q += whatQuestion(sent)
            except: pass
            try: q += whereQuestion(sent)
            except: pass
        q = sorted(q, key=lambda x: x[1])
    for i in xrange(int(nquestions)):
        print q[i%len(q)][0]

main()