import requests
from bs4 import BeautifulSoup
import re
import os
import sys
from pandas import pandas as pd
import string
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
from sklearn.cross_validation import train_test_split
import string
import plotly
import textwrap
import numpy as np

# stemming tokenizer function found here :  http://nlpforhackers.io/text-classification/
def stemming_tokenizer(text):
    stemmer = PorterStemmer()
    return [stemmer.stem(w) for w in word_tokenize(text)]


# first version to search for RSS URL, later went for feedparser, leaving it here for reminiscence :p...
def get_rss_feed(website_url):
    if website_url is None:
        print("URL should not be null")
        return None
    else:
        x = []
        source_code = requests.get(website_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,"lxml")
        for link in soup.find_all("link", {"type" : "application/rss+xml"}):
            href = link.get('href')
            #print("RSS feed for " + website_url + "is -->" + str(href))
            x.append(href)
        return(x)

# improved version for searching RSS URL, it always picks the first RSS link, for speed.
# Future version might have multiple crawlers for all possible found RSS links.
def get_feed(url):
    # no url supplied, return None
    if url is None:
        print("URL should not be null")
        return None
    else:
        # ok url provided, but if nothing found None.
        rss_links = find_feeds(url,'lxml')
        if rss_links == []:
            return None
        feed = feedparser.parse(rss_links[0]) # always picks the first RSS link found in a website, whenever there are multiple ones (speed...).
        return feed

#crawler function looking for anything related to texts written in paragraphs.
def get_page_content(website_url):
    if website_url is None:
        return None
    else:
        # create list to store content
        content = []
        source_code = requests.get(website_url)
        soup = BeautifulSoup(source_code.content,"html.parser")
        # look for all content parts in the html
        temp = soup.find_all('p')
        # create regular expression to look for, in this case p tag
        start_text = re.compile("<p")
        avoid_text = re.compile("</p>")
        # iterate over it, when it finds it, appends it to the list, then returns it.
        for x in temp:
            if start_text.match(str(x)) is not None:
                if avoid_text.match(str(x)) is None:
                    content.append(x)
        return re.sub(r'<[^>]*?>', '', str(content)) # remove as many tags as possible.

# while traversing the found feeds, store them in a dictionary within a dictionary.
def feed_crawler(feed):
    storage = {}
    # If its empty we set it to Nothing found.
    try:
        lan = feed.feed.language
    except AttributeError:
        lan = 'Nothing found'
    for i in range(0,len(feed.entries)):
        if feed.entries[i].title =='': # if the title is empty, we do not need the RSS data. It is in a format which is not useful to the app.
            continue
        else:
            articles = {} # overwrite previous data for a new run
            articles['title'] = str(feed.entries[i].title)
            articles['language'] = lan
            articles['link'] = str(feed.entries[i].link)
            # some RSS links don't supply these information.
            # In the future, an author could be analyzed, to see what sentiment he is spreading
            # articles['author'] = feed.entries[i].author
            # articles['authors'] = feed.entries[i].authors
            # articles['identity'] = feed.entries[i].id

            #crawl through provided link in RSS , to go the original page, in order to get valuable text for analysis.
            content = get_page_content(feed.entries[i].link)
            articles['summary'] = feed.entries[i].summary
            articles['content'] = content
            storage[str(i)] = articles
    return storage



    #bbc examplee url
    #http://www.currybet.net/cbet_blog/2007/11/top-100-bbc-rss-feeds-in-googl.php





    #try tomorrow NLTK, and TextBlob . Read up on both. tryto get sentiments
    # textblob weak sentiment analysis for articles, might consider to get twitter words, lets see... indico seems to be good, but API based.

    #check these out
    # http://nlp.yvespeirsman.be/blog/off-the-shelf-sentiment-analysis/

    #download lexicon
    # http://www.cs.uic.edu/~liub/FBS/opinion-lexicon-English.rar

    # import urllib
    # response = urllib.urlopen('http://www.cs.uic.edu/~liub/FBS/opinion-lexicon-English.rar')
