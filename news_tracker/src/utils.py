import random
import re
import os
from datetime import datetime

def get_titles(arr):
    return list(map(lambda x: x.split("|")[0], arr))

def get_titles_from_tuple(arr):
    return list(map(lambda x: x[0], arr))

def get_urls(filepath="track_urls.txt"):
    with open(filepath, "r") as file:
        # Read lines, strip whitespace, and remove duplicates
        urls = {line.strip() for line in file if line.strip()}
    return list(urls)

def generate_filename(url):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if "naver" in url and "search" in url:
        filename = f"www.naver.com_search{random.randint(10, 99)}"
    elif "naver" in url and "main" in url:
        filename = f"www.naver.com_main{random.randint(10, 99)}"
    else:
        filename = url.split("//")[-1].replace("/", "_")

    return filename + current_time + ".html"

def truncate_string(s: str, max_length: int) -> str:
    if len(s) > max_length:
        return s[:max_length] + "..."
    return s

def clean_text(text):
    """
    Removes garbage or incomplete sentences from the input text.
    
    Args:
        text (str): The input text containing garbage or incomplete sentences.
    
    Returns:
        str: Cleaned text with garbage removed.
    """
    # Split text into sentences using punctuation as a delimiter
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Keep only sentences that are meaningful (e.g., longer than a few words)
    cleaned_sentences = [sentence for sentence in sentences if len(sentence.split()) > 3]

    # Rejoin the cleaned sentences into a single string
    cleaned_text = ' '.join(cleaned_sentences)

    return cleaned_text

def remove_links(text):
    """
    Removes all links (URLs) from the input text.
    
    Args:
        text (str): The input text containing links.
    
    Returns:
        str: Text with all links removed.
    """
    # Use regex to match and remove URLs
    cleaned_text = re.sub(r'http[s]?://\S+', '', text)
    return cleaned_text.strip()

def get_eng_path():
    return os.path.join(os.getcwd() + "/config/.env")