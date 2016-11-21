import sys
import en
import re

from Sentence import Sentence

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