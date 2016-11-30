from Sentence import Sentence
import en
class Question(Sentence):


    def __init__(self, raw_sentence, id):
        Sentence.__init__(self,raw_sentence, id)
        self.type = self.get_type()


    def get_type(self):
        q_word = self.tokenized_text[0].lower()
        if q_word in {'is', 'was', 'are', 'were', 'has', 'have', 'had', 'will', 'would', 'can', 'could', 'shall', 'should','did'}:
            return "YES"
        return q_word.upper()


    def wh_pattern(self):
        tree = self.get_parse().next()
        phrase = None
        pattern  = self.raw_text
        for t in tree.subtrees():
            if t.label() == 'SQ':
                phrase = t
                A = []
                B = []
                C = []
                for sub in phrase:
                    if sub.label().startswith('N'):
                        A = sub.leaves()
                    elif sub.label().startswith('V'):
                        B = sub.leaves()
                    elif sub.label().startswith('S'):
                        C = sub.leaves()
                pattern = ''
                for word in A:
                    pattern += word+' '
                for i in xrange(len(B)):
                    word = B[i]
                    if i == 0 and en.is_verb(word):
                        word = en.verb.past(word)
                    pattern += word +' '
                for word in C:
                    pattern += word+' '
                pattern = pattern.strip()
                break
        return pattern

    def where_pattern(self):
        tree = self.get_parse().next()
        phrase = None
        for t in tree.subtrees():
            if t.label() == 'SQ':
                phrase = t
                A = []
                B = []
                C = []
                for sub in phrase:
                    if sub.label() == 'NP':
                        A = sub.leaves()
                    elif 'VB' in sub.label():
                        B = sub.leaves()
                    else:
                        C = sub.leaves()
                pattern  = ''
                for word in A:
                    pattern += word+' '
                for i in xrange(len(B)):
                    word = B[i]
                    if i == 0:
                        word = en.verb.conjugate(word,'3rd singular past',negate=False)
                    pattern += word +' '
                for word in C:
                    pattern += word+' '
                pattern = pattern.strip()
                break
        return pattern

'''
with open('q.txt') as f:
    i = 0
    for line in f.readlines():
        question = line.split('\t')[0]
        info = Question(question, i)
        i+= 1
        print info.get_answer_pattern()

'''