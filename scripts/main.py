#!/usr/bin/env python3
"""
Main orchestration script for Free Reels Bot.
Fetches news, generates voiceover, creates video, and uploads to YouTube/Instagram.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from rss import fetch_articles
from summarize import summarize_article
from tts import generate_voiceover
from make_reel import create_video_reel
from upload_youtube import upload_to_youtube

def main():
    """Main workflow: fetch -> summarize -> TTS -> create video -> upload"""
    
    print("[1] Fetching articles from RSS feeds...")
    articles = fetch_articles("rss_sources.txt", max_stories=int(os.getenv("MAX_STORIES", 3)))
    
    if not articles:
        print("No articles fetched. Exiting.")
        return
    
    print(f"[2] Got {len(articles)} articles. Summarizing...")
    summaries = [summarize_article(a["content"]) for a in articles]
    
    print("[3] Generating voiceover audio...")
    audio_file = generate_voiceover(summaries, lang=os.getenv("LANG", "en"))
    
    print("[4] Creating video reel...")
    video_file = create_video_reel(summaries, audio_file, articles)
    
    print("[5] Uploading to YouTube Shorts...")
    video_url = upload_to_youtube(video_file, articles)
    print(f"✓ Video uploaded: {video_url}")
    
    print("\n[✓] Workflow complete!")

if __name__ == "__main__":
    main()
