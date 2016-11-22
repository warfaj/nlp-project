from nltk import tokenize
from parse import Parse
from Question import Question
from Sentence import Sentence


class Information_Retrieval:
    def __init__(self, article):
        self.article_name = article
        self.article = Parse(open(article, 'r').read())

    def ranked_list(self, question):
        relevant_sentences = dict()
        for (word,tag) in question.pos_tags:
            if 'DT' not in tag and '.' not in tag:
                sents = self.article.findword(word)
                #print word
                for sent in sents:
                    if sent not in relevant_sentences:
                        relevant_sentences[sent] = len(word)
                    else:
                        relevant_sentences[sent] += len(word)
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
        return best_sentences

'''
inst = Information_Retrieval('a10.txt')

with open('q.txt') as f:
    i = 0
    for line in f.readlines():
        question = line.split('\t')[0]
        info = Question(question, i)
        i+=1
        print inst.ranked_list(info)
'''