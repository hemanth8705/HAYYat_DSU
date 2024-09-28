import time
import json
import sys
import os
from data_collection.twitter_news.tweets_on_search import start_twitter_scraping_on_search
from analyze_sentiment.sentiment_for_twitter_search.get_sentiment_for_tweets import save_sentiment_file_tweets
def search_twitter(general_search, twitter_search):
    
    start1 = time.time()
    start_twitter_scraping_on_search(general_search , limit = 5)
    end1 = time.time()
    

    start = time.time()
    save_sentiment_file_tweets()
    end = time.time()

    print(f'Collect tweets on search: {end1 - start1} seconds')
    print(f'Sentiment analysis on tweets on search: {end - start} seconds')

    return 0

if __name__ == '__main__':
    general_search = sys.argv[1]
    twitter_search = sys.argv[2]
    result = search_twitter(general_search, twitter_search)
    sys.exit(result)