# html = response.read()

# def train(classifier, X, y):
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)
#     classifier.fit(X_train, y_train)
#     print("Accuracy: %s" % classifier.score(X_test, y_test))
#     return classifier


    # start with reading this, nice tutorial: http://www.cs.duke.edu/courses/spring14/compsci290/assignments/lab02.html
    # read up on http://nlpforhackers.io/text-classification/
    # also read up on http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
    # after reading these trhough go through the tutorial, understand the scikit parameters
    # http://scikit-learn.org/stable/tutorial/basic/tutorial.html



# ensure that the algo has enough tags.



# trial5 = Pipeline([
# ('vectorizer', TfidfVectorizer(tokenizer=stemming_tokenizer,
# stop_words=stopwords.words('english') + list(string.punctuation))),
# ('classifier', MultinomialNB(alpha=0.05)),
# ])

#train(trial5, news.data, news.target)

# # to save classifier


#joblib.dump(clf, 'classifier.pkl')


# The brain of the operation! Function allows us to judge text based on sentiment and classification (what category)
def rss_analyzer(rss):
    import os
    import sys
    import pandas as pd
    # import cs50 analyzer function from the sentiment pset
    from analyzer import Analyzer
    # store data in the right format we need, with feed_crawler
    crawled_feed = feed_crawler(rss)
    # load pickled(stored) pretrained ML classifier trained with classifier.py.
    clf = joblib.load('classifier.pkl')
    # iterate through feed
    for i in crawled_feed:
        crawled_feed[i]['output_title'] = news.target_names[int(clf.predict([str(crawled_feed[i]['title']).replace('<p>','').replace('</p>','')])[0])] # apply ML classifier
        crawled_feed[i]['output_content'] = news.target_names[int(clf.predict([str(crawled_feed[i]['content']).replace('<p>','').replace('</p>','')])[0])] # dito
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")
    bs_positive, abs_negative, abs_neutral = 0.0, 0.0, 0.0
    analyzer = Analyzer(positives, negatives)
    for i in crawled_feed:
        crawled_feed[i]['title_score'] = analyzer.analyze(str(crawled_feed[i]['title'])) # judge with analyzer function sentiment of title
        crawled_feed[i]['content_score'] = analyzer.analyze(str(crawled_feed[i]['content'])) # here for the content, which was retrieved from the original URL provided in the RSS.
    pd.set_option('display.max_colwidth', -1) # ensure data is visualized properly
    return pd.DataFrame(crawled_feed).T # return a transposed dataframe


# after having dynamically judged what the found articles in the URL are about, it's time to summarise the stats.
def stats_grabber(crawled_feed):

    # format the sentiment score to numeric
    crawled_feed.content_score = pd.to_numeric(crawled_feed.content_score)
    crawled_feed.title_score = pd.to_numeric(crawled_feed.title_score)

    #create column to judge content sentiment via if statement in pandas
    crawled_feed['content_group'] = 'positive'
    crawled_feed['content_group'][crawled_feed['content_score'] < 0] = 'negative'
    crawled_feed['content_group'][crawled_feed['content_score'] == 0] = 'neutral'

    #same as above for title
    crawled_feed['title_group'] = 'positive'
    crawled_feed['title_group'][crawled_feed['title_score'] < 0] = 'negative'
    crawled_feed['title_group'][crawled_feed['title_score'] == 0] = 'neutral'

    # return sentiment score summary, for later use.
    content_sentiment_outcome = crawled_feed['content_group'].value_counts()
    title_sentiment_outcome = crawled_feed['title_group'].value_counts()

    #distribution = crawled_feed.content_score.describe() # not necessary to output, but allows for simple summary statistics (mean, q1-q3, min,max, stdv)

    #rearrange and remove not used columns
    crawled_feed= crawled_feed[['link','title','title_score','title_group','output_title','content','content_score','content_group','output_content']]

    #rename columns
    crawled_feed= crawled_feed.rename(columns={'title_group':'Title Sentiment','output_title': 'Title Topic','content_group':'Content Sentiment','output_content': 'Content Topic', \
                                                'link':'Link','title':'Title','title_score':'Title Score','content_score':'Content Score','content':'Content'})
    #find the highest sentiment score in content f
    max_pos = crawled_feed.nlargest(1,'Content Score')
    max_pos['Content'] = textwrap.shorten(str(max_pos['Content']),width=100)
    max_neg = crawled_feed.nsmallest(1,'Content Score')
    max_neg['Content'] = textwrap.shorten(str(max_neg['Content']),width=100)
    
    

    return crawled_feed, max_pos, max_neg, distribution, content_sentiment_outcome, title_sentiment_outcome



