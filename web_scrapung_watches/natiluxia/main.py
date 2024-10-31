from bs4 import BeautifulSoup
from typing import List

import pandas as pd
import random
import requests



def read_txt_file(filename: str) -> List:
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]
    
def scrape_box_and_papers(soup) -> str:
    description = soup.select(".product__description p")

    if len(description) == 1:
        description = description[0].get_text(separator="\n").split("\n")

        for item in description:
            if "box" in item.lower() or "papers" in item.lower() or "tags" in item.lower() or "card" in item.lower():
                return item.strip()  # Return the entire line if it contains any of the keywords
            
        return ""

    for item in description:
        if "box" in item.text.lower() or "papers" in item.text.lower() or "tags" in item.text.lower() or "card" in item.text.lower():
            return item.text.strip()  # Return the entire line if it contains any of the keywords
    return ""

def scrape_specific(target: str) -> str:
    description = soup.select(".product__description p")
    if len(description) == 1:
        description = description[0].get_text(separator="\n").split("\n")

        for item in description:
            if target in item:
                return item.split(":")[-1].strip().lower()
            
        return ""

    for item in description:
        if target in item.text:
            return item.text.split(":")[-1].strip().lower()
        
    return ""



dial_colors = read_txt_file("dial_colors.txt")
materials = read_txt_file("materials.txt")
urls = read_txt_file("urls.txt")

items = []


for url in urls:
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "html.parser")

    item = {}

    item["title"] = soup.select_one("h1").text
    item["condition"] = "Pre-Owned"
    item["box, paper, tags, card, other (multiple)"] = scrape_box_and_papers(soup)
    item["manufacturer"] = scrape_specific("Brand")
    item["collection"] = "" # I will add them later
    item["reference number"] = "" # I will add them later
    item["year"] = "" # I will add them later
    item["case-size"] = scrape_specific("Case Size")
    item["case-material"] = scrape_specific("Case:")
    item["band-material"] = scrape_specific("Bracelet:")

    item["dial-color"] = ""
    color = scrape_specific("Dial")
    for dial in dial_colors:
        if dial in color:
            item["dial-color"] = dial
            break

    item["case"] = scrape_specific("Case:")
    item["bezel"] = scrape_specific("Bezel")

    item["bezel-material"] = ""
    mat = item["bezel"]
    for material in materials:
        if material in mat:
            item["bezel-material"] = material
            break

    item["warranty"] = "6 months"
    item["website-url"] = url

    images = ["https:" + item.get("src") for item in soup.select(".product__media-item img")]
    
    for i in range(20):
        try:
            item[f"image-{i}"] = images[i]
        except Exception as e:
            item[f"image-{i}"] = ""

    items.append(item)

    for key, value in item.items():
        print(f"{key} --> {value}")

    print('\n')

df = pd.DataFrame(items)
df.to_excel("output.xlsx", index=False)