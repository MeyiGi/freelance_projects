from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import List, Dict
import time
import pandas as pd

offset = 6
output_name = "output6.xlsx"

#freelance_projects/web_scrapung_watches/themarinvault  

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    driver.get(f"https://www.themarinvault.com/store/All-Watches-c63091048?offset={offset * 100}")

    items = parse(driver, wait)

    df = pd.DataFrame(items)
    df.to_excel(output_name, index=False)

    driver.quit()

def parse(driver: webdriver.Chrome, wait: WebDriverWait) -> List[Dict]:
    products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.grid-product__image')))
    product_urls = []
    items = []

    for product in products:
        try:
            sold_out_label = product.find_element(By.CSS_SELECTOR, ".label__text")
            if "sold out" in sold_out_label.text.lower():
                continue  # Skip sold out products
        except Exception:
            # If the element is not found, it means the product is not sold out
            pass

        product_urls.append(product.get_attribute("href"))

    for product_url in product_urls:
        items.append(parse_product(url=product_url, driver=driver, wait=wait))

    return items

def parse_product(url: str, driver: webdriver.Chrome, wait: WebDriverWait) -> Dict:

    def parse_specific(target: str) -> str:
        try:
            for it in joined:
                text = it.text.lower()
                if target in text:
                    if target in ["brand", "reference number", "case size", "year"]:
                        return text.split(":")[-1]

                    return text
                
            return "" 
        except Exception as e:
            return ""
        
    def scrape_material() -> str:
        materials = ["stainless steel", "titanium", "gold", "ceramic", "sapphire", "metal", "leather", "silicone", "glass"]

        for material in materials:
            if material in item["title"].lower():
                return material
            
        return ""
    
    driver.get(url=url)
    item = {}
    print(url)

    try:
        attributes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-details__product-attributes div")))
    except Exception as e:
        attributes = []

    try:
        description = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-details__product-description p")))
    except Exception as e:
        description = ""

    try:
        joined = attributes + description
    except Exception as e:
        joined = []

    # parsing
    try:
        item["title"] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product-details__product-title"))).text
    except Exception as e:
        item["title"] = ""
    
    try:
        item["description"] = "\n\n".join([element.text.strip() for element in description])
    except Exception as e:
        item["description"] = ""
    item["condition"] = parse_specific("overall")
    item["manufacturer"] = parse_specific("brand")
    item["reference-number"] = parse_specific("reference number")
    item["case-size"] = parse_specific("case size")
    item["year"] = parse_specific("year")
    item["case-material"] = scrape_material()
    item["band-material"] = item["case-material"]
    item["dial"] = parse_specific("dial")
    item["crystal"] = parse_specific("crystal")
    item["hands"] = parse_specific("movement")
    item["bezel"] = parse_specific("bezel")
    item["power-reserve"] = parse_specific("power reserve")
    item["functions"] = parse_specific("function")
    item["url"] = url

    images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".details-gallery__image img")))
    
    for i in range(15):
        try:
            item[f"image-{i}"] = images[i].get_attribute("src")
        except Exception as e:
            item[f"image-{i}"] = ""

    return item



if __name__ == "__main__":
    main()