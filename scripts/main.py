#!/usr/bin/env python3
"""
Main orchestration script for Free Reels Bot - CONTINUOUS MODE.
Fetches ONE new article per run, generates video, and uploads to YouTube.
Tracks posted articles to avoid duplicates.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from rss import fetch_articles
from summarize import summarize_article
from tts import generate_voiceover
from make_reel import create_video_reel
from upload_youtube import upload_to_youtube

POSTED_FILE = "posted_articles.json"

def load_posted_articles():
    """Load list of already posted article links."""
    if os.path.exists(POSTED_FILE):
        try:
            with open(POSTED_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_posted_articles(links):
    """Save posted article links to avoid re-posting."""
    with open(POSTED_FILE, 'w') as f:
        json.dump(links, f)

def main():
    """Main workflow: fetch ONE article -> summarize -> TTS -> video -> upload"""
    
    posted_links = load_posted_articles()
    
    print("[1] Fetching latest news articles...")
    articles = fetch_articles("rss_sources.txt", max_stories=10)  # Fetch more, pick fresh ones
    
    if not articles:
        print("No articles fetched. Exiting.")
        return
    
    # Find first unposted article
    article_to_post = None
    for article in articles:
        if article.get("link") not in posted_links:
            article_to_post = article
            break
    
    if not article_to_post:
        print("No new articles found. All recent articles already posted.")
        return
    
    print(f"[2] Found NEW article: {article_to_post['title'][:60]}...")
    
    # Summarize this ONE article
    summary = summarize_article(article_to_post["content"])
    
    print("[3] Generating voiceover audio...")
    audio_file = generate_voiceover([summary], lang=os.getenv("LANG", "en"))
    
    print("[4] Creating video reel...")
    video_file = create_video_reel([summary], audio_file, [article_to_post])
    
    if not video_file:
        print("Video creation failed.")
        return
    
    print("[5] Uploading to YouTube Shorts...")
    video_url = upload_to_youtube(video_file, [article_to_post])
    
    if video_url:
        # Mark as posted
        posted_links.append(article_to_post.get("link"))
        save_posted_articles(posted_links)
        print(f"✓ Video posted: {video_url}")
        print(f"[✓] Run complete. Waiting for next news refresh ({len(posted_links)} posted so far).")
    else:
        print("Upload failed.")

if __name__ == "__main__":
    main()
