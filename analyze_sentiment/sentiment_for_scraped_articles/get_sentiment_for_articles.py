## reading news articles
import os
import pandas as pd

from analyze_csv_file_and_save import add_sentiment_tags


# Get the current working directory
current_directory = os.getcwd()

# Build the full path
file_path = r'../../scraped_data/news_articles.csv'

def save_sentiment_file_articles():
    try:
        data = pd.read_csv(file_path)
        flag = add_sentiment_tags(data)
        return flag
    except Exception as e:
        print(e)
        print("File not found. Please check the path.")
        return None

if __name__ == "__main__":
    flag = save_sentiment_file_articles()
    if flag:
        print("Sentiment analysis completed successfully.")
    else:
        print("Failed to perform sentiment analysis.")