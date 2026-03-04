import os
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    
    return groq_api_key


def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split large text into smaller overlapping chunks
    
    Example:
    Text: "Hello world this is a test"
    chunk_size=5 words → ["Hello world this is a", "is a test"]
    overlap=2 → chunks share 2 words (so we don't lose context)
    """
    words = text.split()
    chunks = []
    
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
    
    return chunks


def clean_text(text):
    """Remove extra spaces, newlines from text"""
    text = " ".join(text.split())
    return text.strip()