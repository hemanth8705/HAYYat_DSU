from textblob import TextBlob
import pandas as pd
import json
from preprocessing import preprocess_text

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


def add_sentiment_tags(data):
    data['Combined Text'] = data['Headline'] + " " + data['Full Article']

    data[["preProcessed_text"]] = data['Combined Text'].apply(lambda x: pd.Series(preprocess_text(x)))
    
    # Create new columns for sentiment analysis of the combined text
    data[['sentiment', 'intensity']] = data['preProcessed_text'].apply(lambda x: pd.Series(analyze_sentiment(x)))

    # Create a list of dictionaries in the desired format
    json_list = []
    for _, row in data.iterrows():
        json_list.append({
            'url': row['Link'],
            'headline': row['Headline'],
            'sentiment': row['sentiment'],
            'intensity': row['intensity']
        })
    
    # Convert to JSON string
    json_output = json.dumps(json_list, indent=4)

    # Save to a JSON file
    file_path = r"data\news_articles.json"
    with open(file_path, 'w') as json_file:
        # print("updated file in articles" , ">"*10)
        json_file.write(json_output)
    
    return 1
