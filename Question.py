from Sentence import Sentence

class Question(Sentence):


    def __init__(self, raw_sentence, id):
        Sentence.__init__(self,raw_sentence, id)
        self.type = self.get_type()


    def get_type(self):
        q_word = self.tokenized_text[0].lower()
        if q_word in {'is', 'was', 'are', 'were', 'has', 'have', 'had', 'will', 'would', 'can', 'could', 'shall', 'should','did'}:
            return "YES"
        return q_word






'''

with open('q.txt') as f:
    i = 0
    for line in f.readlines():
        question = line.split('\t')[0]
        info = Question(question, i)
        i+= 1
        print info.type
'''