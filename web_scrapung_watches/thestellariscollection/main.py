import httpx
import re
import pandas as pd
from httpx import Limits
from bs4 import BeautifulSoup
from typing import List
import asyncio

base_url = "https://www.thestellariscollection.com"
url = f"{base_url}/store"

async def main():
    limits = Limits(max_connections=100)
    async with httpx.AsyncClient(limits=limits, timeout=30) as client:
        soup: BeautifulSoup = await start_requests(client, url=url)
        results = await parse(client, soup=soup)

        df = pd.DataFrame(results)
        df.to_excel('output.xlsx', sheet_name='Sheet1', index=False)

async def parse(client: httpx.AsyncClient, soup: BeautifulSoup) -> List[dict]:
    products = soup.select(".grid-item")
    items = []

    tasks = []
    for product in products:
        is_soldout = product.select_one(".product-mark")
        if is_soldout:
            continue

        link = product.select_one(".grid-item-link.product-lists-item")["href"]
        product_url = base_url + link
        print(product_url)
        tasks.append(parse_product(client, product_url))

    items = await asyncio.gather(*tasks)
    return items

async def parse_product(client: httpx.AsyncClient, url: str) -> dict:
    response = await client.get(url=url)
    soup = BeautifulSoup(response.text, "html.parser")

    item = {}
    
    item["title"] = soup.select_one("h1.ProductItem-details-title").text.strip()
    
    # Replace 'scrape_specific' calls with an async version
    item["condition"] = await scrape_specific(soup, "condition")
    item["box-paper"] = await scrape_specific(soup, "box")
    item["manufacturer"] = await scrape_specific(soup, "Brand")
    item["reference-number"] = await scrape_specific(soup, "Reference Number")
    item["case-size"] = await scrape_specific(soup, "Case Size")
    item["date"] = await scrape_specific(soup, "Year of Production")
    item["case-material"] = await scrape_specific(soup, "Case Material")
    item["band-material"] = await scrape_specific(soup, "Clasp Material")
    item["dial-color"] = await scrape_specific(soup, "Dial")
    item["crystal"] = await scrape_specific(soup, "Crystal")
    item["hands"] = await scrape_specific(soup, "Movement")
    item["sub-dials"] = ""
    item["bezel"] = ""
    item["bezel-material"] = await scrape_specific(soup, "Bezel Material")
    item["caliber"] = await scrape_specific(soup, "Movement Caliber")
    item["power-reserve"] = await scrape_specific(soup, "Power Reserve")
    
    date_info = await scrape_specific(soup, "date")
    item["warranty"] = date_info.split("|")[1] if "|" in date_info else ""
    item["calendar"] = date_info.split("|")[0] if "|" in date_info else ""
    
    item["function"] = await scrape_specific(soup, "Functions")
    item["website-url"] = url

    images = [item.get("data-image") for item in soup.select('div[aria-label="Gallery thumbnails"] button img')]
    for i in range(20):
        try:
            item[f"image-{i}"] = images[i]
        except Exception as e:
            item[f"image-{i}"] = ""

    return item

async def scrape_specific(soup: BeautifulSoup, target: str) -> str:
    description = soup.select(".ProductItem-details-excerpt-below-price p")

    if target in ["condition", "box"]:
        for section in description:
            text = section.text.strip()
            if target in text:
                return text.split('.')[0] + '.'
        return ""
    
    if target in ["date"]:
        for section in description:
            text = section.text.strip()
            if "box" in text:
                dates = re.findall(r'\b(\d{4})\b', text)
                date = dates[0] if dates else ""
                warranty = dates[1] if len(dates) > 1 else ""
                return f"{date}.|{warranty}."
        return ""

    for section in description:
        text = section.text.strip()
        if target in text:
            return text.split(":")[1].strip()

    return ""

async def start_requests(client: httpx.AsyncClient, url: str) -> BeautifulSoup:
    response = await client.get(url=url, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

if __name__ == "__main__":
    asyncio.run(main())
