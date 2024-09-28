import time
import json
import sys
import os

from data_collection.scrape_yt_comments.get_yt_comments import get_yt_data
from analyze_sentiment.sentiment_for_yt_videos.get_sentiment_for_yt import save_sentiment_file_yt

def search_youtube(general_search, twitter_search):
    # Simulate processing time
    start1 = time.time()
    get_yt_data(general_search)
    end1 = time.time()

    start = time.time()
    save_sentiment_file_yt()
    end = time.time()


    print(f"Fetch YouTube comments: {end1 - start1} seconds")
    print(f"Fetch sentiment for YouTube comments : {end - start} seconds")
    


    return 0  # Return 0 to indicate successful completion

if __name__ == '__main__':
    general_search = sys.argv[1]
    twitter_search = sys.argv[2]
    result = search_youtube(general_search, twitter_search)
    sys.exit(result)
