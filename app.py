from flask import Flask, render_template, request, flash
from sentiment import analyze_sentiment
from utils import fetch_tweet_content

app = Flask(__name__)
app.secret_key = 'dev'  # Needed for flash messages

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    summary = {"Positive": 0, "Neutral": 0, "Negative": 0}
    errors = []

    if request.method == "POST":
        tweets_input = request.form["tweets"]
        tweets = [t.strip() for t in tweets_input.strip().split("\n") if t.strip()]

        for tweet in tweets:
            try:
                # Check if it's a Twitter URL
                if tweet.startswith(('http://', 'https://')) and 'twitter.com' in tweet:
                    tweet_content = None
                    try:
                        tweet_content = fetch_tweet_content(tweet)
                        if not tweet_content:
                            errors.append(f"Could not fetch content from: {tweet}")
                            continue
                    except ValueError as e:
                        errors.append(str(e))
                        continue

                sentiment, scores = analyze_sentiment(tweet_content if tweet.startswith('http') else tweet)
                summary[sentiment] += 1
                results.append({
                    "original_tweet": tweet_content if tweet.startswith('http') else tweet,
                    "tweet": tweet,
                    "sentiment": sentiment, 
                    "scores": scores
                })
            except Exception as e:
                errors.append(f"Error analyzing: {tweet} - {str(e)}")

    return render_template("index.html", 
                         results=results, 
                         summary=summary,
                         errors=errors)

if __name__ == "__main__":
    app.run(debug=True)
