from textblob import TextBlob
import pandas as pd
import json
from analyze_sentiment.sentiment_for_twitter_search.preprocessing import preprocess_text

# Function to determine sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    print(blob.sentiment.polarity)
    positive_sentiment = max(blob.sentiment.polarity, 0)
    positive_sentiment = round(positive_sentiment, 2)
    negative_sentiment = min(blob.sentiment.polarity, 0)
    negative_sentiment = round(negative_sentiment, 2)
    if positive_sentiment != 0:
        return "Positive",positive_sentiment
    return "Negative",negative_sentiment


def add_sentiment_tags_for_tweets(data):
    data[["preProcessed_text"]] = data['tweet'].apply(lambda x: pd.Series(preprocess_text(x)))


    data[['sentiment', 'intensity']] = data['preProcessed_text'].apply(lambda x: pd.Series(analyze_sentiment(x)))

    sentiment_counts = data['sentiment'].value_counts()

    # Calculate percentages
    total_count = len(data)
    positive_percentage = (sentiment_counts.get('Positive', 0) / total_count) * 100
    negative_percentage = (sentiment_counts.get('Negative', 0) / total_count) * 100
    positive_percentage = round(positive_percentage ,2)
    negative_percentage = round(negative_percentage , 2)

    # Create a list of dictionaries in the desired format
    json_list = []
    for _, row in data.iterrows():
        json_list.append({
            "user_id" : row['username'],
            'url': row['url'],
            'tweet': row['tweet'],
            'sentiment': row['sentiment'],
            'intensity': row['intensity']
        })
    json_list.append({
    "positive_percentage" : positive_percentage,
    "negative_percentage" : negative_percentage
    })
    
    # Convert to JSON string
    json_output = json.dumps(json_list, indent=4)

    # Save to a JSON file
    file_path = r"data\tweets_on_search.json"
    with open(file_path, 'w') as json_file:
        json_file.write(json_output)
    
    return 2