from flask import Flask, redirect, render_template, request, url_for
import os
import sys
import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name,count=100)

    # TODO
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")


    abs_positive, abs_negative, abs_neutral = 0.0, 0.0, 0.0
    # instantiate analyzer
    analyzer = Analyzer(positives, negatives)
    results = []
    for i in range(len(tweets)):
        score = analyzer.analyze(tweets[i])
        results.append(score)
        if score > 0.0:
            #print(colored(tweets[i], "green"), colored(results[i],'green'))
            abs_positive += 1
        elif score < 0.0:
            #print(colored(tweets[i], "red"), colored(results[i],'red'))
            abs_negative += 1
        else:
            #print(colored(tweets[i], "yellow"), colored(results[i],'yellow'))
            abs_neutral += 1

    # get the total to easy calc %
    total = abs_positive + abs_negative + abs_neutral

    positive = (abs_positive / total) * 100
    negative = (abs_negative / total) * 100
    neutral = (abs_neutral / total) * 100

    #positive, negative, neutral = 0.0, 0.0, 100.0

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)



# Look (back) at tweets for inspiration!

# Complete the implementation of search in application.py in such a way that the function

# queries Twitter’s API for a user’s most recent 100 tweets,

# classifies each tweet as positive, negative, or neutral,

# generates a chart that accurately depicts those sentiments as percentages.

# If a user has tweeted fewer than 100 times, classify as many tweets as exist.