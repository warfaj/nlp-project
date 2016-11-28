from Question import Question
from Sentence import Sentence
from Information_Retrieval import Information_Retrieval
import nltk
import sys


from nltk.corpus import wordnet as wn
from nltk.parse import stanford

import string


mds = ["did", "do", "does", "di", "do", "doe"]
reps = ["it", "they", "he", "she"]
def main():
    #article = sys.argv[1]
    #questions = sys.argv[2]
    article = 'a1.txt'
    questions = 'q_avo.txt'
    question_answering(article,questions)



def question_answering(article, questions):
    inst = Information_Retrieval(article,True)
    with open(questions) as f:
        for line in f.readlines():
            #try:
                question_text = line.split('\t')[0] #change to line split on server
                question = Question(question_text, 0)

                #if question.type == 'YES':
                 #   print answer_binary(question, inst)
                #if question.type == 'WHO':
                #    print question_text
                #    print answer_who(question, inst)
                #if question.type == 'WHAT':
                #   print question_text
                #   print answer_what(question, inst)
                if question.type == 'WHY':
                   print question_text
                   print answer_why(question, inst)
                #if question.type == 'WHEN':
                #    print question_text
                #    print answer_when(question,inst)
                #if question.type == "WHERE":
                #    print question_text
                #    print answer_where(question,inst)
            #except:
                #print "crash"


def find_tag_answer(pattern, sent, answer_tags, is_when=False):
    tokens = pattern.tokenized_text
    sent_tokens = sent.tokenized_text
    last = 0
    for word in tokens:
        if word in sent_tokens:
            last = max(sent_tokens.index(word),last)
    tags = None
    if is_when:
        tags = sent.get_when_tags()
    else:
        tags = sent.get_ner_tags()
    default = None
    for ind in xrange(len(tags)):
        (word,tag) = tags[ind]
        if tag in answer_tags and word not in pattern.tokenized_text:
            if ind < len(tags) -1:
                (next_word, next_tag) = tags[ind+1]
                if next_tag in answer_tags:
                    default = word +' '+next_word
                else:
                    default = word
            else:
                default = word
            if ind > last:
                break
    return default

def answer_who(question, inst):
    pattern = Sentence(question.wh_pattern(),0)
    best_sen = inst.ranked_list(pattern)[0]
    info = Sentence(best_sen,0)
    answer = find_tag_answer(pattern,info, ['PERSON'])
    if answer:
        return answer
    return inst.default_person

def answer_what(question,inst):
    pattern = Sentence(question.wh_pattern(),0)
    best_sen = inst.ranked_list(pattern)[0]
    info = Sentence(best_sen,0)
    print question.wh_pattern()
    return best_sen

def answer_when(question, inst):
    pattern = Sentence(question.wh_pattern(),0)
    best_sen = inst.ranked_list(pattern)[0]
    info = Sentence(best_sen,0)
    answer = find_tag_answer(pattern,info, ['DATE','TIME'], True)
    if answer:
        return answer
    return "I'm not sure...."

def answer_where(question, inst):
    best_sen = inst.ranked_list(question)[0]
    info = Sentence(best_sen,0)
    answer = find_tag_answer(question,info, ['LOCATION'])
    if answer:
        return answer
    return inst.default_location


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


def answer_binary(question_info, inst):
    best_sentence=inst.ranked_list(question_info)[0]
    question = question_info.raw_text
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

def answer_why(question_info, inst):
    best_sentence=inst.ranked_list(question_info)[0]
    s_tokens = nltk.word_tokenize((best_sentence.lower()))
    question = question_info.raw_text
    ans = ""
    if "because" in s_tokens:
        ans = " ".join(s_tokens[s_tokens.index("because"):][1:])
    elif "since" in s_tokens:
        ans = " ".join(s_tokens[s_tokens.index("since"):][1:])
    elif "therefore" in s_tokens:
        ans = " ".join(s_tokens[:s_tokens.index("therefore")][1:])
    elif "so" in s_tokens:
        ans = " ".join(s_tokens[:s_tokens.index("so")][1:])
    elif "as" in s_tokens:
        ans = " ".join(s_tokens[s_tokens.index("as"):][1:])
    elif "due to" in s_tokens:
        reason_token = s_tokens[s_tokens.index("due"):]
        reason_token = reason_token[1:]
        if "," in reason_token:
            reason_token = reason_token[:s_tokens.index(",")]
        ans = " ".join(reason_token)
    elif "in order to" in s_tokens:
        reason_token = s_tokens[s_tokens.index("order"):]
        reason_token = reason_token[1:]
        if "," in reason_token:
            reason_token = reason_token[:s_tokens.index(",")]
        ans = " ".join(reason_token)
    return ans

def answer_how_many(question_info, inst):
    best_sentence=inst.ranked_list(question_info)[0]
    question = question_info.raw_text
    q_tokens = nltk.tokenize.word_tokenize(question)
    s_tokens = nltk.tokenize.word_tokenize(best_sentence)
    target = q_tokens[2]

    t_index = s_tokens.index(target)
    n_index = t_index-1
    while n_index >= 0 and (not str.isdigit( s_tokens[n_index])):
        n_index -= 1

    return s_tokens[n_index] if n_index>=0 else ""

main()
