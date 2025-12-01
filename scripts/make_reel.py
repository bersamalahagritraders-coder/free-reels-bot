"""Create vertical video reel with text overlays and audio."""

from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import os

def create_video_reel(summaries, audio_file, articles, output="reel.mp4"):
    """Create a 1080x1920 vertical video reel."""
    
    print("Creating video reel...")
    width, height = 1080, 1920
    duration_per_text = 3
    
    try:
        # Load background and audio
        audio = AudioFileClip(audio_file) if audio_file else None
        duration = audio.duration if audio else (len(summaries) * duration_per_text)
        
        # Create text clips for each summary
        clips = []
        current_time = 0
        
        for i, summary in enumerate(summaries):
            txt_clip = TextClip(summary, fontsize=40, color='white', 
                              method='caption', size=(1000, 400),
                              font='assets/fonts/Inter.ttf')
            txt_clip = txt_clip.set_position('center').set_duration(duration_per_text)
            txt_clip = txt_clip.set_start(current_time)
            clips.append(txt_clip)
            current_time += duration_per_text
        
        # Create color clip as background
        bg = ColorClip(size=(width, height), color=(30, 30, 30)).set_duration(duration)
        
        # Composite
        final = CompositeVideoClip([bg] + clips, size=(width, height))
        
        if audio:
            final = final.set_audio(audio)
        
        final.write_videofile(output, fps=24, codec='libx264', audio_codec='aac')
        print(f"Video saved: {output}")
        return output
        
    except Exception as e:
        print(f"Video creation error: {e}")
        return None
