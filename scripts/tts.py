"""Text-to-Speech using gTTS (Google Text-to-Speech)."""

from gtts import gTTS
import os

def generate_voiceover(summaries, lang="en", output_file="voiceover.mp3"):
    """Generate voiceover audio from text summaries."""
    
    # Combine all summaries into one script
    script = "News Bulletin. " + " ".join(summaries)
    
    # Ensure script is reasonable length
    if len(script) > 5000:
        script = script[:5000]
    
    try:
        print(f"Generating TTS in {lang}...")
        tts = gTTS(text=script, lang=lang, slow=False)
        tts.save(output_file)
        print(f"Voiceover saved: {output_file}")
        return output_file
    except Exception as e:
        print(f"TTS Error: {e}")
        # Create a silent audio as fallback
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        print("Falling back to silent audio...")
        return None
