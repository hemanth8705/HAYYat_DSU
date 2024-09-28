import nltk
nltk.download('stopwords')
import spacy

# Load the spaCy model for lemmatization
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
tokenizer = nltk.tokenize.ToktokTokenizer()

import re
import string
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from googletrans import Translator

# Initialize stopword list and remove 'no', 'not' to retain negations
stopword_list = stopwords.words('english')
stopword_list.remove('no')
stopword_list.remove('not')


def translate_to_english(text):
    translator = Translator()
    # Detect the language of the text
    detected_language = translator.detect(text).lang
    
    # If the language is not English, translate it
    if detected_language != 'en':
        translated_text = translator.translate(text, dest='en').text
        return translated_text
    return text
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
    text = translate_to_english(text)
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


