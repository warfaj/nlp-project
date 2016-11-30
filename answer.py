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
    article = 'a10.txt'
    questions = 'q.txt'
    print(article)

    article = sys.argv[1]
    questions = sys.argv[2]
    #article = 'a5.txt'
    #questions = 'q_lob.txt'
    question_answering(article,questions)

def question_answering(article, questions):
    inst = Information_Retrieval(article,True)
    with open(questions) as f:
        for line in f.readlines():
            try:
                question_text = line.split('\t')[0].replace("\xc2\xa0", " ") #change to line split on server
                question = Question(question_text, 0)


                #if question.type == 'YES':
                 #   print answer_binary(question, inst)
                #if question.type == 'WHO':
                #    print question_text
                #    print answer_who(question, inst)
                if question.type == 'HOW':
                   print question_text
                   print answer_how_many(question, inst)
                #if question.type == 'WHEN':
                #    print question_text
                #    print answer_when(question,inst)
                if question.type == "WHY":
                    print question_text
                    print answer_why(question,inst)
            #except:
                #print "crash"

                if question.type == 'YES':
                    print answer_binary_old(question, inst)
                elif question.type == 'WHO':
                    print answer_who(question, inst)
                elif question.type == 'WHAT':
                   print answer_what(question, inst)
                elif question.type == 'WHY':
                   print answer_why(question, inst)
                elif question.type == 'WHEN':
                    print answer_when(question,inst)
                elif question.type == "WHERE":
                    print answer_where(question,inst)
                else:
                    print inst.ranked_list(question)[0]
            except:
                print "I'm not sure.."



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
    return best_sen

def answer_when(question, inst):
    pattern = Sentence(question.wh_pattern(),0)
    best_sen = inst.ranked_list(pattern)[0]
    info = Sentence(best_sen,0)
    answer = find_tag_answer(pattern,info, ['DATE','TIME'], True)
    if answer:
        return answer
    return best_sen

def answer_where(question, inst):
    best_sen = inst.ranked_list(question)[0]
    info = Sentence(best_sen,0)
    answer = find_tag_answer(question,info, ['LOCATION', 'ORGANIZATION'])
    return best_sen


def s2v(sent):
    se, vc = sent.translate(None, string.punctuation), {}
    tokens = nltk.tokenize.word_tokenize(s)
    tokens = filter(None, tokens)
    for token in tokens:
        token = wn.morphy(token)
        if token == None:
            continue
        else:
            token = token.encode('ascii', 'ignore')
        if token in vc.keys():
            vc[token] += 1
        else:
            vc[token] = 1
    return vc


def answer_binary_old(question_info, inst):
    best_sentence=inst.ranked_list(question_info)[0]
    question = question_info.raw_text
    #title = title.lower().split(" ")
    q_vect = s2v(question.lower())
    bs_vect = s2v(best_sentence.lower())
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

def answer_binary(question, inst):
    best_sentence=inst.ranked_list(question)[0]
    best_sen_info = Sentence(best_sentence, 0)
    pattern = Sentence(question.wh_pattern(),0)
    for (word,tag) in pattern.get_pos_tags():
        if tag.startswith('N') or tag.startswith('V'):
            seen = len(inst.article.findword(word))
            if seen == 0:
                print word,tag
                return 'No'
    negs = ["not", "no", "never", "didn't", "wasn't"]
    for neg in negs:
        if neg in best_sentence:
            return "No"


    return 'Yes'



def answer_why(question_info, inst):
    best_sentence=inst.ranked_list(question_info)[0]
    sentok = nltk.word_tokenize((best_sentence.lower()))
    question = question_info.raw_text
    print(best_sentence)
    ans = ""
    words = ["because","so","as","since","therefore"]
    for word in words:
        if word in sentok:
            ans = " ".join(sentok[sentok.index(word):][1:])
            break
    if "due to" in sentok: 
        rdtok = sentok[sentok.index("due"):][1:]
        if "," in rdtok:
            rdtok = rdtok[:sentok.index(",")]
        ans = " ".join(rdtok)
    elif "in order to" in sentok:
        rdtok = sentok[sentok.index("order"):][1:]
        if "," in rdtok:
            rdtok = rdtok[:sentok.index(",")]
        ans = " ".join(rdtok)

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
    return best_sentence


main()
