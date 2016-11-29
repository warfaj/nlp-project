def whereQuestion(info):
    words=info.tokenized_sent[:len(info.tokenized_sent)-1]
    values=[]
    (subject,verb,place,done)=(True,False,False,False)
    questions=[]
    for word in range(len(words)):
        if subject and info.pos_tag[word][1] in ['NN','NNP']:
            values+=[words[word]]
            (subject,verb,place,done)=(False,True,False,False)
        elif verb and info.pos_tag[word][1] in ['VBD','VBZ']:
            values+=[words[word]]
            (subject,verb,place,done)=(False,False,True,False)
        elif place and info.ner_tag[word][1]=='LOCATION':
            if words[word-1]in['in','at']:
                values+=[words[word]]
            elif info.pos_tag[word-1]=='DT':
                if words[word-2]in ['in','at']:
                    values+=[words[word]]
    if len(values)==3:
        try:questions+=[('Where did '+values[0]+' '+en.verb.present(values[1])+'?',10)]
        except:questions+=[('Where did '+values[0]+' '+(values[1])+'?',10)]
    return questions
