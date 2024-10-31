from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin

import requests
import pandas as pd


class WebSpider:
    items = []
    base_url = "https://www.arevandco.com/"
    urls = [
        "https://www.arevandco.com/collections/pre-owned?page=1", 
        "https://www.arevandco.com/collections/pre-owned?page=2",
    ]

    def start_requests(self):
        for url in self.urls:
            response = requests.get(url=url)
            soup = BeautifulSoup(response.text, "html.parser")

            self.items.extend(self.parse(soup))

        self.make_excel_file(items=self.items)


    def parse(self, response: BeautifulSoup) -> List[Dict]:
        products = response.select(".product-block")
        items = []

        for product in products:
            is_soldout = product.select_one("span.product-label.unavailable")
            if is_soldout:
                continue

            link = product.select_one("a.caption").get("href")
            url = urljoin(self.base_url, link)

            product_response = requests.get(url=url)
            soup = BeautifulSoup(product_response.text, "html.parser")

            items.append(self.parse_product(response=soup, url=url))

        return items
            

    def parse_product(self, response: BeautifulSoup, url: str) -> Dict:
        def scrape_from_table(target: str) -> str:
            for row in rows:
                column = row.select_one("td:nth-child(1)").text
                if target in column:
                    return row.select_one("td:nth-child(2)").text.strip()
                
            return ""
        
        rows = response.select("table tr")
        item = {}

        item["title"] = response.select_one(".h2").text
        item["condition"] = scrape_from_table("Condition")
        item["box, paper, tags, card, other (multiple)"] = scrape_from_table("Scope of delivery")
        item["manufacturer"] = scrape_from_table("Brand")
        item["Collection"] = ""
        item["reference-number"] = scrape_from_table("Reference number")
        item["year"] = scrape_from_table("Year of production")
        item["case-size"] = scrape_from_table("Case diameter")
        item["case-material"] = scrape_from_table("Case material")
        item["band-material"] = scrape_from_table("Bracelet material")
        item["dial-color"] = scrape_from_table("Dial")
        item["case"] = item["case-size"] + '\n' + item["case-material"]
        item["bezel"] = scrape_from_table("Bezel")
        item["bezel-material"] = item["case-material"]
        item["warranty"] = "1 year"
        item["website-url"] = url

        images = ["https:" + item.get("data-src") for item in response.select(".theme-img img")]
        for i in range(20):
            try:
                item[f"image-{i}"] = images[i]
            except Exception as e:
                item[f"image-{i}"] = ""

        return item
    
    def make_excel_file(self, items, filename="output.xlsx") -> None:
        df = pd.DataFrame(items)
        df.to_excel(filename, index=False)


if __name__ == "__main__":
    object = WebSpider()
    object.start_requests()