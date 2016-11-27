from nltk import tokenize
from parse import Parse
from Question import Question
from Sentence import Sentence
import en
from collections import defaultdict

class Information_Retrieval:
    def __init__(self, article, saveTags=False):
        self.article_name = article
        self.raw_text = open(article, 'r').read()
        self.article = Parse(self.raw_text)
        self.default_person = None
        self.default_location = None
        self.tags = None
        if saveTags:
            self.tags = (Sentence(self.raw_text,0).get_ner_tags())
            self.default_person = self.get_default_pronoun(self.tags, ['PERSON'])
            self.default_location = self.get_default_pronoun(self.tags, ['LOCATION'])


    def get_default_pronoun(self, tags, answer_tag):
        counts = defaultdict(int)
        for (word,tag) in tags:
            if tag in answer_tag:
                counts[word] +=1
        max = ''
        max_count = 0
        for key in counts:
            count = counts[key]
            if count > max_count:
                max = key
                max_count = count
        return max

    def ranked_list(self, question):
        relevant_sentences = dict()
        i = 1
        for (word,tag) in question.get_pos_tags():
            if 'DT' not in tag and '.' not in tag:
                sents = self.article.findword(word)
                #print word
                for sent in sents:
                    if sent not in relevant_sentences:
                        relevant_sentences[sent] = i
                    else:
                        relevant_sentences[sent] += i
            i+=1
        #print relevant_sentences
        best_indices = sorted(relevant_sentences.keys(),key= lambda x : relevant_sentences[x], reverse=True)
        max = 0
        top = []
        for ind in best_indices:
            count = relevant_sentences[ind]
            if count > max:
                top = [ind]
                max = count
            elif count == max:
                top.append(ind)

        best_sentences = [Sentence(self.article.sentences[x],0).raw_text for x in top]
        return sorted(best_sentences,key= lambda x: len(x))

'''
inst = Information_Retrieval('a10.txt')

with open('q.txt') as f:
    i = 0
    for line in f.readlines():
        question = line.split('\t')[0]
        info = Question(question, i)
        if info.type != 'WHERE' and info.type != 'YES':
            i+=1
            pattern = Sentence(info.wh_pattern(),0)
            print question
            print inst.ranked_list(pattern)[0]
            print ' '
'''