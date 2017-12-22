import nltk
from nltk.tokenize import TweetTokenizer
tkn = TweetTokenizer()
import os
import sys


class Analyzer():
    """Implements sentiment analysis."""
    #positives = os.path.join(sys.path[0], "positive-words.txt")
    #negatives = os.path.join(sys.path[0], "negative-words.txt")

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        negativeWords = open(negatives,"r")
        self.neg_array = negativeWords.readlines()
        positiveWords = open(positives,"r")
        self.pos_array = positiveWords.readlines()

    def analyze(self, text):
        self.text = tkn.tokenize(str.lower(text))
        score = 0
        for i in range(len(self.text)):
            try:
                if self.pos_array.index(self.text[i] + '\n') > -1:
                    score = score + 1
            except ValueError:
                try:
                    if self.neg_array.index(self.text[i] + '\n') > -1:
                        score = score - 1
                except ValueError:
                    score = score + 0
        return score
