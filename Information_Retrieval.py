from bs4 import BeautifulSoup
from nltk import tokenize


class Sentence:
    def __init__(self, sID, raw_text):
        self.sID = sID
        self.raw_text = raw_text


class Information_Retrieval:
    def __init__(self, article):
        self.article_name = article
        self.article = self.parse_html()

    def parse_html(self):
        sentence_arr = []

        with open(self.article_name) as art:
            soup = BeautifulSoup(art, "html.parser")
        art.close()
        all_paras = soup.find_all('p')
        paragraphs = []
        for para in all_paras:
            paragraphs.append(para.get_text())
        content = ""
        for para in all_paras:
            content += para.get_text()
        content = content.encode('ascii', 'ignore')
        sentences = tokenize.sent_tokenize(content)
        counter = 0
        for sent in sentences:
            instance = Sentence("s" + str(counter), sent)
            counter += 1
            sentence_arr.append(instance)
        return sentence_arr

    def ranked_list(self, question):
        return None

inst = Information_Retrieval('article.htm')
print(len(inst.parse_html()))
