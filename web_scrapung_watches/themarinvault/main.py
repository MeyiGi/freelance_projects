import concurrent.futures
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import List, Dict
import pandas as pd

# Initialize a global result list to collect items from all threads
res = []

def main():
    # Use ThreadPoolExecutor to run fetch_data concurrently for each offset
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_data, range(12)))

    # Flatten the results list and save to Excel
    for items in results:
        res.extend(items)

    df = pd.DataFrame(res)
    df.to_excel("output.xlsx", index=False)

def fetch_data(offset: int) -> List[Dict]:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)
    
    driver.get(f"https://www.themarinvault.com/store/All-Watches-c63091048?offset={offset * 100}")
    items = parse(driver, wait)
    driver.quit()
    
    return items

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
            pass  # Product is not sold out if element not found
            
        try:
            product_urls.append(product.get_attribute("href"))
        except Exception as e:
            continue

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
        except Exception:
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
    except Exception:
        attributes = []

    try:
        description = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-details__product-description p")))
    except Exception:
        description = ""

    joined = attributes + description if attributes and description else []

    item["title"] = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product-details__product-title"))).text
    item["condition"] = parse_specific("overall")
    item["box, paper, tags, card, other (multiple)"] = parse_specific("box")
    item["manufacturer"] = parse_specific("brand")
    item["collection"] = ""
    item["reference-number"] = parse_specific("reference number")
    item["year"] = parse_specific("year")
    item["case-size"] = parse_specific("case size")
    item["case-material"] = scrape_material()
    item["band-material"] = item["case-material"]
    item["dial"] = parse_specific("dial")
    item["case"] = item["case-size"] + "\n" + item["case-material"]
    item["bezel"] = parse_specific("bezel")
    item["bezel-material"] = item["band-material"]
    item["warranty"] = parse_specific("warranty")
    item["url"] = url

    images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".details-gallery__image img")))
    for i in range(20):
        try:
            item[f"image-{i}"] = images[i].get_attribute("src")
        except IndexError:
            item[f"image-{i}"] = ""

    return item

if __name__ == "__main__":
    main()
