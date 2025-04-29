from flask import Flask, render_template, request, flash
from sentiment import analyze_sentiment
import csv
import io

app = Flask(__name__)
app.secret_key = 'dev'  # Needed for flash messages

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    summary = {"Positive": 0, "Neutral": 0, "Negative": 0}
    errors = []

    if request.method == "POST":
        print("POST request received")
        if "file" in request.files and request.files["file"].filename != "":
            print("File upload detected")
            file = request.files["file"]
            try:
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_input = csv.DictReader(stream)
                tweets = []
                for row in csv_input:
                    if "text" in row and row["text"].strip():
                        tweets.append(row["text"].strip())
                print(f"Extracted {len(tweets)} tweets from CSV")
                if not tweets:
                    errors.append("CSV file does not contain any tweets in 'text' column.")
            except Exception as e:
                errors.append(f"Error processing CSV file: {str(e)}")
        else:
            print("No file uploaded, using textarea input")
            tweets_input = request.form.get("tweets", "")
            tweets = [t.strip() for t in tweets_input.strip().split("\n") if t.strip()]
            print(f"Extracted {len(tweets)} tweets from textarea")

        # Limit number of tweets to analyze for performance
        max_tweets = 500
        for tweet in tweets[:max_tweets]:
            try:
                sentiment, scores = analyze_sentiment(tweet)
                summary[sentiment] += 1
                results.append({
                    "original_tweet": tweet,
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

