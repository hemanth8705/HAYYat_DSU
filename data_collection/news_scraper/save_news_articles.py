from get_news_articles import bing_news_scraper

def start_news_scraping(query):
    df = bing_news_scraper(query, max_articles=1)  # Limit to maximum articles

    filepath = r"../../scraped_data/news_articles.csv"
    df.to_csv(filepath , index= True)

if __name__ == "__main__":
    # Example usage
    query = "banglore weather"
    start_news_scraping(query)