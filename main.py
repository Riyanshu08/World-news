from flask import Flask, render_template, jsonify
import feedparser
from textblob import TextBlob

app = Flask(__name__)

# Google News RSS for global headlines
RSS_URL = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"

def get_live_news():
    feed = feedparser.parse(RSS_URL)
    articles = []
    for entry in feed.entries[:15]: # Get top 15 breaking stories
        title = entry.title
        # Simple sentiment evaluation
        polarity = TextBlob(title).sentiment.polarity
        sentiment = "Positive" if polarity > 0.1 else "Negative" if polarity < -0.1 else "Neutral"
        
        articles.append({
            "title": title,
            "link": entry.link,
            "published": getattr(entry, 'published', 'Recent'),
            "sentiment": sentiment
        })
    return articles

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/news")
def api_news():
    return jsonify(get_live_news())

if __name__ == "__main__":
    app.run(debug=True, port=5000)