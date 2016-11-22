from Question import Question
from Sentence import Sentence
from Information_Retrieval import Information_Retrieval
import nltk


from nltk.corpus import wordnet as wn
from nltk.parse import stanford

import string

def queston_answering(article, questions):
    inst = Information_Retrieval(article)
    with open(questions) as f:
        for line in f.readlines():
            question_text = line.split('\t')[0] #change to line split on server
            question = Question(question_text, 0)
            best_sentence=inst.ranked_list(question)[0]
            print question_text
            #if question.type == 'YES':
                #print answer_binary(question.raw_text,best_sentence)
            if question.type == 'who':
                print ans_who(question_text,best_sentence)
            #if question.type == 'where':
                #print simple_where(question, best_sentence)



def answer_binary(question, best_sentence):
    #title = title.lower().split(" ")
    q_vect = sent_to_vect(question.lower())
    bs_vect = sent_to_vect(best_sentence.lower())
    count = 0.0
    for token, cnt in q_vect.items():
        if token not in bs_vect and (token not in mds):
            count += 1.0
    if count/len(q_vect) > 0.5:
        return "No"
    negs = ["not", "no", "never"]
    for neg in negs:
        if neg in bs_vect:
            return "No"
    return "Yes"

def simple_where(question, best_sentence):
    s_info = Sentence(best_sentence,0)
    for (word, tag) in s_info.ner_tags:
        if tag == 'LOCATION':
            return word
    return None

def simple_where(question, best_sentence):
    s_info = Sentence(best_sentence,0)
    for (word, tag) in s_info.ner_tags:
        if tag == 'LOCATION':
            return word
    return None










mds = ["did", "do", "does", "di", "do", "doe"]
reps = ["it", "they", "he", "she"]
ques = "Who thought that Newtonian mechanics was no longer enough to reconcile the laws of classical mechanics"
BS = "Near the beginning of his career, Einstein thought that Newtonian mechanics was no longer enough to reconcile the laws of classical mechanics with the laws of the electromagnetic field."
#print('no')
parser = Sentence(ques, 0)
stanford = parser.get_parser()
#print(type(stanford))

#print(stanford.raw_parse_sents("Hi"))
#make a new NER tagger with stanford's stuff, call it tagger
#make new stanford parser, call it parser
def tree_to_sent(tree):
    if tree == None:
        return ""
    return ' '.join(tree.leaves())

def sent_to_vect(sent):
    vect = {}
    sent = sent.translate(None, string.punctuation)
    tokens = nltk.tokenize.word_tokenize(sent)
    tokens = filter(None, tokens)
    for token in tokens:
        token = wn.morphy(token)
        if token == None:
            continue
        else:
            token = token.encode('ascii', 'ignore')
        if token in vect.keys():
            vect[token] += 1
        else:
            vect[token] = 1
    return vect

def get_phrases(tree, pattern, reversed, sort):
    phrases = []
    for t in tree.subtrees():
        if t.label() == pattern:
            phrases.append(t)
    if sort == True:
        phrases = sorted(phrases, key=lambda x:len(x.leaves()), reverse=reversed)
        print phrases
    return phrases

def get_main_verb(vp):
    leaves = vp.leaves()
    return leaves[0]

def sents_to_trees(sentences):
    return stanford.raw_parse_sents(sentences)

def sent_to_tree(sentence):
    t = stanford.raw_parse(sentence)
    return t.next()

def answer_definitions(main_vp, s, verb):
    nps = get_phrases(main_vp, "NP", True, True)
    if len(nps)>0:
        candidates = s.split(" " + verb)
        if tree_to_sent(nps[0]) in candidates[0]:
            ans_tree = sent_to_tree(candidates[1])
        else:
            ans_tree = sent_to_tree(candidates[0])
        s_nps = get_phrases(ans_tree, "NP", True, True)
        if len(s_nps) > 0:
            return tree_to_sent(s_nps[0])
        else:
            return ""

#separating helpers from actual code
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





def ans_who(question, best_sentence):
    answer = ""
    qbody = question.replace("Who", "Jacob").replace("?", "")
    best_sentence = best_sentence.lower()
    parsed_question = sent_to_tree(qbody)
    vps = get_phrases(parsed_question, "VP",True, True)
    main_vp = vps[0]
    main_vb = get_main_verb(main_vp)
    ans = answer_definitions(main_vp, best_sentence, main_vb)
    return ans








queston_answering('a10.txt','q.txt')

