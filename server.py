from flask import Flask, escape, request,render_template
from dotenv import load_dotenv
import requests
import json
import os
app = Flask(__name__, static_url_path='')

@app.route('/')
def home():
    search_item = request.args.get('search_item')
    tweets_json = get_tweets(search_item)
    tweets_dict_list = json.loads(tweets_json).get('statuses')
    if tweets_dict_list is None:
        tweets_dict_list = []

    good_and_bad_counter = []


    for tweet_dict in tweets_dict_list:
        analysis = run_analysis(tweet_dict['text'])
        good_and_bad_counter.append(analysis)
    
    return render_template('index.html', tweet_objs=tweets_dict_list, counter = good_and_bad_counter )


def get_tweets(searchitem): 
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23{}'.format(searchitem)
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")
    headers = {'authorization': 'Bearer {}'.format(BEARER_TOKEN)}
    res = requests.get(url, headers=headers)
    return res.content

def run_analysis(tweet_text):
    tweet_text = tweet_text.lower()
    with open('positive.txt', 'r') as f:
        good_words = set(f.read().split("\n"))
    with open('negative.txt', 'r') as f:
        bad_words = set(f.read().split("\n"))

    words = tweet_text.split(" ")
    good_counter = 0
    bad_counter = 0
    for word in words:
        word= word.strip()
        if word in good_words:
            good_counter += 1
        if word in bad_words:
            bad_counter += 1
    return (good_counter, bad_counter)





if __name__== '__main__':
    app.run()



