import Sentence

class Question(Sentence):


    def __init__(self, raw_sentence, id):
        Sentence.__init__(self, raw_sentence, id)
        self.type = self.get_type()


    def get_type(self):
        return None
