import re
import requests
from bs4 import BeautifulSoup

def extract_tweet_id(url):
    """Extract tweet ID from Twitter URL"""
    pattern = r'twitter\.com\/\w+\/status\/(\d+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def fetch_tweet_content(url):
    """Fetch tweet content from Twitter URL"""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tweet_div = soup.find('div', {'data-testid': 'tweetText'})
        if not tweet_div:
            raise ValueError("Could not find tweet content")
            
        return tweet_div.get_text()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch tweet: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing tweet: {str(e)}")

def preprocess_tweet(tweet):
    """Preprocess tweet text or fetch content from URL"""
    if tweet.startswith('http') and 'twitter.com' in tweet:
        tweet_content = fetch_tweet_content(tweet)
        if tweet_content:
            return tweet_content
    
    words = []
    for word in tweet.split():
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        elif word.startswith('http'):
            word = 'http'
        words.append(word)
    return " ".join(words)
