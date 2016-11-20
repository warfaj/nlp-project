import re

# makes word lower-case, removes punctuation
# allows the word to be stored in a dictionary better
def strip(word):
	w = word.lower()
	w = re.sub('[.!? ,:"\']', '', w)
	return w

def splitsentence(sentence):
	words = sentence.split()
	for i in xrange(len(words)):
		words[i] = strip(words[i])
	return words

class Parse:

	# initialization functions, takes in a string of text
	def __init__(self, raw_text):
		# lines = text.splitlines() # list of text line split by newline delimeter
		dictionary = {} # maps words to indices
		sentences = re.split('(?<=[.!?])\n+|(?<=[.!?]) +', raw_text) # list that maps indices to sentences
		self.dictionary = dictionary
		self.sentences = sentences
		for i in xrange(len(sentences)):
			words = splitsentence(sentences[i])
			for word in words:
				if word in dictionary:
					dictionary[word].add(i)
				else:
					dictionary[word] = {i}

	# given a word, returns all indices of sentences that contain the word
	def findword(self, word):
		w = strip(word)
		if w in self.dictionary:
			return self.dictionary[w]
		else:
			return set()

	# given a list of words, returns all indices of sentences containing all the words
	def findwords(self, words):
		if len(words) == 0:
			return set()
		indices = self.findword(words[0])
		for word in words[1:]:
			idxs = self.findword(word)
			indices = set.intersection(indices,idxs)
		return indices

	# given a string of words, returns all indices of sentences containing all the words
	def findsentence(self, sentence):
		words = splitsentence(sentence)
		return self.findwords(words)

	# given an index, returns the sentence
	def findidx(self, i):
		if 0 <= i and i < len(self.sentences):
			return self.sentences[i]
		else:
			return ''
