import random
import re
from datetime import datetime

def get_urls(filepath="track_urls.txt"):
    with open(filepath, "r") as file:
        # Read lines, strip whitespace, and remove duplicates
        urls = {line.strip() for line in file if line.strip()}
    return list(urls)


def sanitize_filename(filename):
    # Replace any invalid characters with an underscore
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def generate_filename(url):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if "naver" in url and "search" in url:
        filename = f"www.naver.com_search{random.randint(10, 99)}"
    elif "naver" in url and "main" in url:
        filename = f"www.naver.com_main{random.randint(10, 99)}"
    else:
        filename = url.split("//")[-1].replace("/", "_")

    # Sanitize the filename before returning it
    filename = sanitize_filename(filename)

    return filename + current_time + ".html"