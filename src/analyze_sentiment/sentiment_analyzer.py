from transformers import pipeline

# Load the sentiment analysis pipeline
distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
    return_all_scores=True
)

def analyze_sentiment(text):
    text = text[:511]
    # Use the Hugging Face model for sentiment analysis
    results = distilled_student_sentiment_classifier(text)
    
    # Extract positive and negative sentiment scores
    res = {}
    for x in results[0]:
      if x['label'] == 'positive':
        res['positive'] = round(x['score'] , 2)
      if x['label'] == 'negative':
        res['negative'] = round(x['score'] , 2)
      if x['label'] == 'neutral':
        res['neutral'] = round(x['score'] , 2)

    # print(res)
    if res['positive'] > res['negative']:
        # print("ans : Positive", res['positive'] )
        return "Positive", res['positive']
    print("ans : Negative", res['negative'] )
    return "Negative", res['negative']


