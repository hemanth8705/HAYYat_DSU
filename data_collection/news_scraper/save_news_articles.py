from get_news_articles import bing_news_scraper

def start_news_scraping(query):
    df = bing_news_scraper(query, max_articles=10)  # Limit to 70 articles

    filepath = r"../data/news_articles.csv"
    df.to_csv(filepath , index= True)

if __name__ == "__main__":
    # Example usage
    query = "elon musk and his satellite"
    start_news_scraping(query)