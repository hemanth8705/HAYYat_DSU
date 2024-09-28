import time
import json
import sys
import os
import subprocess
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Function to load results from the JSON files
def load_results(file_name):
    with open(os.path.join('data', file_name), 'r') as f:
        return json.load(f)

# Functions to trigger different processes
def senddata_articles(general_search, twitter_search):
    success = subprocess.call(['python', 'articles.py', general_search, twitter_search])
    if success == 0:
        return load_results('news_articles.json')
    return None

def senddata_twitter_id(general_search, twitter_search):
    success = subprocess.call(['python', 'twitter_id.py', general_search, twitter_search])
    if success == 0:
        return load_results('comments_on_id.json')
    return None

def senddata_twitter_search(general_search, twitter_search):
    success = subprocess.call(['python', 'twitter_search.py', general_search, twitter_search])
    if success == 0:
        return load_results('tweets_on_search.json')
    return None

def senddata_yt(general_search, twitter_search):
    success = subprocess.call(['python', 'youtube.py', general_search, twitter_search])
    if success == 0:
        return load_results('yt_data.json')
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results.html')
def results_page():
    return render_template('results.html')

@app.route('/search/articles/<general_search>/<twitter_search>', methods=['GET'])
def search_articles(general_search, twitter_search):
    results = senddata_articles(general_search, twitter_search)
    return jsonify({"results": results})

@app.route('/search/twitter_id/<general_search>/<twitter_search>', methods=['GET'])
def search_twitter_id(general_search, twitter_search):
    results = senddata_twitter_id(general_search, twitter_search)
    return jsonify({"results": results})

@app.route('/search/twitter_search/<general_search>/<twitter_search>', methods=['GET'])
def search_twitter_search(general_search, twitter_search):
    results = senddata_twitter_search(general_search, twitter_search)
    return jsonify({"results": results})

@app.route('/search/youtube/<general_search>/<twitter_search>', methods=['GET'])
def search_youtube(general_search, twitter_search):
    results = senddata_yt(general_search, twitter_search)
    return jsonify({"results": results})

@app.route('/tweets/<sentiment>')
def display_tweets(sentiment):
    # Load the results from the JSON file
    results = load_results('results3.json')  # Assuming this is the relevant JSON file
    # Filter tweets based on sentiment
    filtered_tweets = [tweet for tweet in results if tweet['sentiment'].lower() == sentiment.lower()]
    return render_template('tweets.html', tweets=filtered_tweets)

if __name__ == '__main__':
    app.run(debug=True)
