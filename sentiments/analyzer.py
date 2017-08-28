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



# Odds are you’ll find nltk.tokenize.casual.TweetTokenizer of interest, which can be used to tokenize a tweet (i.e., split it up into a list of words) with code like:

# tokenizer = nltk.tokenize.TweetTokenizer()
# tokens = tokenizer.tokenize(tweet)
# For instance, if tweet is I love you, then tokens will be ["I", "love", "you"]. The tokenizer treats some punctuation as separate tokens, so not to worry if it splits words like a+ (which is in positive-words.txt) into two tokens.

# Be sure to ignore any comments or blank lines inside of positives and negatives.

# If you would like a variable to be accessible from both __init__ and analyze, be sure to define it as an "instance variable" inside of self. For instance, if you were to define

# self.n = 42
# inside of __init__, then self.n would also be accessible inside of analyze.

# Odds are you’ll find str.lower of interest.

# Note that get_user_timeline returns None in cases of error, as might happen if a screen name doesn’t exist or a screen name’s tweets are private.

# And here’s the time-complexity (aka "Big O" or "Big Oh") of various operations in current CPython, the implementation of Python we’re using (which is an interpreter called python, or really python3, which itself is actually written in C).