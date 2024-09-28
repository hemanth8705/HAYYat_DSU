import pandas as pd
from analyze_sentiment.sentiment_for_twitter_id.analyze_twitter_comments_and_save import add_sentiment_tags_for_tweet_comments

file_path =  r'scraped_data/tweets_on_id.json'

def save_sentiment_file_tweet_comments():
    try:
        data = pd.read_json(file_path)
        flag = add_sentiment_tags_for_tweet_comments(data)
        return flag
    except Exception as e:
        print(e)
        print("File not found. Please check the path.")
        return None

# data = pd.read_json(file_path)
# flag = add_sentiment_tags_for_tweets(data)
if __name__ == "__main__":
    flag = save_sentiment_file_tweet_comments()
    if flag:
        print("Sentiment analysis completed successfully.")
    else:
        print("Failed to perform sentiment analysis.")
