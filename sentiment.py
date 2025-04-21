from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import torch
from utils import preprocess_tweet

MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
labels = ['Negative', 'Neutral', 'Positive']

def analyze_sentiment(tweet):
    tweet = preprocess_tweet(tweet)
    encoded = tokenizer(tweet, return_tensors='pt')
    with torch.no_grad():
        output = model(**encoded)
    scores = softmax(output.logits[0].numpy())
    sentiment = labels[scores.argmax()]
    return sentiment, dict(zip(labels, [round(float(s), 4) for s in scores]))
