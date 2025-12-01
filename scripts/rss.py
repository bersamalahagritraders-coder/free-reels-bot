"""RSS Feed Fetcher - Fetches articles from multiple news sources."""

import feedparser
from datetime import datetime

def fetch_articles(rss_file, max_stories=3):
    """Fetch latest articles from RSS feeds listed in file."""
    
    articles = []
    
    try:
        with open(rss_file, "r") as f:
            feeds = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {rss_file} not found")
        return []
    
    for feed_url in feeds:
        try:
            print(f"  Fetching from {feed_url[:50]}...")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:max_stories]:
                article = {
                    "title": entry.get("title", "No Title"),
                    "content": entry.get("summary", entry.get("description", "")),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", datetime.now().isoformat())
                }
                articles.append(article)
                
        except Exception as e:
            print(f"  Error fetching {feed_url}: {str(e)}")
            continue
    
    return articles[:max_stories]
