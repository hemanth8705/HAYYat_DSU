import nltk
nltk.download('stopwords')
import spacy

from analyze_sentiment.sentiment_analyzer import analyze_sentiment
# Load the spaCy model for lemmatization
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
tokenizer = nltk.tokenize.ToktokTokenizer()

import re
import string
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
import pandas as pd
import json

# Initialize stopword list and remove 'no', 'not' to retain negations
stopword_list = stopwords.words('english')
stopword_list.remove('no')
stopword_list.remove('not')



def remove_escape_sequences(text):
    # print("Removing escape sequences...")
    return re.sub(r'\t|\n|\r', '', text)

def remove_punctuations(text):
    # print("Removing punctuations...")
    return text.translate(str.maketrans('', '', string.punctuation))

def remove_stopwords(text):
    # print("Removing stopwords...")
    tokens = tokenizer.tokenize(text)
    tokens = [token for token in tokens if token.lower() not in stopword_list]
    return ' '.join(tokens)

def remove_special_characters(text):
    # print("Removing special characters...")
    return re.sub('[^a-zA-Z0-9\s]', '', text)

def remove_html_tags(text):
    # print("Removing HTML tags...")
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)

def remove_urls(text):
    # print("Removing URLs...")
    return re.sub(r'https?://\S+|www\.\S+', '', text)

def remove_numbers(text):
    # print("Removing numbers...")
    return re.sub(r'\d+', '', text)

def lemmatize_text(text):
    # print("Lemmatizing text...")
    doc = nlp(text)
    return ' '.join([token.lemma_ if token.lemma_ != '-PRON-' else token.text for token in doc])

def preprocess_text(text):
    # print("Starting text preprocessing...")
    text = text.lower()
    text = remove_escape_sequences(text)
    text = remove_html_tags(text)
    text = remove_urls(text)
    text = remove_punctuations(text)
    text = remove_stopwords(text)
    text = remove_special_characters(text)
    text = remove_numbers(text)
    text = lemmatize_text(text)
    # print("Text preprocessing completed.")
    return text









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
        json_file.write(json_output)
    
    return 1



# Build the full path
file_path = r'scraped_data\news_articles.csv'

def save_sentiment_file_articles():
    try:
        data = pd.read_csv(file_path)
        print(data.head())
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