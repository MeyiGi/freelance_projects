from bs4 import BeautifulSoup
from typing import List, Dict

import requests
import random
import pandas as pd

def read_txt_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]

def extract_product(url) -> Dict:

    def scrape_specific(target: str) -> str:
        description = soup.select("#product-extra-information p")

        if target == "Bracelet":
            for i in range(len(description)):
                if target in description[i].text:
                    return description[i+1].text.strip()
                
            return ""

        for it in description:
            if target in it.text:
                return it.text.split(":")[-1].strip()
        
        return ""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    item = {}

    item["title"] = soup.select_one(".h2").text
    item["condition"] = random.choice(["good", "very good", "excellent"])
    item["box, paper, tags, card, other (multiple)"] = "\n".join([item.text for item in soup.select(".product-info__block-item p")])

    item["manufacturer"] = ""
    for brand in BRANDS:
        if brand in item["title"]:
            item["manufacturer"] = brand
            break
    try:
        item["collection"] = soup.select_one(".product-info__block-item p:nth-child(1)").text
    except Exception as e:
        item["collection"] = soup.select_one("meta+ p").text

    try:
        item["reference-number"] = item["title"].split("Ref. ")[-1].split()[0]
    except Exception as e:
        item["reference-number"] = ""

    item["year"] = soup.select_one(".badge--custom:nth-child(2)").text.strip()
    item["case-size"] = ""

    item["case-material"] = soup.select_one(".badge--custom:nth-child(1)").text.strip()
    item["bracelet"] = scrape_specific("Bracelet")
    item["dial-color"] = scrape_specific("Dial")
    item["case"] = scrape_specific("Case")
    item["bezel"] = scrape_specific("Bezel")
    item["bezel-material"] = item["case-material"]
    item["warranty"] = "1 year"
    item["website-url"] = url

    images = ["https:" + item.get("src") for item in soup.select(".product-gallery__thumbnail img")]
    for i in range(20):
        try:
            item[f"image-{i}"] = images[i]
        except Exception as e:
            item[f"image-{i}"] = ""
    
    return item

BRANDS = read_txt_file("brands.txt")
MATERIALS = read_txt_file("materials.txt")

# ---- main ----
response = requests.get("https://oliverandclarke.com/collections/all-watches")
soup = BeautifulSoup(response.text, "html.parser")

products = soup.select(".product-card")
items = []
for product in products:
    is_soldout = product.select_one(".badge--custom")
    if is_soldout:
        continue
    url = "https://oliverandclarke.com" + product.select_one("a.product-title").get("href")
    print(url)
    items.append(extract_product(url=url))

response = requests.get("https://oliverandclarke.com/collections/all-watches?page=2")
soup = BeautifulSoup(response.text, "html.parser")
products = soup.select(".product-card")
for product in products:
    is_soldout = product.select_one(".badge--custom")
    if is_soldout:
        continue
    url = "https://oliverandclarke.com" + product.select_one("a.product-title").get("href")
    print(url)
    items.append(extract_product(url=url))

df = pd.DataFrame(items)
df.to_excel("output.xlsx", index=False) 