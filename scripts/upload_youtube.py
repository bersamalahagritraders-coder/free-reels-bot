"""Upload video to YouTube Shorts using YouTube Data API."""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    """Authenticate with YouTube API using credentials from environment."""
    credentials = None
    
    try:
        from google.oauth2.credentials import Credentials
        
        client_id = os.getenv('YTB_CLIENT_ID')
        client_secret = os.getenv('YTB_CLIENT_SECRET')
        refresh_token = os.getenv('YTB_REFRESH_TOKEN')
        
        if not (client_id and client_secret and refresh_token):
            print("Missing YouTube credentials")
            return None
        
        credentials = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret
        )
        credentials.refresh(Request())
        return build('youtube', 'v3', credentials=credentials)
    except Exception as e:
        print(f"Auth error: {e}")
        return None

def upload_to_youtube(video_file, articles):
    """Upload video to YouTube as a Short."""
    
    if not os.path.exists(video_file):
        print(f"Video file not found: {video_file}")
        return None
    
    try:
        youtube = get_authenticated_service()
        if not youtube:
            return None
        
        title = "News Shorts - " + articles[0]['title'][:60]
        description = "\n".join([f"- {a['title']}\n{a['link']}" for a in articles])
        
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['news', 'shorts', 'youtube'],
                'categoryId': '25'
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(video_file, mimetype='video/mp4')
        request = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        )
        
        response = request.execute()
        video_id = response['id']
        url = f"https://youtube.com/shorts/{video_id}"
        print(f"Video uploaded: {url}")
        return url
    except Exception as e:
        print(f"Upload error: {e}")
        return None
