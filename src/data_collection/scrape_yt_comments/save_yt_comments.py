from get_yt_comments import get_yt_data
import pandas as pd

def start_yt_comments_scraping(query):
    comments_df = get_yt_data(query , limit = 10)

    # Save the DataFrame to a CSV file
    filepath = r"scraped_data/news_articles.csv"
    comments_df.to_csv(filepath , index= True)

if __name__ == "__main__":
    # Example usage
    query = "elon musk and his satellite"
    start_yt_comments_scraping(query)