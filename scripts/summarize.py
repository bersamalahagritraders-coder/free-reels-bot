"""Article Summarization - Extracts key points from articles."""

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizer import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import re

def summarize_article(text, sentences=2):
    """Summarize article text using TextRank."""
    
    if not text or len(text.strip()) < 50:
        return text[:200]
    
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = TextRankSummarizer()
        summary_sentences = summarizer(parser.document, sentences_count=sentences)
        summary = " ".join([str(s) for s in summary_sentences])
        return summary if summary else text[:200]
    except Exception as e:
        print(f"Summarization error: {e}. Using first 200 chars.")
        return text[:200]

def clean_text(text):
    """Remove HTML tags and extra whitespace."""
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    return text.strip()
