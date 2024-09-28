import time
import json
import sys
import os
from data_collection.twitter_news.tweets_on_specific_id import start_twitter_scraping_on_id

from analyze_sentiment.sentiment_for_twitter_id.get_sentiment_for_twitter_comments import save_sentiment_file_tweet_comments
def search_twitter_id(general_search, profile_username):
    start1 = time.time()
    # start_twitter_scraping_on_id(profile_username)
    end1 = time.time()
    

    start = time.time()
    # save_sentiment_file_tweet_comments()
    end = time.time()

    print(f"twitter comments on id : {end1 - start1} seconds.")
    print(f"Sentiment Analysis for twitter comments on id : {end - start} seconds.")


    return 0

if __name__ == '__main__':
    general_search = sys.argv[1]
    twitter_search = sys.argv[2]
    result = search_twitter_id(general_search, twitter_search)
    sys.exit(result)
