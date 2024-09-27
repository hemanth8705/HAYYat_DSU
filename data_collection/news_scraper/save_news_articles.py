from get_news_articles import bing_news_scraper

def start_news_scraping(query):
    df = bing_news_scraper(query, max_articles= 7)  # Limit to maximum articles

    filepath = r"../../scraped_data/news_articles.csv"
    df.to_csv(filepath , index= True)

if __name__ == "__main__":
    # Example usage
    query = "news about nithin ghatkari "
    start_news_scraping(query)