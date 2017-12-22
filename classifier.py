import os
import re
import urllib.request, json
import pandas as pd
from flask import Flask, jsonify, render_template, request, url_for, flash, redirect, session
from flask_jsglue import JSGlue
from flask_session import Session
from tempfile import mkdtemp
import requests
from bs4 import BeautifulSoup
import sys
from string import *
from analyzer import Analyzer
from nltk.stem import PorterStemmer
from nltk import word_tokenize
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.datasets import fetch_20newsgroups
from sklearn.externals import joblib
from sklearn.cross_validation import train_test_split
news = fetch_20newsgroups(subset='all')
import feedparser
from feedfinder2 import find_feeds
import helpers1
import string


def train(classifier, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)
    classifier.fit(X_train, y_train)
    print("Accuracy: %s" % classifier.score(X_test, y_test))
    return classifier

trial5 = Pipeline([
('vectorizer', TfidfVectorizer(tokenizer=helpers1.stemming_tokenizer,
stop_words=stopwords.words('english') + list(string.punctuation))),
('classifier', MultinomialNB(alpha=0.05)),
])

classifier = train(trial5, news.data, news.target)
joblib.dump(classifier, 'classifier.pkl')



# make sure to get the right url, and append later on https:// via https://  +  url


# # give later the option, to insert the direct RSS feed URL or an URL to be scanned for RSS feeds.
# # IF URL empty,give error.
# rss_links = find_feeds('http://www.currybet.net/cbet_blog/2007/11/top-100-bbc-rss-feeds-in-googl.php','lxml')
# # default take the first rss feed offer found in rss_links, might improve in the future
# feed = feedparser.parse(rss_links[0])
# crawled_feed = feed_crawler(feed)

# # traverse through crawled feed and add outcome from classifier to it

# clf = joblib.load('classifier.pkl')

#remove all paragraph <p> tags, ensure that new keys are being added to the object.
# for i in range(0,len(crawled_feed)):
#     crawled_feed[str(i)]['output_title'] = news.target_names[int(clf.predict([str(crawled_feed[str(i)]['title']).replace('<p>','').replace('</p>','')])[0])]
#     crawled_feed[str(i)]['output_content'] = news.target_names[int(clf.predict([str(crawled_feed[str(i)]['content']).replace('<p>','').replace('</p>','')])[0])]



# positives = os.path.join(sys.path[0], "positive-words.txt")
# negatives = os.path.join(sys.path[0], "negative-words.txt")

# abs_positive, abs_negative, abs_neutral = 0.0, 0.0, 0.0
# # instantiate analyzer
# analyzer = Analyzer(positives, negatives)
# for i in range(0,len(crawled_feed)):
#     crawled_feed[str(i)]['title_score'] = analyzer.analyze(str(crawled_feed[str(i)]['title']))
#     crawled_feed[str(i)]['content_score'] = analyzer.analyze(str(crawled_feed[str(i)]['content']))

#     # results.append(score)
#     # if score > 0.0:
#     #     #print(colored(tweets[i], "green"), colored(results[i],'green'))
#     #     abs_positive += 1
#     # elif score < 0.0:
#     #     #print(colored(tweets[i], "red"), colored(results[i],'red'))
#     #     abs_negative += 1
#     # else:
#     #     #print(colored(tweets[i], "yellow"), colored(results[i],'yellow'))
#     #     abs_neutral += 1

# # get the total to easy calc %
# # total = abs_positive + abs_negative + abs_neutral

# # positive = (abs_positive / total) * 100
# # negative = (abs_negative / total) * 100
# # neutral = (abs_neutral / total) * 100


# # find good tool to summarise sentiment and tags. pandas maybe something else.


# for x in range(0,len(crawled_feed)):
#     print(crawled_feed[str(x)]['title_score'], crawled_feed[str(x)]['title'])
#category_chart(dataframe=crawled_feed,column='output_title',title='test')


http://www.bbc.com/sport/rugby-league/42207590