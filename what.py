def whatQuestion(info):
    words=info.tokenized_sent[:len(info.tokenized_sent)-1]
   # print(info.pos_tag)
    whatIndices=[]
    for pos in ['NN','NNS']:
        for tag in range(len(info.pos_tag)):
            if info.pos_tag[tag][1]==pos:
                whatIndices+=[tag]
    questions=[]
    for whatIndex in whatIndices:
        question=''
        score=10
        if whatIndex!=-1:
            for word in range(len(words)):
                if info.pos_tag[word]!='JJ':
                    if word==whatIndex:
                        if word==0:
                            question+='What '
                        elif word==len(words)-1:
                            question+='what?'
                        else:
                            question+='what '
                    else:
                        if word==len(words)-1:
                            question+=words[word]+'?'
                        else:
                            question+=words[word]+' '
        if word>1:
            if info.pos_tag[word-1][1] in ['DT','VBZ','VBD']:score-=3
        ptags=[item[1]for item in info.pos_tag]
        for pos in ['NNP','PRP','JJ']:
            if pos in ptags:score+=5
        for word in ['Thus','thus','This','this','These','these','Those','those','That','that','also','Also']:
            if word in question:score+=5
        questions+=[(question,score)]
    return questions
