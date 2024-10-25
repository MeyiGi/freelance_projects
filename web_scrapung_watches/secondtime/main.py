import httpx
import re
import pandas as pd
from httpx import Limits
from bs4 import BeautifulSoup
from typing import List
import asyncio

base_url = "https://secondtime.com"

async def main():
    limits = Limits(max_connections=100)
    async with httpx.AsyncClient(limits=limits, timeout=30) as client:
        results = []

        for page in range(1, 7):
            url = f"{base_url}/new-arrivals/?page={page}"
            soup: BeautifulSoup = await start_requests(client, url=url)
            results.extend(await parse(client, soup=soup))

        df = pd.DataFrame(results)
        df.to_excel('output.xlsx', sheet_name='Sheet1', index=False)

async def parse(client: httpx.AsyncClient, soup: BeautifulSoup) -> List[dict]:
    products = soup.select("#product-listing-container .product")
    items = []

    tasks = []
    for product in products:
        product_url = product.select_one("h4.card-title a")["href"]
        print(product_url)
        tasks.append(parse_product(client, product_url))

    items = await asyncio.gather(*tasks)
    return items

async def parse_product(client: httpx.AsyncClient, url: str) -> dict:
    response = await client.get(url=url)
    soup = BeautifulSoup(response.text, "html.parser")

    item = {}
    
    item["title"] = soup.select_one(".productView-details .productView-title").text.strip()
    
    # Replace 'scrape_specific' calls with an async version
    item["condition"] = await scrape_specific(soup, "condition")
    item["box-paper"] = await scrape_specific(soup, "box")
    item["manufacturer"] = await scrape_specific(soup, "Brand")
    item["reference-number"] = await scrape_specific(soup, "Reference Number")
    item["case-size"] = ""
    item["date"] = await scrape_specific(soup, "date")
    item["case-material"] = await scrape_specific(soup, "material")
    item["band-material"] = await scrape_specific(soup, "material")
    item["dial-color"] = await scrape_specific(soup, "dial")
    item["crystal"] = ""
    item["hands"] = ""
    item["sub-dials"] = ""
    item["bezel"] = await scrape_specific(soup, "bezel")
    item["bezel-material"] = await scrape_specific(soup, "material")
    item["caliber"] = ""
    item["power-reserve"] = ""
    item["warranty"] = await scrape_specific(soup, "warranty")
    item["calendar"] = await scrape_specific(soup, "date")
    
    item["function"] = ""
    item["website-url"] = url

    images = [item.get("src") for item in soup.select('.productView-imageCarousel-nav-item-img-container img')]
    for i in range(20):
        try:
            item[f"image-{i}"] = images[i]
        except Exception as e:
            item[f"image-{i}"] = ""

    return item

async def scrape_specific(soup: BeautifulSoup, target: str) -> str:
    description = soup.select(".productView-desc-content span")

    if target in ["condition", "bezel", "warranty"]:
        for section in description:
            text = section.text.strip().lower()
            if target in text:
                if target == "condition":
                    return text.split(':')[-1] + '.'
                else:
                    return text
            
        for section in soup.select("p"):
            text = section.get_text().lower()
            if target in text:
                text = text.split(";")[0]
                if "condition" not in text:
                    return text
                
                return text.split(":")[-1]
        return ""

    if target in ["box"]:
        for section in description:
            text = section.text.strip()
            if target in text:
                return text.split(':')[-1] + '.'
        return ""
    
    if target in ["date"]:
        title = soup.select_one(".productView-details .productView-title").text.strip()
        try:
            match = re.search(r'\b(20\d{2})\b', title).group(0)
        except Exception as e:
            match = ""
        return match
     
    if target == "Brand":
        title = soup.select_one(".productView-details .productView-title").text.strip()
        brand = re.split(r'(\d)', title, 1)[0]
        return brand
    
    if target == "Reference Number":
        title = soup.select_one(".productView-details .productView-title").text.strip()
        try:
            ref_number = title.split("Ref ")[1].split()[0]
        except Exception as e:
            ref_number = ""

        return ref_number
    
    if target == "material":
        materials = ["stainless steel", "titanium", "gold", "platinum", "ceramic", "aluminum"]
        title = soup.select_one(".productView-details .productView-title").text.strip().lower()

        for material in materials:
            if material in title:
                return material
            
        return ""
    
    if target == "dial":
        title = soup.select_one(".productView-details .productView-title").text.strip().lower()
        try:
            dial = title.split(" dial")
            if len(dial) > 1:
                dial = dial.split()[-1]
            else:
                dial = ""
        except Exception as e:
            dial = ""

        return dial
    

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
