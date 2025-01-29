import os
import aiohttp
import asyncio
import random
import time
from bs4 import BeautifulSoup
from utils import get_urls, generate_filename

WAIT_TIME = 20

class HTMLDownloader:
    def __init__(self, download_to: str):
        self.watch_dir = download_to
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        if not os.path.exists(self.watch_dir):
            os.makedirs(self.watch_dir)

    async def download_from_url(self, url: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=60) as response:
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, "html.parser")
                    
                    # Generate a filename based on the URL\
                    filename = generate_filename(url)
                    filepath = os.path.join(self.watch_dir, filename)
                    
                    # Save the prettified soup
                    with open(filepath, "w", encoding="utf-8") as file:
                        file.write(soup.prettify())
                    
                    print(f"Downloaded and saved: {filepath}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

    async def download_multiple(self):
        urls = get_urls()
        tasks = [self.download_from_url(url) for url in urls]
        await asyncio.gather(*tasks)


async def main():
    while True:
        downloader = HTMLDownloader("/home/meyigi/Downloads")
        await downloader.download_multiple()
        print(f"waiting {WAIT_TIME} sec\n\n")
        time.sleep(random.uniform(WAIT_TIME*0.8, WAIT_TIME*1.2))

asyncio.run(main())