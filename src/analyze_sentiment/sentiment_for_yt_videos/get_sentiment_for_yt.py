import pandas as pd
from analyze_sentiment.sentiment_for_yt_videos.analyze_yt_and_save import add_sentiment_tags_yt


file_path =  r'scraped_data/yt_data.json'


def save_sentiment_file_yt():
    try:
        data = pd.read_json(file_path)
        flag = add_sentiment_tags_yt(data)
        return flag
    except Exception as e:
        print(e)
        print("File not found. Please check the path.")
        return None
    
if __name__ == "__main__":
    flag = save_sentiment_file_yt()
    if flag:
        print("Sentiment analysis completed successfully.")
    else:
        print("Failed to perform sentiment analysis.")
