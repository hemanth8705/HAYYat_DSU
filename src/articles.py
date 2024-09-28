import time
import json
import sys
import os

from data_collection.news_scraper.save_news_articles import start_news_scraping

from analyze_sentiment.sentiment_for_scraped_articles.get_sentiment_for_articles import save_sentiment_file_articles
def search_articles(general_search, twitter_search):
    #Simulate some processing time (e.g., fetching articles)
    start1 = time.time()
    # print("general_search for articles",general_search)
    # start_news_scraping(general_search)
    end1 = time.time()

    

    start = time.time()
    # print("analyzing sentiment for articels")
    # save_sentiment_file_articles()
    end = time.time()

    print(f"Time taken to fetch articles: {end1 - start1} seconds")
    print(f"Time taken to analyze sentiment for articles: {end - start} seconds")
    

    return 0  # Return 0 to indicate successful completion

if __name__ == '__main__':
    general_search = sys.argv[1]
    twitter_search = sys.argv[2]
    result = search_articles(general_search, twitter_search)
    sys.exit(result)  # Exit with the result (0)
