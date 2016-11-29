def whatQuestion(info):
    words=info.tokenized_sent[:len(info.tokenized_sent)-1]
    questions=[]
    people=[]
    actions=[]
    for word in range(1,len(words)):
        if info.pos_tag[word-1][1]=='NNP':
            if info.pos_tag[word][1]=='VBD':
                people+=[info.pos_tag[word-1][0]]
                actions+=[info.pos_tag[word][0]]
    for question in range(len(people)):
        questions+=[('What did '+people[question]+' '+en.verb.present(actions[question])+'?',5)]
    return questions 