def sentiment_title_chart(outcome,title):
    try:
        positive = outcome.positive
    except AttributeError:
        positive = 0
    try:
        negative = outcome.negative
    except AttributeError:
        negative = 0
    try:
        neutral = outcome.neutral
    except AttributeError:
        neutral = 0

    figure = {
        "data": [
            {
                "labels": ["Positive Articles", "Negative Articles", "Neutral Articles"],
                "hoverinfo": "none",
                "marker": {
                    "colors": [
                        "rgb(0,255,00)",
                        "rgb(255,0,0)",
                        "rgb(255,255,0)"
                    ]
                },
                "type": "pie",
                "values": [positive, negative, neutral]
            }
        ],
        "layout": {
            "title": title,
            "showlegend": True
            }
    }
    return plotly.offline.plot(figure, output_type="div", show_link=False, link_text=False)


def sentiment_boxpot(title, content):
    import plotly.plotly as py
    import plotly.graph_objs as go
    title_trace = go.Box(
            y=title,
            name = 'Title Score'
    )
    content_trace = go.Box(
            y=content,
            name = 'Content Score'
    )
    data = [title_trace, content_trace]

    layout = go.Layout(
            title = 'Sentiment Distribution'
    )
    fig = go.Figure(data=data,layout=layout)
    return plotly.offline.plot(fig,output_type="div",show_link=False,link_text=False)


def category_boxplot(dataframe,columns,values,title):
    import plotly.plotly as py
    import plotly.graph_objs as go
    dataframe = dataframe.pivot(columns=columns,values=values)
    data = [{
        'y': dataframe[i],
        'type':'box',
        'name': i
        } for i in dataframe]
    layout = {'xaxis': {'showgrid':False,'zeroline':False, 'tickangle':60,'showticklabels':False},
          'yaxis': {'zeroline':False,'gridcolor':'white'},
          'paper_bgcolor': 'rgb(233,233,233)',
          'plot_bgcolor': 'rgb(233,233,233)',
          'title': title
          }
    fig = go.Figure(data=data,layout=layout)
    return plotly.offline.plot(fig,output_type="div",show_link=False,link_text=False)

# from selenium import webdriver
# br = webdriver.PhantomJS()
# br.get('http://www.stackoverflow.com')
# br.save_screenshot('screenshot.png')
# br.quit


#df.groupby(['col5','col2'])

#df[['col1', 'col2', 'col3', 'col4']].groupby(['col1', 'col2']).agg(['mean', 'count'])


# crawled_feed, max_pos, max_neg, distribution, \
# content_sentiment_outcome, title_sentiment_outcome = helpers1.stats_grabber(crawled_feed)

# sentiment_content_chart = helpers1.sentiment_title_chart(content_sentiment_outcome.positive, \
#                         content_sentiment_outcome.negative,content_sentiment_outcome.neutral)


# ADD SOURCES!
# clean code
# be done

#crawl.pivot(columns='output_title',values='title_score')