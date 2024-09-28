from textblob import TextBlob
import pandas as pd
import json
from analyze_sentiment.preprocessing import preprocess_text

def analyze_sentiment(text):
    blob = TextBlob(text)
    # print(blob.sentiment.polarity)
    positive_sentiment = max(blob.sentiment.polarity, 0)
    positive_sentiment = round(positive_sentiment, 2)
    negative_sentiment = min(blob.sentiment.polarity, 0)
    negative_sentiment = round(negative_sentiment, 2)
    if positive_sentiment != 0:
        return "Positive",positive_sentiment
    return "Negative",negative_sentiment



def analyze_comments(row):
    positive_count = 0
    negative_count = 0
    
    for comment in row['comments']:
        sentiment, intensity = analyze_sentiment(comment[0])
        comment.append((sentiment, intensity))  # Assuming comment is a list
        
        if sentiment == 'Positive':
            positive_count += 1
        elif sentiment == 'Negative':
            negative_count += 1
    
    # Calculate percentages
    total_comments = positive_count + negative_count
    positive_percentage = (positive_count / total_comments) * 100 if total_comments > 0 else 0
    negative_percentage = (negative_count / total_comments) * 100 if total_comments > 0 else 0
    
    return pd.Series({
        "positive_comments": round(positive_percentage, 2),
        "negative_comments": round(negative_percentage, 2),
        "sentiment": analyze_sentiment(row["srt"])[0],
        "intensity": analyze_sentiment(row["srt"])[1]
    })

def add_sentiment_tags_yt(data):
    # Apply the function to each row and update the DataFrame
    data[['positive_comments', 'negative_comments', 'sentiment', 'intensity']] = data.apply(analyze_comments, axis=1)
    file_path = r"data\yt_data.json"
    data.to_json(file_path, orient='records', indent=4)
    # print("saved json file to ",file_path)
    return 3