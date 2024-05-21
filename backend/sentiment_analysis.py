from transformers import pipeline

# Explicitly specify the model and revision
sentiment_pipeline = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english", 
    revision="af0f99b"
)

def analyze_sentiment(text):
    result = sentiment_pipeline(text)
    return result[0]