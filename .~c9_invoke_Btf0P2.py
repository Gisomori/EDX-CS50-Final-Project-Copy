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
news = fetch_20newsgroups(subset='all')
import feedparser
from feedfinder2 import find_feeds
import numpy as np
import helpers1

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# starting point of the app
@app.route("/")
def index():

    """Index page."""
    return render_template('index.html')

# when input, handle the input
@app.route("/",methods=['POST'])
def get_rss():
    if request.form['yesno'] == 'rss':
        # if input is empty flash message, reload page
        if not request.form.get('insert_rss'):
            flash('Forgot RSS Link :/')
            return render_template('index.html')
        # get rss link, and then crawl through it
        input_rss = request.form.get('insert_rss')
        crawled_feed = helpers1.rss_analyzer(feedparser.parse(input_rss))

        # return a list
        crawled_feed, max_pos, max_neg, distribution, \
        content_sentiment_outcome, title_sentiment_outcome = helpers1.stats_grabber(crawled_feed)

        sentiment_title_chart = helpers1.sentiment_title_chart(title_sentiment_outcome,'Sentiment of Titles observed')

        sentiment_content_chart = helpers1.sentiment_title_chart(content_sentiment_outcome,'Sentiment of Contents observed')

        scoring_boxplot = helpers1.sentiment_boxpot(title=np.asarray(crawled_feed['Title Score']),\
                                                    content=np.asarray(crawled_feed['Content Score']))

        title_cat_boxplot = helpers1.category_boxplot(dataframe=crawled_feed,title = 'Title Topic Sentiment Distribution',\
                                                    values='Title Score',columns='Title Topic')

        content_cat_boxplot = helpers1.category_boxplot(dataframe=crawled_feed,title = 'Content Topic Sentiment Distribution',\
                                                    values='Content Score',columns='Content Topic')

        return render_template("rss_output.html",table=crawled_feed.to_html(),title_chart = sentiment_title_chart, \
                                content_chart = sentiment_content_chart,inputted_url = input_rss,\
                                posit_example = max_pos.to_html(), negat_example = max_neg.to_html(), \
                                scoring_boxplot = scoring_boxplot, title_cat_boxplot = title_cat_boxplot, \
                                content_cat_boxplot = content_cat_boxplot)
    if request.form['yesno'] == 'crawl':
        if not request.form.get('insert_url'):
            flash('Forgot URL')
            return render_template('index.html')
        insert_url = request.form.get('insert_url')
        feed = helpers1.get_feed(insert_url)
        crawled_feed = helpers1.rss_analyzer(feed)
        crawled_feed.language
        crawled_feed, max_pos, max_neg, distribution, \
        content_sentiment_outcome, title_sentiment_outcome = helpers1.stats_grabber(crawled_feed)

        sentiment_title_chart = helpers1.sentiment_title_chart(title_sentiment_outcome,'Sentiment of Titles observed')

        sentiment_content_chart = helpers1.sentiment_title_chart(content_sentiment_outcome,'Sentiment of Contents observed')

        scoring_boxplot = helpers1.sentiment_boxpot(title=np.asarray(crawled_feed['Title Score']),\
                                                    content=np.asarray(crawled_feed['Content Score']))

        title_cat_boxplot = helpers1.category_boxplot(dataframe=crawled_feed,title = 'Title Topic Sentiment Distribution',\
                                                    values='Title Score',columns='Title Topic')

        content_cat_boxplot = helpers1.category_boxplot(dataframe=crawled_feed,title = 'Content Topic Sentiment Distribution',\
                                                    values='Content Score',columns='Content Topic')

        return render_template("rss_output.html",table=crawled_feed.to_html(),title_chart = sentiment_title_chart, \
                                content_chart = sentiment_content_chart,inputted_url = insert_url, \
                                posit_example = max_pos.to_html(), negat_example = max_neg.to_html(), \
                                scoring_boxplot = scoring_boxplot,title_boxplot = title_cat_boxplot, \
                                content_cat_boxplot = content_cat_boxplot)



# need to now write function to process all the sentiment/ML in one time, output into proper chart.
# consider to make one page app, or multiple pages. Need to see what works better. Best would be to handle all of it with AJAX.


